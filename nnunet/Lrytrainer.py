from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.cuda.amp import GradScaler, autocast
import torch
import numpy as np
from typing import Union, List, Tuple


class CustomTrainerV2(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device('cuda')):
        super().__init__(plans, configuration, fold, dataset_json, device)

        # 自定义超参数
        self.initial_lr = 1e-3  # 初始学习率
        self.weight_decay = 1e-4  # 权重衰减
        self.num_epochs = 300  # 总训练轮次
        self.enable_amp = True  # 启用混合精度
        self.grad_clip = 1.0  # 梯度裁剪阈值
        self.eta_min = 1e-6  # 余弦退火最低学习率

        # 初始化AMP梯度缩放器
        self.scaler = GradScaler(enabled=self.enable_amp)

    def build_network_architecture(self, *args, **kwargs):
        # 继承基础网络构建逻辑
        network = super().build_network_architecture(*args, **kwargs)

        # === 插入SE注意力模块到解码器最后一层 ===
        from torch import nn
        class SEBlock(nn.Module):
            def __init__(self, channel, reduction=16):
                super().__init__()
                self.avg_pool = nn.AdaptiveAvgPool2d(1)
                self.fc = nn.Sequential(
                    nn.Linear(channel, channel // reduction),
                    nn.ReLU(inplace=True),
                    nn.Linear(channel // reduction, channel),
                    nn.Sigmoid()
                )

            def forward(self, x):
                b, c, _, _ = x.size()
                y = self.avg_pool(x).view(b, c)
                y = self.fc(y).view(b, c, 1, 1)
                return x * y.expand_as(x)

        # 修改解码器结构
        last_decoder = network.decoder[-1]
        last_decoder.conv = nn.Sequential(
            last_decoder.conv,
            SEBlock(last_decoder.conv.out_channels)
        )
        return network

    def configure_optimizers(self):
        # 使用AdamW优化器替代默认SGD
        optimizer = AdamW(
            self.network.parameters(),
            lr=self.initial_lr,
            weight_decay=self.weight_decay
        )

        # 余弦退火学习率策略
        lr_scheduler = CosineAnnealingLR(
            optimizer,
            T_max=self.num_epochs,  # 周期长度=总epoch数
            eta_min=self.eta_min
        )
        return optimizer, lr_scheduler

    def _build_loss(self):
        # 混合Dice + Focal Loss
        from nnunetv2.training.loss.dice import MemoryEfficientSoftDiceLoss
        from nnunetv2.training.loss.compound_losses import DC_and_CE_loss

        class FocalLoss(nn.Module):
            def __init__(self, alpha=0.25, gamma=2.0):
                super().__init__()
                self.alpha = alpha
                self.gamma = gamma

            def forward(self, inputs, targets):
                ce_loss = torch.nn.functional.cross_entropy(inputs, targets, reduction='none')
                pt = torch.exp(-ce_loss)
                return (self.alpha * (1 - pt) ** self.gamma * ce_loss).mean()

        # 基础Dice损失
        dice_loss = DC_and_CE_loss(
            {'batch_dice': self.configuration_manager.batch_dice, 'smooth': 1e-5},
            {}, weight_ce=1, weight_dice=1,
            ignore_label=self.label_manager.ignore_label,
            dice_class=MemoryEfficientSoftDiceLoss
        )

        # 混合损失
        focal_loss = FocalLoss()
        total_loss = lambda x, y: dice_loss(x, y) + 0.5 * focal_loss(x, y)

        # 深度监督包装
        if self.enable_deep_supervision:
            deep_supervision_scales = self._get_deep_supervision_scales()
            weights = np.array([1 / (2 ** i) for i in range(len(deep_supervision_scales))])
            weights[-1] = 1e-6  # 防止DDP报错
            weights /= weights.sum()
            from nnunetv2.training.loss.deep_supervision import DeepSupervisionWrapper
            total_loss = DeepSupervisionWrapper(total_loss, weights)

        return total_loss

    def train_step(self, batch: dict) -> dict:
        data = batch['data'].to(self.device, non_blocking=True)
        target = [t.to(self.device, non_blocking=True) for t in batch['target']]

        # 混合精度训练
        self.optimizer.zero_grad(set_to_none=True)
        with autocast(self.device.type, enabled=self.enable_amp):
            output = self.network(data)
            loss = self.loss(output, target)

        # 梯度裁剪与反向传播
        self.scaler.scale(loss).backward()
        self.scaler.unscale_(self.optimizer)
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), self.grad_clip)
        self.scaler.step(self.optimizer)
        self.scaler.update()
        return {'loss': loss.detach().cpu().item()}

    def get_training_transforms(self, *args, **kwargs):
        # 增强数据增强策略
        tr_transforms = super().get_training_transforms(*args, **kwargs)

        # 添加弹性变形
        from batchgeneratorsv2.transforms.spatial.spatial import SpatialTransform
        tr_transforms.transforms.insert(
            0,
            SpatialTransform(
                patch_size=kwargs['patch_size'],
                do_elastic_deform=True,
                alpha=(0, 1000),
                sigma=(40, 60)
            )
        )

        # 添加对比度扰动
        from batchgeneratorsv2.transforms.intensity.contrast import ContrastTransform
        tr_transforms.transforms.append(
            ContrastTransform(
                contrast_range=(0.75, 1.25),
                preserve_range=True,
                per_channel=True
            )
        )
        return tr_transforms
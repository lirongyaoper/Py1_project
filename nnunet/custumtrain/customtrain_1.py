from nnunetv2.training.loss.compound_losses import DC_and_topk_loss
from nnunetv2.training.loss.deep_supervision import DeepSupervisionWrapper
from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer
import numpy as np
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR

class CustomTrainer(nnUNetTrainer):
    def _build_loss(self):
        # 确保不支持区域标签
        assert not self.label_manager.has_regions, "regions not supported by this trainer"
        # 构建 DC_and_topk_loss 损失函数
        loss = DC_and_topk_loss(
            {"batch_dice": self.configuration_manager.batch_dice, "smooth": 1e-5, "do_bg": False, "ddp": self.is_ddp},
            {"k": 10, "label_smoothing": 0.0},
            weight_ce=1,
            weight_dice=1,
            ignore_label=self.label_manager.ignore_label,
        )
        # 如果启用深度监督
        if self.enable_deep_supervision:
            # 获取深度监督的尺度
            deep_supervision_scales = self._get_deep_supervision_scales()
            # 为每个输出分配权重，随着分辨率降低权重指数衰减
            weights = np.array([1 / (2**i) for i in range(len(deep_supervision_scales))])
            weights[-1] = 0
            # 不使用最低的 2 个输出，归一化权重使其和为 1
            weights = weights / weights.sum()
            # 包装损失函数
            loss = DeepSupervisionWrapper(loss, weights)
        return loss

    def configure_optimizers(self):
        # 配置优化器，使用 Adam 优化器
        optimizer = optim.Adam(self.network.parameters(), lr=self.initial_lr)
        # 配置学习率调度器，每 20 个 epoch 学习率衰减为原来的 0.1 倍
        scheduler = StepLR(optimizer, step_size=20, gamma=0.1)
        return optimizer, scheduler

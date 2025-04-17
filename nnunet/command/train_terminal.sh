format_duration() {
    local total_seconds=$1
    local hours=$((total_seconds / 3600))
    local minutes=$(( (total_seconds % 3600) / 60 ))
    local seconds=$((total_seconds % 60))

    # 动态构建时间字符串
    local time_str=""
    [ $hours -gt 0 ] && time_str+="${hours}小时"
    [ $minutes -gt 0 ] && time_str+="${minutes}分"
    [ $seconds -gt 0 ] && time_str+="${seconds}秒"

    # 处理全零情况（至少1秒）
    [ -z "$time_str" ] && echo "0秒" || echo "$time_str"
}


group_one() {
  echo "预处理命令开始执行"
  nnUNetv2_plan_and_preprocess -d 001 -c 2d 3d_fullres 3d_lowres -np 40 20 20 -pl nnUNetPlannerResEncL --verify_dataset_integrity #内存不足
  nnUNetv2_plan_and_preprocess -d 001 -pl nnUNetPlannerResEncL --verify_dataset_integrity
  nnUNetv2_plan_and_preprocess -d 001 -c 2d -np 24 -pl nnUNetPlannerResEncL
  nnUNetv2_plan_and_preprocess -d 001 -c 3d_fullres  -np 8 -pl nnUNetPlannerResEncL
  nnUNetv2_plan_and_preprocess -d 001 -c 3d_lowres -np 32 -pl nnUNetPlannerResEncL
  echo "预处理完成"
}

group_two() {
  echo "2D U-Net 训练"
#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -d 001 2d 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -d 001 2d 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -d 001 2d 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -d 001 2d 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -d 001 2d 4 -p nnUNetResEncUNetLPlans --npz

  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr lryTrainer -d 001 2d 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr lryTrainer -d 001 2d 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr lryTrainer -d 001 2d 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr lryTrainer -d 001 2d 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr lryTrainer -d 001 2d 4 -p nnUNetResEncUNetLPlans --npz
  echo "2D U-Net 训练完成！！！"
}

group_three(){
  echo "3d_lowres训练"
#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_lowres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_lowres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_lowres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train  001 3d_lowres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_lowres 4 -p nnUNetResEncUNetLPlans --npz
  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_lowres 0 -p nnUNetResEncUNetLPlans --npz -c & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_lowres 1 -p nnUNetResEncUNetLPlans --npz -c & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_lowres 2 -p nnUNetResEncUNetLPlans --npz -c & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_lowres 3 -p nnUNetResEncUNetLPlans --npz -c & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_lowres 4 -p nnUNetResEncUNetLPlans --npz -c
  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr lryTrainer -d 001 3d_lowres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr lryTrainer -d 001 3d_lowres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr lryTrainer -d 001 3d_lowres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr lryTrainer -d 001 3d_lowres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr lryTrainer -d 001 3d_lowres 4 -p nnUNetResEncUNetLPlans --npz
  echo "3d_lowres训练完成！！！"



}

group_four(){
  echo "3d_cascade_fullres训练"

#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_cascade_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_cascade_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_cascade_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train  001 3d_cascade_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_cascade_fullres 4 -p nnUNetResEncUNetLPlans --npz

  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 4 -p nnUNetResEncUNetLPlans --npz
  echo "3d_cascade_fullres训练完成！！！"
}

group_five(){
  echo "3d_fullres 训练"
#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_fullres 4 -p nnUNetResEncUNetLPlans --npz

  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr lryTrainer -d 001 3d_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr lryTrainer -d 001 3d_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr lryTrainer -d 001 3d_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr lryTrainer -d 001 3d_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr lryTrainer -d 001 3d_fullres 4 -p nnUNetResEncUNetLPlans --npz
  echo "3d_fullres 训练完成！！！"
}


START_TIME=$(date +%s)
#group_one || exit 1
group_two || exit 1
group_three || exit 1
group_four || exit 1
group_five || exit 1
END_TIME=$(date +%s)
TOTAL_SECONDS=$((END_TIME - START_TIME))
echo "✅ 所有命令执行完成，总耗时: $(format_duration $TOTAL_SECONDS)"
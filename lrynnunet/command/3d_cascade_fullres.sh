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

3d_cascade_fullres(){
  echo "3d_cascade_fullres训练开始"
#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_cascade_fullres 0 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_cascade_fullres 1 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_cascade_fullres 2 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train  001 3d_cascade_fullres 3 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_cascade_fullres 4 -p nnUNetResEncUNetLP1ans --npz
  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_cascade_fullres 0 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_cascade_fullres 1 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_cascade_fullres 2 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train  001 3d_cascade_fullres 3 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_cascade_fullres 4 -p nnUNetResEncUNetLP1ans --npz

#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 0 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 1 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 2 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 3 -p nnUNetResEncUNetLP1ans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 4 -p nnUNetResEncUNetLP1ans --npz
  echo "3d_cascade_fullres训练完成！！！"
}

START_TIME=$(date +%s)
3d_cascade_fullres || exit 1
END_TIME=$(date +%s)
TOTAL_SECONDS=$((END_TIME - START_TIME))
echo "✅ 所有命令执行完成，总耗时: $(format_duration $TOTAL_SECONDS)"
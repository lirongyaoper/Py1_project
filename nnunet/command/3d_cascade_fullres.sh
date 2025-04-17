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
  #生成npz文件命令
#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_lowres 0 -p nnUNetResEncUNetLPlans --val --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_lowres 1 -p nnUNetResEncUNetLPlans  --val --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_lowres 2 -p nnUNetResEncUNetLPlans --val --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_lowres 3 -p nnUNetResEncUNetLPlans --val --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_lowres 4 -p nnUNetResEncUNetLPlans --val --npz

  echo "3d_cascade_fullres训练开始"
#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_cascade_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_cascade_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_cascade_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train  001 3d_cascade_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_cascade_fullres 4 -p nnUNetResEncUNetLPlans --npz
  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train  001 3d_cascade_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train  001 3d_cascade_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train  001 3d_cascade_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train  001 3d_cascade_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train  001 3d_cascade_fullres 4 -p nnUNetResEncUNetLPlans --npz

#  CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 0 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 1 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 2 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 3 -p nnUNetResEncUNetLPlans --npz & CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr lryTrainer -d 001 3d_cascade_fullres 4 -p nnUNetResEncUNetLPlans --npz
  echo "3d_cascade_fullres训练完成！！！"
}

START_TIME=$(date +%s)
3d_cascade_fullres || exit 1
END_TIME=$(date +%s)
TOTAL_SECONDS=$((END_TIME - START_TIME))
echo "✅ 所有命令执行完成，总耗时: $(format_duration $TOTAL_SECONDS)"



 nnUNetv2_find_best_configuration 001 -c 2d 3d_lowres 3d_fullres 3d_cascade_fullres  -p nnUNetResEncUNetLPlans

 nnUNetv2_predict -d Dataset001_Lung -i INPUT_FOLDER -o OUTPUT_FOLDER -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_cascade_fullres -p nnUNetResEncUNetLPlans
 nnUNetv2_predict -d Dataset001_Lung -i /root/ry/ -o /root/outcome/ -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_cascade_fullres -p nnUNetResEncUNetLPlans

***Once inference is completed, run postprocessing like this:***

nnUNetv2_apply_postprocessing -i OUTPUT_FOLDER -o OUTPUT_FOLDER_PP -pp_pkl_file /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/plans.json
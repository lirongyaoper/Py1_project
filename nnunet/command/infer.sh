

#级联推理
nnUNetv2_predict -d Dataset001_Lung -i /mnt/result/input/ -o /mnt/result/medput/ -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_lowres -p nnUNetResEncUNetLPlans && nnUNetv2_predict -d Dataset001_Lung -i /mnt/result/input/ -o /mnt/result/output/ -c 3d_cascade_fullres -tr nnUNetTrainer -p nnUNetResEncUNetLPlans -prev_stage_predictions /mnt/result/medput/





***Once inference is completed, run postprocessing like this:***

nnUNetv2_apply_postprocessing -i OUTPUT_FOLDER -o OUTPUT_FOLDER_PP -pp_pkl_file /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/plans.json

nnUNetv2_find_best_configuration 001 -c 3d_fullres  -p nnUNetResEncUNetLPlans

nnUNetv2_predict -d Dataset001_Lung -i INPUT_FOLDER -o OUTPUT_FOLDER -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetLPlans
nnUNetv2_predict -d Dataset001_Lung -i /home/lirongyao0916/Documents/infer_nnunet/input/ -o /home/lirongyao0916/Documents/infer_nnunet/output/ -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetLPlans

***Once inference is completed, run postprocessing like this:***

nnUNetv2_apply_postprocessing -i /mnt/result/input/  -o  /mnt/result/output/ -pp_pkl_file /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/plans.json
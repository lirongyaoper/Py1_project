
nnUNetv2_predict -d Dataset001_Lung -i INPUT_FOLDER -o OUTPUT_FOLDER -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_cascade_fullres -p nnUNetResEncUNetLPlans

nnUNetv2_predict -d Dataset001_Lung -i /root/ry/ -o /root/outcome/ -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_lowres -p nnUNetResEncUNetLPlans

nnUNetv2_predict -d Dataset001_Lung -i /root/ry/ -o /root/outcome/ -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_cascade_fullres -p nnUNetResEncUNetLPlans


***Once inference is completed, run postprocessing like this:***

nnUNetv2_apply_postprocessing -i OUTPUT_FOLDER -o OUTPUT_FOLDER_PP -pp_pkl_file /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/plans.json

nnUNetv2_find_best_configuration 001 -c 3d_fullres  -p nnUNetResEncUNetLPlans

nnUNetv2_predict -d Dataset001_Lung -i INPUT_FOLDER -o OUTPUT_FOLDER -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetLPlans
nnUNetv2_predict -d Dataset001_Lung -i /root/ry/ -o /root/outcome/ -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetLPlans

***Once inference is completed, run postprocessing like this:***

nnUNetv2_apply_postprocessing -i /root/outcome/ -o /root/rypp/ -pp_pkl_file /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json /data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/plans.json
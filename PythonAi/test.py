import torch
#1.创建一个tenosr
tensor_1 = torch.tensor([1,2,3])

#2. 观察tensor的属性
print(tensor_1)
print(tensor_1.device)
#3.将tensor转到gpu
if torch.cuda.is_available():
    tensor_1 = tensor_1.cuda()
    print(tensor_1)
    print(tensor_1.device)
# 4. 将tensor 转回cpu
if torch.cuda.is_available():
    tensor_1 = tensor_1.cpu()
    print(tensor_1)
    print(tensor_1.device)
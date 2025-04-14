import torch
print(torch.cuda.is_available())        # 检查CUDA是否可用
print(torch.backends.cudnn.is_available())  # 检查cuDNN是否可用
print(torch.version.cuda)               # 正确获取CUDA版本的方式
print(torch.backends.cudnn.version())   # 获取cuDNN版本
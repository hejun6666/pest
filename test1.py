# 在创建数据集后添加
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 数据增强和预处理
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
train_dataset = datasets.ImageFolder('/root/autodl-tmp/01/data/Agri/train', train_transforms)
val_dataset = datasets.ImageFolder('/root/autodl-tmp/01/data/Agri/val', val_transforms)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)
print("\n===== 数据集诊断信息 =====")
print(f"训练集路径: {train_dataset.root}")
print(f"类别数量: {len(train_dataset.classes)}")
print(f"实际样本数: {len(train_dataset)}")
print(f"Batch数量: {len(train_loader)}")
print(f"理论Batch数: {len(train_dataset)//8} (+{len(train_dataset)%8})")
print("=========================\n")
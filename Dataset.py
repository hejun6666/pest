from torch.utils.data import Dataset, DataLoader

from torchvision import transforms, datasets

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),  # 随机裁剪缩放
    transforms.RandomHorizontalFlip(),  # 水平翻转
    transforms.ColorJitter(brightness=0.2, contrast=0.2),  # 颜色扰动
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # ImageNet标准
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = datasets.ImageFolder(root='C:\\Users\\17832\\PycharmProjects\\pythonProject\\01\\data\\Agri\\train', transform=train_transform)
val_dataset = datasets.ImageFolder(root='C:\\Users\\17832\\PycharmProjects\\pythonProject\\01\\data\\Agri\\val', transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)


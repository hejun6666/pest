# 1. 数据准备
import time

import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

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

import os
from PIL import Image
from tqdm import tqdm  # 进度条支持

#用于检查有损坏的图片
def check_images_v2(root_dir):
    bad_files = []
    # 获取所有图像文件（包含更多格式）
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}

    # 递归遍历所有文件
    for root, _, files in os.walk(root_dir):
        for file in tqdm(files, desc=f"扫描 {root}"):
            ext = os.path.splitext(file)[1].lower()
            if ext not in image_extensions:
                continue

            path = os.path.join(root, file)
            try:
                # 严格检测步骤
                with Image.open(path) as img:
                    img.verify()  # 第一阶段验证

                    # 第二阶段：尝试实际加载和转换
                    img = Image.open(path)  # 重新打开
                    img = img.convert("RGB")  # 强制转换为RGB
                    img.load()  # 完全加载数据

                    # 第三阶段：检查基本属性
                    if img.size[0] == 0 or img.size[1] == 0:
                        raise ValueError("无效的图像尺寸")

            except Exception as e:
                bad_files.append(path)
                print(f"\n损坏文件: {path} | 错误类型: {type(e).__name__} | 错误信息: {str(e)}")

    return bad_files


def delete_files(file_list):
    deleted = 0
    for path in file_list:
        try:
            os.remove(path)
            print(f"已删除: {path}")
            deleted += 1
        except Exception as e:
            print(f"删除失败 [{path}]: {str(e)}")
    return deleted
#
#
# # 带进度提示的检测
# print("=> 正在深度扫描训练集...")
# bad_train = check_images_v2('/root/autodl-tmp/01/data/Agri/train')
# print("\n=> 正在深度扫描验证集...")
# bad_val = check_images_v2('/root/autodl-tmp/01/data/Agri/val')
#
# # 删除处理
# total_deleted = 0
# if bad_train:
#     print(f"\n=> 正在删除 {len(bad_train)} 个训练集损坏文件...")
#     total_deleted += delete_files(bad_train)
# if bad_val:
#     print(f"\n=> 正在删除 {len(bad_val)} 个验证集损坏文件...")
#     total_deleted += delete_files(bad_val)
#
# print(f"\n操作完成！共删除 {total_deleted} 个损坏文件")

train_dataset = datasets.ImageFolder('/root/autodl-tmp/01/data/Agri/train', train_transforms)
val_dataset = datasets.ImageFolder('/root/autodl-tmp/01/data/Agri/val', val_transforms)

# 2. 模型定义（使用MobileNetV2）
def create_model(num_classes=53):
    model = models.mobilenet_v2(pretrained=True)

    # 修改分类器
    in_features = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(in_features, num_classes)
    return model

def train_model(model, train_loader, val_loader, num_epochs=10):
    for epoch in range(num_epochs):
        epoch_start_time = time.time()

        # ===== 训练阶段 =====
        model.train()
        running_loss = 0.0
        processed_samples = 0

        # 添加带进度条的迭代器
        train_iter = tqdm(train_loader,
                          desc=f"Epoch {epoch + 1}/{num_epochs} [Train]",
                          bar_format="{l_bar}{bar:20}{r_bar}",
                          postfix={"loss": "?.???", "lr": f"{optimizer.param_groups[0]['lr']:.2e}"})

        batch_times = []
        for batch_idx, (images, labels) in enumerate(train_iter):
            batch_start = time.time()

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            processed_samples += images.size(0)

            # 更新进度条
            batch_time = time.time() - batch_start
            batch_times.append(batch_time)
            avg_batch_time = sum(batch_times[-10:]) / len(batch_times[-10:])  # 最近10个batch的平均时间

            train_iter.set_postfix({
                "loss": f"{loss.item():.3f}",
                "lr": f"{optimizer.param_groups[0]['lr']:.2e}",
                "speed": f"{images.size(0) / batch_time:.1f} samples/s",
                "eta": f"{avg_batch_time * (len(train_loader) - batch_idx - 1):.0f}s"
            })

        epoch_loss = running_loss / len(train_dataset)
        train_time = time.time() - epoch_start_time

        # ===== 验证阶段 =====
        val_start_time = time.time()
        model.eval()
        correct = 0
        total = 0

        val_iter = tqdm(val_loader,
                        desc=f"Epoch {epoch + 1}/{num_epochs} [Val]  ",
                        bar_format="{l_bar}{bar:20}{r_bar}",
                        postfix={"acc": "?.???"})

        with torch.no_grad():
            for images, labels in val_iter:
                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                # 更新验证进度条
                current_acc = correct / total
                val_iter.set_postfix({
                    "acc": f"{current_acc * 100:.2f}%"
                })

        val_acc = correct / total
        val_time = time.time() - val_start_time
        total_epoch_time = time.time() - epoch_start_time

        # ===== 打印统计信息 =====
        print(f"\nEpoch {epoch + 1:02d}/{num_epochs} Summary:")
        print(f"├── Train Loss: {epoch_loss:.4f}  |  Val Acc: {val_acc * 100:.2f}%")
        print(f"├── LR: {optimizer.param_groups[0]['lr']:.2e}")
        print(f"├── Time: Train {train_time:.1f}s  Val {val_time:.1f}s  Total {total_epoch_time:.1f}s")
        print(
            f"└── Elapsed: {(time.time() - total_start_time) // 3600:.0f}h {((time.time() - total_start_time) % 3600) // 60:.0f}m\n")

        # 保存最佳模型
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')
            print(f"🔥 New best model saved! (Acc: {val_acc * 100:.2f}%)")

        scheduler.step()


if __name__ == '__main__':
    # 创建数据加载器
    batch_size = 8
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    model = create_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # 训练配置
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    # 4. 增强版训练循环
    best_acc = 0.0
    num_epochs = 10
    total_start_time = time.time()

    train_model(model, train_loader, val_loader)

import torch
from torchvision import transforms, models
from PIL import Image
import json
import json
import os


# 自动生成类别映射文件（在数据加载之后添加）
def generate_class_mapping(dataset_path, save_path="class_indices.json"):
    # 获取排序后的类别列表
    classes = sorted(os.listdir(dataset_path))
    # 创建映射字典（与ImageFolder自动生成的顺序一致）
    class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}

    # 保存为JSON文件
    with open(save_path, 'w') as f:
        json.dump(class_to_idx, f, indent=4)

    print(f"类别映射文件已生成：{os.path.abspath(save_path)}")
    return class_to_idx


class CropDiseaseClassifier:
    def __init__(self, model_path, class_map_path):
        # 加载设备配置
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 加载类别映射表
        with open(class_map_path, 'r') as f:
            self.class_map = json.load(f)

        # 加载模型
        self.model = models.mobilenet_v2()
        in_features = self.model.classifier[1].in_features
        self.model.classifier[1] = torch.nn.Linear(in_features, len(self.class_map))
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model = self.model.to(self.device).eval()

        # 定义预处理
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image_path, topk=3):
        """返回前topk个预测结果"""
        img = Image.open(image_path).convert('RGB')
        tensor = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = torch.nn.functional.softmax(self.model(tensor), dim=1)
            probs, indices = torch.topk(outputs, topk)

        return [
            {"class": self.class_map[str(i.item())], "prob": p.item()}
            for p, i in zip(probs.squeeze(), indices.squeeze())
        ]


# 使用示例
classifier = CropDiseaseClassifier(
    model_path="best_model.pth",
    class_map_path="class_indices_inverse.json"  # 需提前生成类别映射文件
)
result = classifier.predict("C:\\Users\\17832\\PycharmProjects\\pythonProject\\01\\data\\Agri\\val\\Corn_Curvularia_leaf_spot\\0b3a35d8-25af-44ae-beed-398f591d5c1b___RS_NLB 0833.JPG")
print(result)  # 输出示例：[{"class": "apple_scab", "prob": 0.92}, ...]

# # 新代码（生成索引到类名的映射）
# import json
#
# # 读取原始JSON文件
# with open("class_indices.json", "r") as f:
#     class_to_idx = json.load(f)  # 原始结构: {"apple_scab": 0, ...}
#
# # 反转字典：索引（转为字符串） → 类名
# idx_to_class = {str(idx): cls for cls, idx in class_to_idx.items()}
#
# # 保存新的JSON文件
# with open("class_indices_inverse.json", "w") as f:
#     json.dump(idx_to_class, f, indent=4)
# 在数据加载后调用（任选train或val路径，需确保两者类别顺序一致）
# generate_class_mapping('/root/autodl-tmp/01/data/Agri/train')
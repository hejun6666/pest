import torch
from model import create_model  # 导入你的模型定义

# 加载训练好的模型
model = create_model(num_classes=53)
model.load_state_dict(torch.load('best_model.pth'))  # 关键！加载.pth文件
model.eval()

# 创建虚拟输入（必须与训练时输入尺寸一致）
dummy_input = torch.randn(1, 3, 224, 224)  # [batch, channels, height, width]

# 导出ONNX
torch.onnx.export(
    model,
    dummy_input,
    "ill-pest.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={
        "input": {0: "batch_size"},
        "output": {0: "batch_size"}
    },
    opset_version=12  # 确保与TensorFlow兼容
)
import onnx
import onnxruntime as ort

# 验证ONNX模型结构
onnx_model = onnx.load("ill-pest.onnx")
onnx.checker.check_model(onnx_model)

# 运行推理测试
ort_session = ort.InferenceSession("ill-pest.onnx")
outputs = ort_session.run(
    None,
    {"input": dummy_input.numpy()}
)
print("ONNX 推理输出形状:", outputs[0].shape)  # 应为(1,53)

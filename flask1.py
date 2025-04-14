# # 文件名：main.py
# import io
# import numpy as np
# from PIL import Image
# import onnxruntime
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
#
# # -------------------- 初始化部分 --------------------
# # 创建FastAPI应用实例
# app = FastAPI(title="图像分类API")
#
# # 加载ONNX模型（自动选择GPU/CPU）
# ort_session = onnxruntime.InferenceSession(
#     "ill-pest.onnx",
#     providers=[
#         'CUDAExecutionProvider',  # 优先使用GPU
#         'CPUExecutionProvider'  # 无法使用GPU时自动回退到CPU
#     ]
# )
#
# # -------------------- 配置常量 --------------------
# # 与训练时完全一致的预处理参数
# IMG_SIZE = (224, 224)  # 图像缩放尺寸
# MEAN = np.array([0.485, 0.456, 0.406])  # 均值
# STD = np.array([0.229, 0.224, 0.225])  # 标准差
#
# # 安全限制
# ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}  # 允许的文件类型
# MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB文件大小限制
#
# # -------------------- 预处理函数 --------------------
# def preprocess_image(image: Image.Image) -> np.ndarray:
#     """
#     修改后的预处理函数，确保输出float32类型
#     """
#     # 调整尺寸并转换为RGB
#     image = image.resize(IMG_SIZE).convert("RGB")
#
#     # 转换为numpy数组（明确指定float32）
#     img_array = np.array(image, dtype=np.float32) / 255.0
#
#     # 标准化参数也转为float32
#     mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
#     std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
#     normalized = (img_array - mean) / std
#
#     # 调整维度并再次确认类型
#     input_tensor = normalized.transpose(2, 0, 1)[np.newaxis, ...]
#     return input_tensor.astype(np.float32)  # 最终保险
#
#
# # -------------------- API端点 --------------------
# @app.post("/predict")
# async def predict_api(file: UploadFile = File(...)):
#     """
#     处理图片分类请求的核心端点
#     处理流程：
#     1. 验证文件合法性
#     2. 读取图片内容
#     3. 预处理
#     4. 模型推理
#     5. 结果解析
#     """
#     # ===== 1. 安全验证 =====
#     if file.content_type not in ALLOWED_MIME_TYPES:
#         raise HTTPException(400, detail="仅支持JPEG/PNG格式图片")
#
#     if file.size > MAX_FILE_SIZE:
#         raise HTTPException(413, detail="文件大小超过5MB限制")
#
#     # ===== 2. 读取图片 =====
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents))  # 从字节流打开图片
#     except Exception as e:
#         raise HTTPException(400, detail=f"图片解析失败: {str(e)}")
#
#     # ===== 3. 预处理 =====
#     try:
#         input_tensor = preprocess_image(image)
#     except Exception as e:
#         raise HTTPException(500, detail=f"预处理错误: {str(e)}")
#
#     # ===== 4. 模型推理 =====
#     try:
#         # 准备ONNX输入（注意名称匹配）
#         ort_inputs = {ort_session.get_inputs()[0].name: input_tensor}
#
#         # 执行推理
#         ort_outputs = ort_session.run(None, ort_inputs)
#         logits = ort_outputs[0]  # 假设第一个输出是分类logits
#     except Exception as e:
#         raise HTTPException(500, detail=f"模型推理失败: {str(e)}")
#
#     # ===== 5. 解析结果 =====
#     try:
#         # 获取最高概率类别
#         predicted_class = int(np.argmax(logits))
#
#         # 计算置信度（softmax概率）
#         probabilities = np.exp(logits) / np.sum(np.exp(logits))
#         confidence = float(probabilities[0, predicted_class])
#     except Exception as e:
#         raise HTTPException(500, detail=f"结果解析失败: {str(e)}")
#
#     return JSONResponse({
#         "class_id": predicted_class,
#         "confidence": round(confidence, 4),  # 保留4位小数
#         "message": "success"
#     })
#
# # -------------------- 启动服务 --------------------
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=5001)

# 修改后的 flask1.py
import io
import numpy as np
import json
import os
from PIL import Image
import onnxruntime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pymysql
from pymysql.cursors import DictCursor

# -------------------- 初始化部分 --------------------
# 创建FastAPI应用实例
app = FastAPI(title="图像分类API")

# 加载ONNX模型（自动选择GPU/CPU）
ort_session = onnxruntime.InferenceSession(
    "ill-pest.onnx",
    providers=[
        'CUDAExecutionProvider',  # 优先使用GPU
        'CPUExecutionProvider'  # 无法使用GPU时自动回退到CPU
    ]
)

# 加载类别索引
with open("class_indices_inverse.json", "r") as f:
    class_indices = json.load(f)

# 数据库连接设置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 替换为你的数据库密码
    'db': 'pest',  # 替换为你的数据库名
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# -------------------- 配置常量 --------------------
# 与训练时完全一致的预处理参数
IMG_SIZE = (224, 224)  # 图像缩放尺寸
MEAN = np.array([0.485, 0.456, 0.406])  # 均值
STD = np.array([0.229, 0.224, 0.225])  # 标准差

# 安全限制
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}  # 允许的文件类型
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB文件大小限制


# -------------------- 预处理函数 --------------------
def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    修改后的预处理函数，确保输出float32类型
    """
    # 调整尺寸并转换为RGB
    image = image.resize(IMG_SIZE).convert("RGB")

    # 转换为numpy数组（明确指定float32）
    img_array = np.array(image, dtype=np.float32) / 255.0

    # 标准化参数也转为float32
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    normalized = (img_array - mean) / std

    # 调整维度并再次确认类型
    input_tensor = normalized.transpose(2, 0, 1)[np.newaxis, ...]
    return input_tensor.astype(np.float32)  # 最终保险


# 数据库查询函数
def query_disease_info(disease_name):
    """
    根据疾病英文名称查询数据库中的详细信息
    """
    # 创建数据库连接
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 使用LIKE进行模糊匹配
            sql = """
            SELECT id, code, name_zh, name_en, description, symptoms, treatment, image_url 
            FROM diseases 
            WHERE name_en LIKE %s OR name_zh LIKE %s
            LIMIT 1
            """
            cursor.execute(sql, (f'%{disease_name}%', f'%{disease_name}%'))
            result = cursor.fetchone()

            if result:
                # 处理NULL值
                for key, value in result.items():
                    if value is None:
                        result[key] = ""
                return result

            return None
    finally:
        connection.close()


# 默认信息（当数据库中没有匹配记录时）
def get_default_info(disease_name):
    is_healthy = 'healthy' in disease_name.lower()
    return {
        'disease_found': False,
        'is_healthy': is_healthy,
        'description': f"这是一种{'健康状态' if is_healthy else '病害或虫害'}。",
        'symptoms': '植物健康，无异常症状。' if is_healthy else '可能出现叶片变色、枯萎、斑点或其他生长异常。',
        'treatment': '继续保持当前的种植管理方式。' if is_healthy else '建议咨询专业农业技术人员获取针对性建议。可考虑适当修剪、使用农药或生物防治方法。'
    }


# -------------------- API端点 --------------------
@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    """
    处理图片分类请求并返回详细的疾病信息
    """
    # ===== 1. 安全验证 =====
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, detail="仅支持JPEG/PNG格式图片")

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(413, detail="文件大小超过5MB限制")

    # ===== 2. 读取图片 =====
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))  # 从字节流打开图片
    except Exception as e:
        raise HTTPException(400, detail=f"图片解析失败: {str(e)}")

    # ===== 3. 预处理 =====
    try:
        input_tensor = preprocess_image(image)
    except Exception as e:
        raise HTTPException(500, detail=f"预处理错误: {str(e)}")

    # ===== 4. 模型推理 =====
    try:
        # 准备ONNX输入（注意名称匹配）
        ort_inputs = {ort_session.get_inputs()[0].name: input_tensor}

        # 执行推理
        ort_outputs = ort_session.run(None, ort_inputs)
        logits = ort_outputs[0]  # 假设第一个输出是分类logits
    except Exception as e:
        raise HTTPException(500, detail=f"模型推理失败: {str(e)}")

    # ===== 5. 解析结果 =====
    try:
        # 获取最高概率类别
        predicted_class = int(np.argmax(logits))

        # 计算置信度（softmax概率）
        probabilities = np.exp(logits) / np.sum(np.exp(logits))
        confidence = float(probabilities[0, predicted_class])

        # 获取类别名称
        disease_name = class_indices.get(str(predicted_class), "未知")

        # 判断是否为健康状态
        is_healthy = 'healthy' in disease_name.lower()

        # 查询数据库获取详细信息
        db_info = query_disease_info(disease_name)

        # 构建响应
        response = {
            "class_id": predicted_class,
            "disease_name": disease_name,
            "confidence": round(confidence * 100, 2),  # 转为百分比
            "is_healthy": is_healthy,
            "message": "success"
        }

        # 添加详细信息
        if db_info:
            # 数据库中有匹配记录
            response.update({
                "disease_found": True,
                "name_zh": db_info["name_zh"],
                "code": db_info["code"],
                "description": db_info["description"],
                "symptoms": db_info["symptoms"],
                "treatment": db_info["treatment"],
                "image_url": db_info["image_url"]
            })
        else:
            # 无匹配记录，使用默认信息
            default_info = get_default_info(disease_name)
            response.update(default_info)

    except Exception as e:
        raise HTTPException(500, detail=f"结果解析失败: {str(e)}")

    return JSONResponse(response)


# -------------------- 启动服务 --------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
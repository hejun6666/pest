import shutil
from pathlib import Path
import logging


def merge_test_to_train(test_root, train_root):
    """
    递归合并测试集到训练集

    参数：
    test_root  -- 测试集根目录（包含类别子文件夹）
    train_root -- 训练集根目录（包含对应类别子文件夹）
    """
    # 配置日志记录
    logging.basicConfig(
        filename='data_merge.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )

    total_moved = 0
    conflict_files = []

    # 遍历所有测试类别
    for test_class_dir in Path(test_root).iterdir():
        if not test_class_dir.is_dir():
            continue

        class_name = test_class_dir.name
        train_class_dir = Path(train_root) / class_name

        # 验证对应训练目录存在性
        if not train_class_dir.exists():
            logging.warning(f"训练目录缺失: {class_name}，已自动创建")
            train_class_dir.mkdir(parents=True, exist_ok=True)

        # 迁移图片文件
        for img_path in test_class_dir.glob('**/*.*'):
            dest_path = train_class_dir / img_path.name

            try:
                if not dest_path.exists():
                    shutil.move(str(img_path), str(dest_path))
                    total_moved += 1
                    logging.info(f"成功移动: {img_path} → {dest_path}")
                else:
                    # 处理文件名冲突（添加_test后缀）
                    new_name = f"{img_path.stem}_test{img_path.suffix}"
                    dest_path = train_class_dir / new_name
                    shutil.move(str(img_path), str(dest_path))
                    conflict_files.append(new_name)
                    logging.warning(f"重命名移动: {img_path} → {dest_path}")
            except Exception as e:
                logging.error(f"移动失败 {img_path}: {str(e)}")

    # 生成报告
    print(f"迁移完成！共处理 {total_moved + len(conflict_files)} 个文件")
    print(f"直接移动: {total_moved}")
    if conflict_files:
        print(f"重命名移动: {len(conflict_files)}")
        print("冲突文件列表:\n" + "\n".join(conflict_files))


# 使用示例
if __name__ == "__main__":
    merge_test_to_train(
        test_root="C:\\Users\\17832\\PycharmProjects\\pythonProject\\01\\data\\Agri\\val",  # 测试集路径
        train_root="C:\\Users\\17832\\PycharmProjects\\pythonProject\\01\\data\\Agri\\train"  # 训练集路径
    )
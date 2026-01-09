from ultralytics import YOLO
import os

# 无论你要训练一个识别什么物体的模型 模型的内部架构都是一样的
model = YOLO('yolo11n.pt')

# 获取 data.yaml 的路径（相对于当前脚本）
data_yaml_path = os.path.join(
    'Valorant object detection image dataset', 
    'data.yaml'
)

# 检查文件是否存在
if not os.path.exists(data_yaml_path):
    # 如果相对路径不存在，尝试绝对路径
    data_yaml_path = r'C:/Users/Leo/Desktop/ultralytics-8.3.86/Valorant object detection image dataset/data.yaml'
    if not os.path.exists(data_yaml_path):
        print(f'错误：找不到 data.yaml 文件')
        print(f'请检查路径：{data_yaml_path}')
        exit(1)

print(f'使用配置文件：{data_yaml_path}')

# 模型训练
model.train(
    # yaml配置文件路径
    data=data_yaml_path,
    # 模型训练轮次 默认50轮 此处可以减小训练轮次
    epochs=50,
    # 数据加载的工作线程数量
    workers=10,
    # 图像大小
    imgsz=640,
    # 批次大小（如果内存不足可以减小）
    batch=16,
    # 验证集比例（从训练集中自动划分，因为 val 目录没有图片）
    val=True,
    # 如果验证集为空，可以设置 split=0.2 来从训练集中划分 20% 作为验证集
    # split=0.2  # 可选：从训练集中划分验证集
)
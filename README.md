# 二维码识别系统使用文档

## 项目简介

本项目是一个基于深度学习的二维码识别系统，支持多种数据输入方式：
- Socket 二进制数据流
- Kafka 消息队列
- 本地图片文件

系统使用 YOLO 模型进行二维码检测，结合 OpenCV 进行二维码解码，能够实时处理图像数据并提取二维码信息。

## 系统架构

```
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── best.pt              # YOLO 模型文件
├── detection/           # 检测模块
│   ├── detector.py      # 二维码检测器
│   └── best.pt          # 备用模型文件
├── data_get/            # 数据获取模块
│   └── data_score.py    # 数据源处理
├── data_produce/        # 数据输出模块
│   └── data_keep.py     # 结果保存
├── data/                # 检测结果存储目录
└── pic_s/               # 本地图片目录
```

## 环境要求

### 系统要求
- Python 3.8+
- CUDA 支持（可选，用于 GPU 加速）

### 依赖包
```bash
pip install torch torchvision
pip install ultralytics
pip install opencv-python
pip install kafka-python
pip install numpy
pip install requests
```

## 配置说明

编辑 `config.py` 文件进行系统配置：

```python
# Kafka 配置
bootstrap_servers = "192.168.88.161:9092"  # Kafka 服务器地址
topic = "video_data0"                       # Kafka 主题名称
auto_offset_reset = 'latest'                # 消费者偏移量重置策略

# Socket 配置
host = "your_server_ip"                     # Socket 服务器 IP
port = 6666                                 # Socket 服务器端口
BUFFER_SIZE = 4096                          # 缓冲区大小

# 本地文件配置
data_set_path = "./pic_s"                   # 本地图片目录路径

# 性能配置
max_workers_kafka = 2                       # Kafka 处理线程数
max_workers_socket = 2                      # Socket 处理线程数
CACHE_EXPIRE_SECONDS = 300                  # 缓存过期时间（秒）
```

## 使用方法

### 1. 启动系统

```bash
python main.py
```

### 2. 选择数据输入方式

系统启动后会显示三种数据输入方式：

```
方式1 socket
方式2 kafka  
方式3 本地文件

选择数据接收方式（输入数值1-3）
```

#### 方式1：Socket 数据流
- 适用于实时视频流处理
- 需要配置 `host` 和 `port` 参数
- 支持二进制图像数据传输

#### 方式2：Kafka 消息队列
- 适用于分布式系统
- 需要配置 Kafka 服务器地址和主题
- 支持高并发数据处理

#### 方式3：本地图片文件
- 适用于批量图片处理
- 处理 `pic_s` 目录下的所有图片文件
- 支持常见图片格式（jpg、png 等）

## 功能特性

### 二维码检测
- 使用 YOLO 模型进行二维码区域检测
- 置信度阈值：0.3（可调整）
- 支持 GPU 加速（CUDA）

### 二维码解码
- 使用 OpenCV QRCodeDetector 进行解码
- 自动处理检测区域的 ROI 提取
- 支持多个二维码同时识别

### 数据处理
- 多线程并发处理
- 内存优化和垃圾回收
- 结果自动保存到文件

### HTTP 请求处理
- 自动识别 HTTP URL 类型的二维码
- 发送 GET 请求验证链接有效性

## 输出结果

### 控制台输出
系统会实时打印识别到的二维码内容：
```
['https://example.com/qr1', 'TEXT_CONTENT']
```

### 文件保存
检测结果会自动保存到 `data/` 目录下：
- 文件名格式：`{时间戳}.txt`
- 每30秒创建一个新文件
- 内容格式：每行包含一次检测的所有结果

## 性能优化

### GPU 加速
系统会自动检测 CUDA 可用性：
```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

### 内存管理
- 及时释放图像对象
- 强制垃圾回收
- 线程池管理并发任务

### 缓存机制
- 二维码结果缓存（300秒过期）
- 避免重复处理相同内容

## 故障排除

### 常见问题

1. **模型文件缺失**
   ```
   确保 best.pt 文件存在于项目根目录
   ```

2. **Kafka 连接失败**
   ```
   检查 bootstrap_servers 配置
   确认 Kafka 服务正常运行
   ```

3. **Socket 连接超时**
   ```
   检查 host 和 port 配置
   确认服务器端正常监听
   ```

4. **CUDA 内存不足**
   ```
   减少 max_workers 数量
   或使用 CPU 模式
   ```

### 日志查看
系统使用标准日志输出，可以查看详细的运行信息和错误提示。

## 扩展功能

### 自定义 Kafka 主题
```python
from data_get.data_score import topic_make
topic_make("your_topic_name")
```

### 数据过滤
```python
from data_produce.data_keep import data_filter
unique_data = data_filter()  # 获取去重后的数据
```

## 注意事项

1. 确保有足够的磁盘空间存储检测结果
2. 根据硬件配置调整线程数量
3. 定期清理 `data/` 目录下的历史文件
4. 监控内存使用情况，避免内存泄漏

## 技术支持

如遇到问题，请检查：
1. 依赖包是否正确安装
2. 配置文件是否正确设置
3. 输入数据格式是否符合要求
4. 系统资源是否充足
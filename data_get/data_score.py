from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from detection.detector import simple_detect_and_show
import socket
import struct
import cv2
import concurrent.futures
import logging
import os
import config
model = None
qr_detector = None
device = None
BUFFER_SIZE = 4096
TIMEOUT = 1.0  # 秒
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ImageReceiver')


def topic_make(bvid):
    # 配置Kafka连接
    admin_client = KafkaAdminClient(
        bootstrap_servers="192.168.88.161:9092,192.168.88.162:9092,192.168.88.163:9092",  # Kafka 服务地址
    )

    # 定义 Topic 的名称、分区数和副本数
    topic_name = bvid
    num_partitions = 3  # 分区数
    replication_factor = 2  # 副本数

    # 创建 NewTopic 对象
    new_topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )

    # 创建 topic
    try:
        admin_client.create_topics([new_topic])
        print(f"Topic '{topic_name}' created successfully")
    except Exception as e:
        print(f"Failed to create topic '{topic_name}': {e}")


def read_dataset(pic_path):
    pics = os.listdir(pic_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for pic in pics:
            pic_data = cv2.imread(pic_path+"/" + pic)
            executor.submit(simple_detect_and_show, pic=pic_data)


def read_kafka(topic, bootstrap_servers):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='latest'
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers_kafka) as executor:
        for data in consumer:
            executor.submit(simple_detect_and_show, pic=data.value)


def receive_image(sock):
    """从socket接收单张图像数据"""
    try:
        # 先接收4字节的图像大小（大端序）
        size_data = sock.recv(4)
        if not size_data:
            return None

        # 解析图像大小
        image_size = struct.unpack('>I', size_data)[0]

        # 接收完整的图像数据
        image_data = b''
        while len(image_data) < image_size:
            chunk = sock.recv(min(4096, image_size - len(image_data)))
            if not chunk:
                return None  # 连接中断
            image_data += chunk

        return image_data

    except Exception as e:
        logger.error(f"接收图像数据出错: {e}")
        return None


def process_server_stream(host, port):
    """连接到图像服务器并处理视频流"""
    # 创建socket连接
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        logger.info(f"已连接到服务器 {host}:{port}")

        # 使用线程池处理图像，避免阻塞接收
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers_socket) as executor:
            while True:
                image_data = receive_image(sock)
                if not image_data:
                    logger.warning("未接收到图像数据，连接可能已关闭")
                    break

                # 提交图像处理任务
                executor.submit(simple_detect_and_show,image_data)

    except ConnectionRefusedError:
        logger.error(f"无法连接到服务器 {host}:{port}，请检查服务器是否启动")
    except Exception as e:
        logger.error(f"处理过程出错: {e}")
    finally:
        sock.close()
        cv2.destroyAllWindows()
        logger.info("连接已关闭")

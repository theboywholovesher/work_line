import os
import time

start_time = time.time()
max_workers_kafka = 2
max_workers_socket = 2
bootstrap_servers = "192.168.88.161:9092"
auto_offset_reset = 'latest'
topic = "video_data0"
data_set_path = "./pic_s"
BUFFER_SIZE = 4096
host = os.getenv("HOST")
port = 6666
CACHE_EXPIRE_SECONDS = 300
max_poll_interval_ms = 30000

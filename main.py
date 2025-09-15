import config
import time
from data_get.data_score import process_server_stream, read_kafka, read_dataset


def main():
    print("方式1 socket" + '\n')
    print("方式2 kafka" + '\n')
    print("方式3 本地文件" + '\n')
    try:
        way = int(input("选择数据接收方式（输入数值1-3）"))
        if way == 1:
            read_kafka(config.topic, config.bootstrap_servers)
        elif way == 2:
            process_server_stream(config.host, config.port)
        elif way == 3:
            read_dataset(config.data_set_path)
        else:
            print('wrong input')
            main()
    except Exception as e:
        print(e)
        main()


if __name__ == '__main__':
    main()

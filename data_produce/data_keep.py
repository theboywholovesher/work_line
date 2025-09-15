import os


def data_keep(file_path, res):
    if os.path.exists(file_path):
        with open(file_path, 'a') as f:
            for data in res:
                f.write(str(data) + ',')
            f.write('\n')
    else:
        print("创建文件" + file_path)
        with open(file_path, "w") as f:
            pass
        with open(file_path, 'a') as f:
            for data in res:
                f.write(str(data) + ',')
            f.write('\n')


def data_filter():
    set_data = set()
    files = os.listdir('data')
    for file in files:
        with open('data/' + file, 'r') as f:
            data = f.readlines()
        for line in data:
            set_data.add(line)
    return set_data

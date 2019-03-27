import random

REAL_NORMAL_PATH = "./data/real_normal.txt"
REAL_SQL_PATH = "./data/real_sql.txt"
TRAIN_NORMAL_PATH = "./data/train_normal.txt"
TRAIN_SQL_PATH = "./data/train_sql.txt"

def ReadFileDatas():
    FileNamelist = []
    file = open(TRAIN_SQL_PATH, 'r+')
    for line in file:
        line = line.strip('\n')  # 删除每一行的\n
        FileNamelist.append(line)
    print('len ( FileNamelist ) = ', len(FileNamelist))
    file.close()
    return FileNamelist


def WriteDatasToFile(listInfo):
    fileInfo = ""
    for each_info in listInfo:
        fileInfo += each_info + '\n'
    with open(TRAIN_SQL_PATH, 'w') as f:
        f.write(fileInfo)



if __name__ == "__main__":
    listFileInfo = ReadFileDatas()
    # 打乱列表中的顺序
    random.shuffle(listFileInfo)
    WriteDatasToFile(listFileInfo)
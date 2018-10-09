import os
import re

path="F:/我的文件/视频制作/素材/我们"
file_walk = os.walk(path)
fileNum = 0
filesPathList = []
for root, dirs, files in file_walk:
    # print(root, end=',')
    # print(dirs, end=',')
    # print(files)
    for file in files:
        fileNum = fileNum + 1
        filePath = root + '/' + file
        # print(filePath)
        filesPathList.append(filePath)
        protion = os.path.splitext(filePath)
        # print(protion[0],protion[1])

        if protion[1].lower() == '.png':
            print("正在处理：" + filePath)
            newFilePath = protion[0] + '.JPG'
            os.rename(filePath, newFilePath)
# print(fileNum)
# print(filesPathList)
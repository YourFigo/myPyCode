import time

from controller import get_Total

from controller import get_Revenue
from public import common_mysql

def action_Run():
    print("准备爬虫............")
    common_mysql.crePltfmTb()
    get_Revenue.get_Revenue()
    print("数据爬取结束............")
    print("请稍后，5秒后进行数据汇总..........")
    time.sleep(5)
    print("正在准备数据汇总..................")
    get_Total.get_Total()
    print('10秒后自动关闭本窗口')
    time.sleep(10)

if __name__ == '__main__':
    action_Run()
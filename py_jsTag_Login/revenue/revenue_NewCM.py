import time
import traceback
import ctypes
from selenium import webdriver
from public import comm_logging
from public import common
from public import common_mysql

def test_NewCM():
    print("............NewCM................")
    flag = False
    for try_num in range(5):
        print("NewCM第" + str(try_num + 1) + "次尝试-----------")
        try:
            yesterday = common.getNowTime(-1)
            yyyy = yesterday[0:4]
            mm = yesterday[5:7]
            dd = yesterday[8:10]
            nowTime = common.getNowTime()
            yearNow = nowTime[0:4]
            monthNow = nowTime[5:7]
            dayNow = nowTime[8:10]

            # NewCM下载的文件名的前缀
            prefix = "Brand+Details_" + yearNow + monthNow + dayNow
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "NewCM")

            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
            # 修改默认下载地址
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path}
            chrome_options.add_experimental_option('prefs', prefs)

            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            loginURL = "https://peg.cmcm.com/login"
            dataURL = "https://peg.cmcm.com/frontReport/default"
            browser.get(loginURL)
            time.sleep(5)
            print("输入用户名密码---------------------------------")
            username, password = common_mysql.selectFromTb("NewCM")
            browser.find_element_by_name("username").send_keys(username)
            browser.find_element_by_name("password").send_keys(password)
            ctypes.windll.user32.MessageBoxA(0, u"点击确定后，请在15秒内输入验证码，不要点击登录!!!".encode('gb2312'),
                                             u' 信息'.encode('gb2312'), 0)
            print("请输入验证码，等待 15秒")
            for i in range(1,15):
                print("倒计时：",15-i)
                time.sleep(1)
            print("点击登录按钮------")
            browser.find_element_by_xpath('//button[@type="submit"]').click()
            time.sleep(5)
            print("跳转到数据页面---------------------------------")
            browser.get(dataURL)
            time.sleep(5)
            # 选择 AD unit
            print("选择 AD unit")
            browser.find_element_by_xpath('//button[text()="Dimension & Metric"]').click()
            browser.find_element_by_xpath('//span[text()="Ad Unit"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//button[text()="Submit"]').click()
            time.sleep(2)
            # 选择日期
            print("选择日期")
            browser.find_element_by_xpath('//button[@class="btn btn-default ng-binding"]').click()
            browser.find_element_by_xpath('//span[text()="Yesterday"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//button[text()="Submit"]').click()
            time.sleep(2)
            # 点击search
            print("# 点击search")
            browser.find_element_by_xpath('//input[@value="Search"]').click()
            time.sleep(5)
            print("点击下载")
            browser.find_element_by_xpath('//a[@class="btn btn-outline"]').click()
            time.sleep(5)

            # 扫描文件夹，获取 NewCM 的文件列表
            print("正在扫描下载的 csv 文件---------")
            fileList = common.scan_File(path, prefix)
            common.mkdir(path)
            # 读取下载的文件，删除无用数据并 重新保存
            print("正在剔除其他日期的数据 并另存为 excel ---------")
            common.turnToXls_ByPandas(path + fileList[-1], path + excelName, 'NewCM')
            common.remove_File(path, prefix)
            print("  excel保存成功，路径：" + path + "-----------")
            print("||||||||||||NewCM抓取完毕||||||||||||||")
            flag = True
        except:
            flag = False
            print(traceback.format_exc())
            errorInfo = traceback.format_exc()
            comm_logging.myLogger.write_logger(errorInfo)
            continue
        finally:
            browser.quit()
            if (flag or try_num == 5):
                break

if __name__ == '__main__':
    test_NewCM()
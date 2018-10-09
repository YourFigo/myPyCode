import time
import traceback
import ctypes
from selenium import webdriver
from public import comm_logging
from public import common
from public import common_mysql

def test_OpenX():
    print("............OpenX................")
    nowTime = common.getNowTime()
    yearNow = nowTime[0:4]
    monthNow = nowTime[5:7]
    dayNow = nowTime[8:10]
    # 路径只取nowTime的日期部分
    path = common.getDirPath(nowTime)
    # 用于删除 匹配的字符串
    prefix = "Workspace 1-" + monthNow + "-" + dayNow + "-" + yearNow
    excelName = common.getExcelName(nowTime, "openx")

    # 尝试5次，错误继续
    flag = False
    for try_num in range(2):
        print("OpenX第" + str(try_num + 1) + "次尝试-----------")
        try:
            print("打开浏览器")
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path}
            chrome_options.add_experimental_option('prefs', prefs)
            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            # 不最大化 某些按钮按不到会报错
            browser.maximize_window()
            time.sleep(2)
            logInURL = "https://sso.openx.com/login/login"
            dataURL = "http://mobimagic-ui.openx.net/app.html#/reports/pie"

            # 前天
            yesterday = common.getNowTime(-2)
            yyyy = yesterday[0:4]
            mm = yesterday[5:7]
            dd = yesterday[8:10]
            # print(yyyy,mm,dd)

            print("打开登录网址")
            browser.get(logInURL)
            time.sleep(5)

            # try 是正常不需要验证码登录，如果try里面失败了，相当于登录失败，需要验证码，然后就跑到了except中，按照需要验证码的方式进行登录。
            username, password = common_mysql.selectFromTb("OpenX")
            try:
                browser.find_element_by_id("email").send_keys(username)
                time.sleep(3)
                browser.find_element_by_id('password').send_keys(password)
                time.sleep(2)
                browser.find_element_by_id("submit").click()
                time.sleep(5)
                browser.find_element_by_xpath('//a[text()="http:// mobimagic-ui.openx.net/"]').click()
            except:
                print(traceback.format_exc())
                errorInfo = traceback.format_exc()
                comm_logging.myLogger.write_logger(errorInfo)
                #  不能再重新载入界面，重新载入后不会出现验证码，然后继续失败
                # browser.get(logInURL)
                time.sleep(2)
                browser.find_element_by_id("email").clear()
                browser.find_element_by_id("email").send_keys(username)
                time.sleep(3)
                browser.find_element_by_id('password').clear()
                browser.find_element_by_id('password').send_keys(password)
                ctypes.windll.user32.MessageBoxA(0, u"点击确定后，请在15秒内输入验证码，不要点击登录!!!".encode('gb2312'),
                                                 u' 信息'.encode('gb2312'), 0)
                print("请输入验证码，等待 15秒")
                for i in range(1, 15):
                    print("倒计时：", 15 - i)
                    time.sleep(1)
                browser.find_element_by_id("submit").click()

            print("模拟登录成功")
            print("打开数据网址")
            browser.get(dataURL)
            time.sleep(10)
            browser.find_element_by_xpath('//div[@class="date-range-filter__input"]').click()
            browser.find_element_by_xpath('//li[@class="date-range-filter__filter date-range-filter__filter--custom date-range-filter__filter__label"]').click()
            time.sleep(5)
            # startElements = browser.find_element_by_xpath('//input[@placeholder="Enter Date"]').send_keys(mm + "/" + dd + "/" + yyyy)
            # 各种方法试了一通，根本不行，下面可以list[0] 是开始日期，list[1]是结束日期
            print("开始选择日期和维度")
            inputElements = browser.find_elements_by_css_selector('[placeholder="Enter Date"]')
            inputElements[0].clear()
            inputElements[0].send_keys(mm + "/" + dd + "/" + yyyy)
            inputElements[1].clear()
            inputElements[1].send_keys(mm + "/" + dd + "/" + yyyy)
            browser.find_element_by_xpath('//div[@class="date-range-filter__custom-date-range-menu__buttons"]/div/button[2]').click()
            time.sleep(5)

            # 隐藏日期栏、折线图 不隐藏点不到下载按钮
            browser.find_element_by_xpath('//div[@class="reports-pie-data-collection-container__collapse-trigger"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//div[@class="reports-pie-collapse-toggle"]').click()
            time.sleep(1)
            # 点击下载 选择xlsx
            browser.find_element_by_xpath('//div[@class="reports-pie-chart-toolkit__export"]/ox-dropdown').click()
            time.sleep(1)
            # browser.find_element_by_xpath('//button[@class="ox-btn ox-btn--tertiary"]/div').click()
            browser.find_element_by_xpath('//span[text()="Excel "]').click()
            time.sleep(10)

            common.mkdir(path)
            # 扫描文件夹，获取 openx 的文件列表
            print("正在扫描下载的 xlsx 文件---------")
            fileList = common.scan_File(path, prefix)
            common.turnToXls_ByPandas(path + fileList[-1], path + excelName, 'openx')
            common.remove_File(path, prefix)
            print("  excel保存成功，路径：" + path + "-----------")
            print("||||||||||||OpenX抓取完毕||||||||||||||")
            flag = True
        except Exception as e:
            flag = False
            print(traceback.format_exc())
            errorInfo = traceback.format_exc()
            comm_logging.myLogger.write_logger(errorInfo)
            continue
        finally:
            browser.quit()
            if (flag or try_num == 4):
                break
if __name__ == '__main__':
    test_OpenX()
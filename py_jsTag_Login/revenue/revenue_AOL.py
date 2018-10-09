import time
import traceback
from datetime import datetime, timedelta

import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver

from public import comm_logging
from public import common
from public import common_mysql

def test_AOL():
    print("............AOL................")

    # 找到前天的日期
    def getDate():
        d = datetime.now() + timedelta(days=-2)
        d1 = d + timedelta(days=-1)
        if (int(d.strftime('%Y-%m-%d %H:%M:%S')[11:13]) <= 3):
            str_d = d1.strftime('%Y-%m-%d %H:%M:%S')
        else:
            str_d = d.strftime('%Y-%m-%d %H:%M:%S')
        yyyy1 = str_d[0:4]
        mmmm1 = str_d[5:7]
        dddd1 = str_d[8:10]
        logInURL1 = yyyy1 + "-" + mmmm1 + "-" + dddd1
        return logInURL1

    flag = False
    for try_num in range(5):
        print("AOL第" + str(try_num + 1) + "次尝试-----------")
        try:
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
            browser = webdriver.Chrome(chrome_options=chrome_options)
            loginURL = "https://onemobile.aol.com/"
            dataURL = "https://onemobile.aol.com/#/seller/39625/reports"
            browser.get(loginURL)
            print("点击登录---------------------------------")
            browser.find_element_by_id("native-login").click()
            time.sleep(15)
            username, password = common_mysql.selectFromTb("AOL")
            print("输入用户名---------------------------------")
            browser.find_element_by_xpath("//input[@placeholder='Username']").send_keys(username)
            time.sleep(2)
            print("确认用户名，点击下一步---------------------------------")
            browser.find_element_by_xpath("//input[@name='callback_2']").click()
            time.sleep(10)
            print("输入密码---------------------------------")
            browser.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
            time.sleep(2)
            print("点击登录按钮---------------------------------")
            browser.find_element_by_xpath("//input[@name='callback_2']").click()
            time.sleep(10)
            browser.get(dataURL)
            # 等待网页刷新
            t = 15
            while t > 0:
                print("网页加载中……倒计时" + str(t) + "秒后开始操作……")
                time.sleep(1)  # 等待10秒钟加载时间，网络好的话，5秒就够，但是10秒比较保守
                t = t - 1

            # 有一个概率性弹窗，有就点击关闭。
            try:
                print("点击X")
                browser.find_element_by_xpath("//a[@data-dismiss='modal']").click()
                print("关闭弹窗成功")
            except Exception as e:
                errorInfo = traceback.format_exc()
                print(errorInfo)
                comm_logging.myLogger.write_logger(errorInfo)

            print("选择开始日期%s---------------------------------" % getDate())
            browser.find_element_by_xpath("//input[@placeholder='YYYY-MM-DD'][1]").clear()
            time.sleep(3)
            browser.find_element_by_xpath("//input[@placeholder='YYYY-MM-DD'][1]").send_keys(getDate())
            browser.find_element_by_xpath("//input[@placeholder='YYYY-MM-DD'][2]").clear()
            time.sleep(3)
            print("选择结束日期---------------------------------")
            browser.find_element_by_xpath("//input[@placeholder='YYYY-MM-DD'][2]").send_keys(getDate())
            time.sleep(3)
            print("点击确认日期---------------------------------")
            # class='datepicker-apply-button pendo-id-datepicker-apply-button' 的 a 有3个 为何不用 index

            browser.find_element_by_xpath("//div[@class='datepicker-button-panel']/a").click()
            print("点击查询---------------------------------")
            browser.find_element_by_xpath("//button[@class='e-btn button-primary pendo-id-generate-report']").click()
            print("点击第一行数据---------------------------------")
            time.sleep(5)
            browser.find_element_by_xpath("//tbody[@aria-live='polite']/tr[1]").click()
            print("点击维度选择---------------------------------")
            time.sleep(2)
            browser.find_elements_by_xpath("//span[@class='title']")[2].click()
            time.sleep(1)
            print("点击tag维度---------------------------------")
            browser.find_element_by_xpath("//li[@data-sid='report-dimension-adTagId']").click()
            print("等待加载数据---------------------------------")
            time.sleep(10)
            dimensionsOfdata = ["Ad Tag", "Requests", "Served", "Delivered", "Fill Rate", "Clicks", "CTR", "Revenue",
                                "eCPM", "RPM"]
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('AOL')

            # 加表头
            col = 0
            for di in dimensionsOfdata:
                worksheet.write(0, col, dimensionsOfdata[col])
                col = col + 1

            print("开始爬数据")
            soup = BeautifulSoup(browser.page_source, "lxml")
            table = soup.find("table",
                              {"class": "table table-body table-nexage tablesorter tablesorter-default hasResizable"})
            # find() 直接返回结果 findAll()返回一个符合条件的所有tag的list
            tbody = table.find("tbody")
            trSum = tbody.findAll("tr")
            # trSum 为表格中的所有行的list
            row = 1
            for tr in trSum:
                # col 放在for 外面，会引起错误ValueError: column index (256) not an int in range(256)
                col = 0
                # tdSum 为一个tr的所有列的list
                tdSum = tr.findAll("td")
                # td 中存在空的<td></td>,在每个tr的最后一个td
                # 不取每一行的最后一个 td
                for td in tdSum:
                    if td.text.strip() != '':
                        if col == 0:
                            worksheet.write(row, col, td.text)
                        else:
                            worksheet.write(row, col, float(td.text.replace(",", "").replace("%", "").replace("$", "")))
                    col = col + 1
                row = row + 1

            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "AOL")
            common.mkdir(path)
            workbook.save(path + excelName)
            print("  excel保存成功，路径：" + path + "-----------")
            print("||||||||||||AOL抓取完毕||||||||||||||")
            flag = True
        except Exception as e:
            flag = False
            errorInfo = traceback.format_exc()
            print(errorInfo)
            comm_logging.myLogger.write_logger(errorInfo)
            continue
        finally:
            browser.quit()
            if (flag or try_num >= 4):
                break

if __name__ == '__main__':
    test_AOL()
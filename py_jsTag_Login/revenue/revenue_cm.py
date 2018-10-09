import time
import traceback
from datetime import datetime, timedelta

import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from public import comm_logging
from public import common
from public import common_mysql


def test_cm():
    print("............cm................")

    # 尝试5次，错误继续
    flag = False
    for try_num in range(5):
        print("cmcm第" + str(try_num + 1) + "次尝试-----------")
        try:
            print("打开浏览器")
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            logInURL = "http://console.cmcm.com"
            d = datetime.now() + timedelta(days=-1)
            d1 = d + timedelta(days=-1)
            if (int(d.strftime('%Y-%m-%d %H:%M:%S')[11:13]) <= 3):
                str_d1 = d1.strftime('%Y-%m-%d %H:%M:%S')
            else:
                str_d1 = d.strftime('%Y-%m-%d %H:%M:%S')
            yyyy1 = str_d1[0:4]
            mmmm1 = str_d1[5:7]
            dddd1 = str_d1[8:10]
            dataURL = "http://console.cmcm.com/report/placement?by=day&from=" + yyyy1 + "-" + mmmm1 + "-" + dddd1 + "&to=" + yyyy1 + "-" + mmmm1 + "-" + dddd1
            print("打开登录网址")
            browser.get(logInURL)
            time.sleep(2)
            print("模拟输入用户名密码中")
            username, password = common_mysql.selectFromTb("cm")
            browser.find_element_by_name('email').send_keys(username)
            browser.find_element_by_name('password').send_keys(password)
            browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/div/button').click()
            print("模拟登录成功")
            print("打开数据网址")
            browser.get(dataURL)
            time.sleep(20)
            dimensionsOfdata = ["datekey", "item_placement", "backfill", "wins", "impressions","requests", "fillrate", "winrate",
                                "clicks", "ctr", "ecpm", "money"]
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('cmcm')

            pageNum = browser.find_elements_by_xpath('//li[@data-page]').__len__()
            # 如果不进行此判断，会出现空表
            if pageNum >= 1:
                row = 1
                for page in range(pageNum):
                    print("-------读取第" + str(page + 1) + "页----------")
                    browser.find_element_by_xpath('//li[@data-page=' + str(page + 1) + ']').click()
                    soup = BeautifulSoup(browser.page_source, "lxml")
                    tbody = soup.find("table", {"class": "bordered highlighted scrolling-table"}).find("tbody")
                    trSum = tbody.findAll("tr")
                    for tr in trSum:
                        col = 0
                        tdSum = tr.findAll("td")
                        for td in tdSum:
                            if col == 0 or col == 1:
                                worksheet.write(row, col, td.text)
                            else:
                                worksheet.write(row, col, float(td.text.replace(",", "")))
                            col = col + 1
                        row = row + 1
                    time.sleep(2)
            else:
                continue

            # 处理表头
            col = 0
            for d in dimensionsOfdata:
                worksheet.write(0, col, dimensionsOfdata[col])
                col = col + 1

            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "cmcm")
            common.mkdir(path)
            workbook.save(path + excelName)
            print("  excel保存成功，路径：" + path + "-----------")
            print("||||||||||||cmcm抓取完毕||||||||||||||")
            flag = True
        except Exception as e:
            flag = False
            errorInfo = traceback.format_exc()
            comm_logging.myLogger.write_logger(errorInfo)
            continue
        finally:
            browser.quit()
            if (flag or try_num == 4):
                break
if __name__ == '__main__':
    test_cm()
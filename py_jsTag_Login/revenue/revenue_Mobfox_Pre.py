import time
import traceback

import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select

from public import comm_logging
from public import common


def test_Mobfox():
    print("............Mobfox................")
    flag = False
    for try_num in range(3):
        print("Mobfox第" + str(try_num + 1) + "次尝试-----------")
        try:
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')

            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            loginURL = "https://account.mobfox.com/www/cp/login.php"
            dataURL = "https://account.mobfox.com/www/cp/exchange_reporting.php"
            dataInnerURL = "https://account.mobfox.com/react/exchange-reporting?apikey=065f325c0728e09132ebf4cedfe10ed3&accountid=72511&hash=a305f8299d4f99e855a6a8aa26d3a221&env=prod&siteRoot=https://account.mobfox.com:443/&apiRoot=https://api-v3.mobfox.com"
            browser.get(loginURL)
            time.sleep(2)
            print("输入用户名密码---------------------------------")
            browser.find_element_by_id("email").send_keys("apiad@mobimagic.com")
            browser.find_element_by_id("password").send_keys("360Security2017")

            # 有一个概率性弹窗，有就点击关闭。
            try:
                print("点击accept")
                browser.find_element_by_xpath('//a[@class="optanon-allow-all"]').click()
                print("关闭弹窗成功")
            except Exception as e:
                errorInfo = traceback.format_exc()
                comm_logging.myLogger.write_logger(errorInfo)
                print(traceback.format_exc())
                print("无弹窗 或 弹窗关闭失败")

            time.sleep(5)
            browser.find_element_by_xpath(".//*[@type='submit']").click()
            # browser.find_element_by_class_name('btn btn-primary btn-myDsp ').click()
            print("跳转到数据页面---------------------------------")
            browser.get(dataURL)
            time.sleep(2)
            browser.get(dataInnerURL)
            print("自动选择数据维度内容---------------------------------")
            # s = browser.find_element_by_id("react-select-5--value")
            # Select(s).select_by_value("inventory_id")
            # s = browser.find_element_by_id("period")
            # Select(s).select_by_value("yesterday")
            # s = browser.find_element_by_id("timezone")
            # Select(s).select_by_value("Asia/Hong_Kong")
            # s = browser.find_element_by_id("timegroup")
            # Select(s).select_by_value("day")

            # browser.find_element_by_xpath('//span[@id="react-select-5--value"]/div[2]/input').send_keys("Daily")
            # browser.find_element_by_xpath('//span[@id="react-select-6--value-item"]').text = "react-select-6--value-item"
            # browser.find_element_by_class_name("text-center form-control").click()
            time.sleep(10)

            s = browser.find_element_by_xpath('//div[@id="content"]')
            html = browser.find_element_by_xpath('//html[@class=" supports cssfilters"]')
            browser.find_element_by_xpath('//li[text()="Yesterday"]').click()
            browser.find_element_by_xpath('//button[@title="Download Excel"]').click()

            time.sleep(2)
            browser.find_element_by_xpath('//button[@type="submit"]').click()

            dimensionsOfdata = ["col-day sorting_1", "col-inventory_id", "col-total_ad_source_opportunities",
                                "col-total_served", "col-total_impressions", "col-total_clicks", "col-ctr",
                                "col-fillrate",
                                "col-total_earnings", "col-ecpm"]
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Mobfox')
            print("开始爬数据")
            soup = BeautifulSoup(browser.page_source, "lxml")
            tbody = soup.find("div", {"class": "dataTables_scrollBody"}).find("tbody")
            trSum = tbody.findAll("tr")

            # 加表头
            col = 0
            for di in dimensionsOfdata:
                worksheet.write(0, col, dimensionsOfdata[col])
                col = col + 1

            row = 1
            for tr in trSum:
                # col 放在for 外面，会引起错误ValueError: column index (256) not an int in range(256)
                col = 0
                # tdSum 为一个tr的所有列的list
                tdSum = tr.findAll("td")
                for td in tdSum:
                    try:
                        worksheet.write(row, col,
                                        float(td.text.strip().replace(",", "").replace("%", "").replace("$", "")))
                    except ValueError:
                        worksheet.write(row, col, td.text.strip())
                    col = col + 1
                row = row + 1

            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "Mobfox")
            common.mkdir(path)
            workbook.save(path + excelName)
            print("  excel保存成功，路径：" + path + "-----------")
            print("||||||||||||Mobfox抓取完毕||||||||||||||")
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
    test_Mobfox()



'''
for dimensions in dimensionsOfdata:
    print("开始爬"+dimensions+"数据")
    liList = soup.findAll("td", dimensions)
    worksheet.write(0, j, dimensions)
    i=1
    for li in liList:
        try:
            if dimensions=="col-day sorting_1" or dimensions=="col-inventory_id":
                worksheet.write(i, j, li.text[33:][:-28])
            elif dimensions=="col-ctr" or dimensions=="col-fillrate":
                worksheet.write(i, j, float(li.text[33:][:-28].replace("%","")))
            elif dimensions=="col-total_earnings" or dimensions=="col-ecpm":
                worksheet.write(i, j, float(li.text[33:][:-28].replace("$", "")))
            else:
                worksheet.write(i, j, float(li.text[33:][:-28].replace(",", "")))
        except ValueError:
            worksheet.write(i, j, li.text)
        i = i + 1
    j = j+1

print("保存为excel")
workbook.save('D:/DailyReport_Mobfox.xls')
browser.quit()
print("||||||||||||||||||||||Mobfox抓取完毕|||||||||||||||||||||||||||||||||||")
'''
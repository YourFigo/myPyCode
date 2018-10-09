import time
import traceback

import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from public import comm_logging
from public import common
from public import common_mysql

def test_Tappx():
    print("............Tappx................")
    flag = False
    for try_num in range(3):
        print("Tappx第" + str(try_num + 1) + "次尝试-----------")
        try:
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')

            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            loginURL = "https://www.tappx.com/en/admin/login/"
            dataURL = "https://www.tappx.com/en/admin/monetize/"
            browser.get(loginURL)

            print("输入用户名密码---------------------------------")
            username, password = common_mysql.selectFromTb("Tappx")
            browser.find_element_by_id("username").send_keys(username)
            browser.find_element_by_id("password").send_keys(password)
            browser.find_element_by_xpath("//button[@type='submit']").click()
            print("跳转到数据页面---------------------------------")
            browser.get(dataURL)
            print("自动选择数据维度内容---------------------------------")
            time.sleep(5)
            print("选择货币形式为美元---------------------------------")
            browser.find_element_by_xpath("//div[@id='currency-selector']/a[2]").click()
            time.sleep(1)
            print("取消APP维度---------------------------------")
            browser.find_element_by_xpath("//i[@class='tappxicon tappxicon-close']").click()
            time.sleep(1)
            print("展开维度---------------------------------")
            browser.find_element_by_xpath("//button[@class='btn-block btn btn-default dropdown-toggle']").click()
            time.sleep(1)
            print("点击显示下拉维度---------------------------------")
            browser.find_element_by_xpath("//a[@class='dropdown-opener']").click()
            time.sleep(1)
            print("点击day维度---------------------------------")
            browser.find_element_by_xpath("//li[@class='model-g_time_day no-image']").click()
            time.sleep(1)
            print("展开维度---------------------------------")
            browser.find_element_by_xpath("//button[@class='btn-block btn btn-default dropdown-toggle']").click()
            time.sleep(1)
            print("点击app维度---------------------------------")
            browser.find_element_by_xpath("//ul[@class='list-unstyled']/li[5]").click()
            time.sleep(1)
            print("展开维度---------------------------------")
            browser.find_element_by_xpath("//button[@class='btn-block btn btn-default dropdown-toggle']").click()
            time.sleep(1)
            print("点击format维度---------------------------------")
            browser.find_element_by_xpath("//ul[@class='list-unstyled']/li[2]").click()
            time.sleep(1)
            print("展开维度---------------------------------")
            browser.find_element_by_xpath("//button[@class='btn btn-default btn-plus dropdown-toggle']").click()
            time.sleep(1)
            print("点击时间下拉维度---------------------------------")
            browser.find_element_by_xpath("//ul[@id='default-options']/li[4]").click()
            time.sleep(1)
            print("点击昨天维度---------------------------------")
            browser.find_element_by_xpath("//ul[@id='default-options']/li[4]/ul/li[2]").click()
            time.sleep(3)
            dimensionsOfdata = ["Date", "App", "Format", "Requests", "Deliveries", "Impressions", "Clicks", "CPM",
                                "CTR","Fill Rate", "Render Rate", "Benefits"]
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Tappx')
            soup = BeautifulSoup(browser.page_source, "lxml")
            print("开始爬数据")
            tbody = soup.find("tbody", {"id": "data-raw-table"})
            trSum = tbody.findAll("tr")
            row = 1
            for tr in trSum:
                col = 0
                tdSum = tr.findAll("td")
                for td in tdSum:
                    # print(td.text)
                    try:
                        if col >= 3:
                            worksheet.write(row, col, float(td.text.replace(",", "").replace("%", "").replace("$", "")))
                        elif col == 1:
                            x = td.text.replace("\n","").strip()
                            worksheet.write(row, col, td.text.replace("\n","").strip())
                        else:
                            worksheet.write(row, col, float(td.text))
                    except ValueError:
                        worksheet.write(row, col, td.text)
                    col = col + 1
                row = row + 1
            # 加表头
            col = 0
            for di in dimensionsOfdata:
                worksheet.write(0, col, dimensionsOfdata[col])
                col = col + 1

            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "Tappx")
            common.mkdir(path)
            workbook.save(path + excelName)
            print("  excel保存成功，路径：" + path + "-----------")
            browser.quit()
            print("||||||||||||Tappx抓取完毕||||||||||||||")
            flag = True
        except:
            flag = False
            print(traceback.format_exc())
            errorInfo = traceback.format_exc()
            comm_logging.myLogger.write_logger(errorInfo)
            continue
        finally:
            browser.quit()
            if (flag or try_num == 3):
                break

if __name__ == '__main__':
    test_Tappx()
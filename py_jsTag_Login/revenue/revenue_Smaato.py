import time
import traceback

import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from public import comm_logging
from public import common
from public import common_mysql

def test_Smaato():
    print("............Smaato................")

    # 尝试5次，错误继续
    flag = False
    for try_num in range(5):
        print("Smaato第" + str(try_num + 1) + "次尝试-----------")
        try:
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            loginURL = "https://spx.smaato.com/publisherportal/pages/login.xhtml"
            username, password = common_mysql.selectFromTb("Smaato")
            dataURL = "https://spx.smaato.com/publisherportal/pages/reporting/reporting.xhtml"
            print("进入登陆页---------------------------------")
            browser.get(loginURL)
            print("  输入用户名密码-------------------------")
            browser.find_element_by_id("j_username").send_keys(username)
            browser.find_element_by_id("j_password").send_keys(password)
            browser.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(5)
            print("跳转到数据页面---------------------------------")
            browser.get(dataURL)
            time.sleep(10)
            print("  点击日历表------------------")
            browser.find_element_by_xpath("//span[@id='reporting:popup']").click()
            print("  选择yesterday----------------")
            browser.find_element_by_xpath("//div[@class='drp_shortcuts-block1']/span[2]").click()
            print("  点击update----------------")
            browser.find_element_by_xpath("//input[@class='apply-btn']").click()
            time.sleep(2)
            print("  点击display by：----------------")
            browser.find_element_by_xpath("//label[@id='reporting:displayByMenu_label']").click()
            print("  点击Adspace----------------")
            # data-label 是 li 的数据部分
            browser.find_element_by_xpath("//li[@data-label='Adspace']").click()
            # 需要一个刷新延时
            time.sleep(5)
            # 表头信息列表
            dimensionsOfdata = ["Adspace", "Adspace ID", "Net Revenue", "Gross Revenue", "Ad Requests", "Served Ads",
                                "Fillrate", "Impressions", "Viewrate", "Net eCPM", "Gross eCPM", "Clicks"]
            # 新建表格对象
            workbook = xlwt.Workbook(encoding='utf-8')
            # 新建sheet对象
            worksheet = workbook.add_sheet('Smaato')

            soup = BeautifulSoup(browser.page_source, "lxml")
            print("开始爬数据------------------")
            table = soup.find("tbody", {"id": "reporting:reportingSummaryTable_data"})
            trSum = table.findAll("tr")
            time.sleep(2)
            # 处理数据部分
            # 第一行为表头，从第二行开始填充数据
            row = 1
            # 对所有行进行循环
            for tr in trSum:
                col = 0
                tdSum = tr.findAll("td")
                # 对每一行的所有列进行循环
                for td in tdSum:
                    try:
                        if col == 2 or col == 3 or col == 9 or col == 10:
                            worksheet.write(row, col, float(td.text.replace("$", "").replace(",", "")))
                        elif col == 4 or col == 5 or col == 7 or col == 11:
                            worksheet.write(row, col, float(td.text.replace(",", "")))
                        elif col == 6 or col == 8:
                            worksheet.write(row, col, float(td.text.replace("%", "")))
                        elif col == 1:
                            worksheet.write(row, col, float(td.text))
                        else:
                            worksheet.write(row, col, td.text)
                    except Exception as e:
                        print(traceback.format_exc())
                        # continue

                    col = col + 1
                row = row + 1
            # 处理表头
            col = 0
            for d in dimensionsOfdata:
                worksheet.write(0, col, dimensionsOfdata[col])
                col = col + 1

            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "Smaato")
            common.mkdir(path)
            workbook.save(path + excelName)
            print("  excel保存成功，路径：" + path + "-----------")

            print("||||||||||||Smaato抓取完毕||||||||||||||")

            flag = True
            # read_workbook = xlrd.open_workbook(path + excelName)
            # read_sheetName = read_workbook.sheet_names()[0]
            # read_sheet = read_workbook.sheet_by_name(read_sheetName)
            # read_numRow, read_numCol = read_sheet.nrows, read_sheet.ncols
            # if read_sheet.cell(read_numRow - 1,1) is '':
            #     flag = False

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
     test_Smaato()
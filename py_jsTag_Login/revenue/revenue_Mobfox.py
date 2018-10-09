import time
import traceback
import json
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver

from public import comm_logging
from public import common
from public import common_mysql

def test_Mobfox():
    print("............Mobfox................")
    flag = False
    for try_num in range(3):
        print("Mobfox第" + str(try_num + 1) + "次尝试-----------")
        yesterday = common.getNowTime(delta= -1 ,type= "-")[0:10]
        try:
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')

            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)
            loginURL = "https://account.mobfox.com/www/cp/login.php"
            dataURL = "https://account.mobfox.com/www/cp/exchange_reporting.php"
            dataInnerURL = "https://account.mobfox.com/react/exchange-reporting?apikey=065f325c0728e09132ebf4cedfe10ed3&accountid=72511&hash=a305f8299d4f99e855a6a8aa26d3a221&env=prod&siteRoot=https://account.mobfox.com:443/&apiRoot=https://api-v3.mobfox.com"
            dataLoadURL = "https://api-v3.mobfox.com/publisher/report?apikey=065f325c0728e09132ebf4cedfe10ed3&from=" + yesterday + "&to=" + yesterday + "&tz=Asia%2FHong_Kong&group=inventory_id&timegroup=day&totals=total_impressions%2Ctotal_served%2Ctotal_ad_source_opportunities%2Ctotal_clicks%2Ctotal_earnings&f%3Aad_source=exchange&o%3Ainclude_entities=true"
            browser.get(loginURL)
            time.sleep(2)
            print("输入用户名密码---------------------------------")
            username, password = common_mysql.selectFromTb("Mobfox")
            browser.find_element_by_id("email").send_keys(username)
            browser.find_element_by_id("password").send_keys(password)

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
            browser.get(dataLoadURL)
            time.sleep(2)

            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Mobfox')
            print("开始爬数据")

            soup = BeautifulSoup(browser.page_source, "lxml")
            dataSoup = soup.find("pre").text
            #网页里提供的数据为json数据，需要json进行解析
            dataJson = json.loads(dataSoup)
            dataCol = dataJson["columns"]
            # dataResults 的大小为 rowNum * 7
            dataResults = dataJson["results"]
            rowNum = dataResults.__len__()
            dimensions = ["day","inventory","source_opportunities","total_served","total_impressions","total_clicks","ctr","fillrate","total_earnings","ecpm"]
            for col in range(10):
                worksheet.write(0, col, dimensions[col])
            try:
                for row in range(0,rowNum):

                    for col in range(10):
                        if col == 0 or col == 3 or col == 5:
                            worksheet.write(row + 1, col, dataResults[row][col])
                        elif col == 1:
                            InventoryID = str(dataResults[row][col])
                            InventoryName = dataJson["entities"]["inventory_id"][InventoryID]["name"]
                            Inventory = InventoryName + " (" + InventoryID + ")"
                            worksheet.write(row + 1,col,Inventory)
                        elif col == 2:
                            worksheet.write(row + 1, col, dataResults[row][4])
                        elif col == 4:
                            worksheet.write(row + 1, col, dataResults[row][2])
                        elif col == 6:
                            if dataResults[row][4] != 0:
                                ctr = dataResults[row][5] / dataResults[row][4] * 100
                            else:
                                ctr = "#DIV/!"
                            worksheet.write(row + 1, col, ctr)
                        elif col == 7:
                            if dataResults[row][2] != 0:
                                fillRate = dataResults[row][4] / dataResults[row][2] * 100
                            else:
                                fillRate = "#DIV/!"
                            worksheet.write(row + 1, col, fillRate)
                        elif col == 8:
                            worksheet.write(row + 1,col,dataResults[row][6])
                        elif col == 9:
                            if dataResults[row][4] != 0:
                                ecpm = dataResults[row][6] / dataResults[row][4] * 100
                            else:
                                ecpm = "#DIV/!"
                            worksheet.write(row + 1, col, ecpm)
            except Exception:
                print(traceback.format_exc())
                errorInfo = traceback.format_exc()
                comm_logging.myLogger.write_logger(errorInfo)
                continue

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
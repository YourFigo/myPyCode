import time
import traceback

from selenium import webdriver
from selenium.webdriver.support.select import Select
from public import comm_logging
from public import common
from public import common_mysql

def test_Pubnative():
    print("............Pubnative................")
    flag = False
    for try_num in range(3):
        print("Pubnative第" + str(try_num + 1) + "次尝试-----------")
        try:
            yesterday = common.getNowTime(-1)
            yyyy = yesterday[0:4]
            mm = yesterday[5:7]
            dd = yesterday[8:10]
            # downloadFile = "C:/Users/Administrator/Downloads" + "/" + "Publisher App_" + dd + "." + mm + "." + yyyy + ".csv"
            # 下载的文件名
            downloadFile = "Publisher App_" + dd + "." + mm + "." + yyyy + "-" + dd + "." + mm + "." + yyyy + ".csv"
            # 用于删除 匹配的字符串
            prefix = "Publisher App_" + dd + "." + mm + "." + yyyy + "-" + dd + "." + mm + "." + yyyy
            # print(downloadFile)
            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            # print(path)
            excelName = common.getExcelName(nowTime, "Pubnative")

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
            loginURL = "https://dashboard.pubnative.net"
            dataURL = "https://dashboard.pubnative.net/partner/#!/api"
            browser.get(loginURL)
            time.sleep(5)
            print("输入用户名密码---------------------------------")
            from public import common_mysql
            username, password = common_mysql.selectFromTb("Pubnative")
            browser.find_element_by_id("email").send_keys(username)
            browser.find_element_by_id("password").send_keys(password)
            # browser.find_element_by_xpath('//form[@action="/sessions"]/div[0]/div/input').send_keys("jstagad@mobimagic.com")
            # browser.find_element_by_xpath('//form[@action="/sessions"]/div[1]/div/input').send_keys("360Security2017666")
            time.sleep(2)
            browser.find_element_by_xpath('//input[@value="LOGIN"]').click()
            print("跳转到数据页面---------------------------------")
            browser.get(dataURL)
            time.sleep(15)
            print("自动选择数据维度内容---------------------------------")
            browser.find_element_by_xpath('//div[@class="col-md-7"]').click()
            browser.find_element_by_xpath('//div[@class="daterange"]/ul/li[2]').click()
            s = browser.find_element_by_tag_name("select")
            # Select(s).select_by_value("0")
            Select(s).select_by_index(12)
            browser.find_element_by_xpath('//button[@class="btn btn-secondary ng-star-inserted"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//div[@class="reports-filters row"]/div[3]').click()
            print("准备下载...")
            time.sleep(2)

            dimensionsOfdata = ["Publisher App", "Impressions",
                                "Requests", "Fill Rate", "eCPM", "Clicks", "CTR",
                                "Conversions", "Payout"]
            # workbook = xlwt.Workbook(encoding='utf-8')
            # worksheet = workbook.add_sheet('Pubnative')
            # print("开始爬数据")
            # soup = BeautifulSoup(browser.page_source, "lxml")
            # tbody = soup.find("tbody")
            # time.sleep(2)
            # trSum = tbody.findAll("tr")
            # time.sleep(2)
            # # 加表头
            # col = 0
            # for di in dimensionsOfdata:
            #     worksheet.write(0, col, dimensionsOfdata[col])
            #     col = col + 1
            #
            # row = 1
            # for tr in trSum[3:]:
            #     # col 放在for 外面，会引起错误ValueError: column index (256) not an int in range(256)
            #     col = 0
            #     # tdSum 为一个tr的所有列的list
            #     tdSum = tr.findAll("td")
            #     for td in tdSum:
            #         worksheet.write(row, col, td.text.strip())
            #         col = col + 1
            #     row = row + 1
            print("点击下载")
            browser.find_element_by_xpath('//div[@class="col-md order-disabled optional-buttons"]/a[2]').click()
            time.sleep(2)

            common.mkdir(path)
            # workbook.save(path + excelName)
            print("读取 csv 另存为 excel")
            common.turnToXls_ByPandas(path + downloadFile, path + excelName, 'Pubnative')
            print("删除多余的 csv")
            common.remove_File(path, prefix)
            print("  excel保存成功，路径：" + path + "-----------")
            print("||||||||||||Pubnative抓取完毕||||||||||||||")
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
    test_Pubnative()
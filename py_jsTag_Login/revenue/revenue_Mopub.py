import time
from datetime import datetime, timedelta
import traceback
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver

from public import comm_logging
from public import common
from public import common_mysql

def test_Mopub():
    print("............Mopub................")
    flag = False
    for try_num in range(3):
        print("Mopub第" + str(try_num + 1) + "次尝试-----------")
        try:
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')

            # 启动浏览器，获取网页源代码
            browser = webdriver.Chrome(chrome_options=chrome_options)

            def getURL(str):
                d = datetime.now() + timedelta(days=-1)
                d1 = d + timedelta(days=-1)
                d2 = d + timedelta(days=-2)
                if (int(d.strftime('%Y-%m-%d %H:%M:%S')[11:13]) <= 3):
                    str_d1 = d1.strftime('%Y-%m-%d %H:%M:%S')
                    str_d2 = d2.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    str_d1 = d.strftime('%Y-%m-%d %H:%M:%S')
                    str_d2 = d1.strftime('%Y-%m-%d %H:%M:%S')
                yyyy1 = str_d1[0:4]
                mmmm1 = str_d1[5:7]
                dddd1 = str_d1[8:10]
                yyyy2 = str_d2[0:4]
                mmmm2 = str_d2[5:7]
                dddd2 = str_d2[8:10]
                # 这个MopubBanner的link
                logInURL1 = "https://dash.metamarkets.com/mopub-360_mobile_security/explore#ed=app_name&fs.0.k=ad_size&fs.0.v.0=300x250&fs.0.v.1=320x50&fs.1.k=timestamp&fs.1.t.0.tr.end=" + yyyy1 + "-" + mmmm1 + "-" + dddd1 + "T16&fs.1.t.0.tr.start=" + yyyy2 + "-" + mmmm2 + "-" + dddd2 + "T16&gm.0=rev_adj&gm.1=auctions&gm.2=win_rate_v2&gm.3=cleared_done&gm.4=ctr&gm.5=ecpm&gm.6=uniques&od.0=ad_size&od.1=adgroup_priority&od.2=adunit_name&od.3=app_version&od.4=app_name&od.5=country&od.6=creative_id&od.7=pub_id&sbd=0&sortBy=rev_adj&sortDim=0&sortDir=descending&td=time_day&tm.0=rev_adj&tm.1=auctions&tm.2=win_rate_v2&tm.3=cleared_done&tm.4=ctr&tm.5=ecpm&tm.6=uniques&tz=Asia~2fShanghai&zz=4"
                # 这个Mopub native的link
                logInURL2 = "https://dash.metamarkets.com/mopub-360_mobile_security/explore#ed=app_name&fs.0.k=ad_size&fs.0.v.0=0x0&fs.0.v.1=320x480&fs.1.k=timestamp&fs.1.t.0.tr.end=" + yyyy1 + "-" + mmmm1 + "-" + dddd1 + "T16&fs.1.t.0.tr.start=" + yyyy2 + "-" + mmmm2 + "-" + dddd2 + "T16&gm.0=rev_adj&gm.1=auctions&gm.2=win_rate_v2&gm.3=cleared_done&gm.4=ctr&gm.5=ecpm&gm.6=uniques&od.0=ad_size&od.1=adgroup_priority&od.2=adunit_name&od.3=app_version&od.4=app_name&od.5=country&od.6=creative_id&od.7=pub_id&sbd=0&sortBy=rev_adj&sortDim=0&sortDir=descending&td=time_day&tm.0=rev_adj&tm.1=auctions&tm.2=win_rate_v2&tm.3=cleared_done&tm.4=ctr&tm.5=ecpm&tm.6=uniques&tz=Asia~2fShanghai&zz=4"
                if str == "Mopub_Banner":
                    logInURL = logInURL1
                elif str == "Mopub_Native":
                    logInURL = logInURL2
                # 传什么参数，那么就返回哪个链接
                return logInURL

            # dimensionsOfdata中元素 = 数据div中的colid 值
            dimensionsOfdata = ["auctions", "cleared_done", "uniques", "rev_adj", "win_rate_v2", "ctr", "ecpm"]
            dataRes = ["Mopub_Banner", "Mopub_Native"]

            workbook = xlwt.Workbook(encoding='utf-8')

            for resouce in dataRes:
                worksheet1 = workbook.add_sheet(resouce)
                browser.get(getURL(resouce))
                print("现在开始抓取" + resouce + "的数据。" + "\n链接:" + getURL(resouce))
                # 因为先运行Mopub_Banner，因此只要判断第一次，第一次登陆即可
                if resouce == "Mopub_Banner":
                    username, password = common_mysql.selectFromTb("Mopub")
                    browser.find_element_by_id("form-id1").send_keys(username)
                    browser.find_element_by_id("form-id2").send_keys(password)
                    browser.find_element_by_xpath("//button[@class='primary login']").click()

                time.sleep(10)

                soup = BeautifulSoup(browser.page_source, "lxml")
                appNameList = soup.findAll("div", colid="app_name")

                # 插入表头
                m = 0
                for appName in appNameList:
                    # 虽然网页的表头 colid="app_name" ，但是，div的下一层没有span，而数据部分的div下一层有span，因此appname的第一行空着
                    worksheet1.write(m, 0, appName.span.text)
                    m = m + 1

                # 将数据按列插入excel中
                j = 1
                for col in dimensionsOfdata:
                    worksheet1.write(0, j, col)
                    colData = soup.findAll("div", colid=col)
                    i = 1
                    for row in colData[1:]:
                        try:
                            worksheet1.write(i, j, float(row.span["title"]))
                            i = i + 1
                        except BaseException as err:
                            print("Exception:", err)
                    j = j + 1
                print(resouce + " 抓取完成----------------")

            nowTime = common.getNowTime()
            # 路径只取nowTime的日期部分
            path = common.getDirPath(nowTime)
            excelName = common.getExcelName(nowTime, "Mopub")
            common.mkdir(path)
            workbook.save(path + excelName)
            print("  excel保存成功，路径：" + path + "-----------")
            browser.quit()
            print("||||||||||||Mopub抓取完毕||||||||||||||")
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
    test_Mopub()

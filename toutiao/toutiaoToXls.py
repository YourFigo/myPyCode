from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime,timedelta
import xlwt
import re
import commAPI

startTime = datetime.now()
# 创建一个模拟滚动条滚动到页面底部函数
def scroll(driv):
    driv.execute_script("""   
    (function () {   
        var y = document.body.scrollTop;   
        var step = 100;   
        window.scroll(0, y);   


        function f() {   
            if (y < document.body.scrollHeight) {   
                y += step;   
                window.scroll(0, y);   
                setTimeout(f, 50);   
            }  
            else {   
                window.scroll(0, y);   
                document.title += "scroll-done";   
            }   
        }   


        setTimeout(f, 1000);   
    })();   
    """)

print("请输入滚动次数，输入完成后按Enter键开始：")
scrollNum = int(input())
webUrl = "https://www.toutiao.com/"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options = chrome_options)
browser.get(webUrl)
time.sleep(3)

print("开始模拟鼠标拉到文章底部")
b=0
c=0
while b < scrollNum: #设置循环，可替换这里值来选择你要滚动的次数
    scroll(browser) #滚动一次
    b = b + 1
    if (b % 10 == 0) or (b == 1):
        print('正在拉动第 {} 次...'.format(b))
    if c < 10:
        c = c + 1
    time.sleep(c) #休息c秒的时间

# 创建excel
workbook = xlwt.Workbook(encoding='utf-8')
worksheet1 = workbook.add_sheet("今日头条")
title = ['序号','标题','详情网址','新闻来源','评论数','发布日期']
for i in range(6):
    worksheet1.write(0, i, title[i])

#开始解析
soup = BeautifulSoup(browser.page_source,'lxml')
i = 0
for liOut in soup.find_all('div',ga_event="article_item_click"):
    li = liOut.find('div',class_="single-mode-rbox-inner")
    if li != None:
        i = i + 1
        # 获得新闻的标题div 和 相关信息div
        NewsDiv = li.find('div', class_="title-box")
        NewsInfoDiv = li.find('div', class_="bui-left footer-bar-left")

        # 从标题div 取相关内容
        NewsTitle = NewsDiv.find('a', class_="link").text
        NewsUrl = 'www.toutiao.com' + NewsDiv.a['href']

        # 从相关信息div 取相关内容
        # NewsTag = NewsInfoDiv.find('a', ga_event="article_tag_click").text
        # 只取字符串中的数字
        patt1 = r"\d+\.?\d*"
        patt1 = re.compile(patt1)
        # 排除字符串中的字母、数字、符号
        patt2 = "[A-Za-z0-9\!\%\[\]\,\。]"
        NewsSource = NewsInfoDiv.find('a', ga_event="article_name_click").text.replace("⋅","").replace(" ","").replace(u"\xa0","")
        NewsCommentNum = NewsInfoDiv.find('a', ga_event="article_comment_click").text.replace("⋅","").replace(" ","")
        # commentNum = int(re.findall(patt1, NewsCommentNum))
        commentNum = re.search(patt1, NewsCommentNum)
        if commentNum:
            commentNum = int(re.search(patt1, NewsCommentNum).group(0))
        else:
            commentNum = 0
        NewsCommentUrl = NewsInfoDiv.find('a', ga_event="article_comment_click").get('href')
        NewsTime = NewsInfoDiv.find('span', class_="footer-bar-action").text.replace("⋅","").replace(" ","").replace(u"\xa0","")
        if NewsTime != "刚刚":
            timeNum = int(re.search(patt1, NewsTime).group(0))
        else:
            timeNum = 0
        timeUnitType = re.sub(patt2, "", NewsTime)
        if timeUnitType == "天前":
            NewsDate =(datetime.now() + timedelta(days= -timeNum)).strftime('%Y%m%d')
        else:
            NewsDate = datetime.now().strftime('%Y%m%d')
        one = (None,NewsTitle,NewsUrl,NewsSource,commentNum,NewsDate)
        for j in range(6):
            if j == 0:
                worksheet1.write(i, j, i)
            else:
                worksheet1.write(i, j, one[j])

        print("第 {} 个 :".format(i))
        print("标题 ：",NewsTitle)
        print("详情URL ：",NewsUrl)
        print("新闻来源 ：",NewsSource)
        print("评论数 ：",commentNum)
        print("日期 ：",NewsDate)
        print('-------------------------------------------')

endTime = datetime.now()
timeDuration = (endTime - startTime).seconds
worksheet1.write(0, 7, "耗时: {} 秒".format(timeDuration))
workbook.save("C:/Users/Administrator/Desktop/toutiao" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xls")
print("抓完咯")
print("关闭浏览器")
print('耗时 {} 秒'.format(timeDuration))
browser.quit()

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime, timedelta
import re
import my_mysql
import commAPI

startTime = datetime.now()
print("开始时间：",startTime)

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
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get(webUrl)
time.sleep(3)

print("开始模拟鼠标拉到文章底部")
b = 0
c = 0
while b < scrollNum:  # 设置循环，可替换这里值来选择你要滚动的次数
    scroll(browser)  # 滚动一次
    b = b + 1
    if (b % 10 == 0) or (b == 1):
        print('正在拉动第 {} 次...'.format(b))
    if c < 10:
        c = c + 1
    time.sleep(c)  # 休息c秒的时间

# 只取字符串中的数字
patt1 = r"\d+\.?\d*"
patt1 = re.compile(patt1)
# 排除字符串中的字母、数字、符号
patt2 = "[A-Za-z0-9\!\%\[\]\,\。]"
print('-------------------------------------------------------------------')
# 开始解析
soup = BeautifulSoup(browser.page_source, 'lxml')
i = 0
# article_item_click 可排除广告信息，但里面混有 没有评论 和 没有专题的文章
for liOut in soup.find_all('div', ga_event="article_item_click"):
    li = liOut.find('div', class_="single-mode-rbox-inner")
    if li != None:
        # 排除没有专题 和 没有评论 的信息
        tag = li.find('a', ga_event="article_tag_click")
        comment = li.find('a', ga_event="article_comment_click")
        if tag != None and comment != None:
            i = i + 1
            # 获得新闻的标题div 和 相关信息div
            NewsDiv = li.find('div', class_="title-box")
            NewsInfoDiv = li.find('div', class_="bui-left footer-bar-left")

            # 从标题div 取相关内容
            NewsTitle = NewsDiv.find('a', class_="link").text
            NewsUrl = 'www.toutiao.com' + NewsDiv.a['href']
            NewsID = re.search(patt1, NewsDiv.a['href']).group(0)

            # 从相关信息div 取相关内容
            # NewsTag = NewsInfoDiv.find('a', ga_event="article_tag_click").text
            NewsSource = NewsInfoDiv.find('a', ga_event="article_name_click").text.replace("⋅", "").replace(" ","").replace(u"\xa0", "")
            NewsCommentNum = NewsInfoDiv.find('a', ga_event="article_comment_click").text.replace("⋅", "").replace(" ","")
            # commentNum = int(re.findall(patt1, NewsCommentNum))
            commentNum = re.search(patt1, NewsCommentNum)
            if commentNum:
                commentNum = re.search(patt1, NewsCommentNum).group(0)
            else:
                commentNum = 0
            NewsCommentUrl = NewsInfoDiv.find('a', ga_event="article_comment_click").get('href')
            NewsTime = NewsInfoDiv.find('span', class_="footer-bar-action").text.replace("⋅", "").replace(" ","").replace(u"\xa0", "")
            if NewsTime != "刚刚":
                timeNum = int(re.search(patt1, NewsTime).group(0))
            else:
                timeNum = 0
            timeUnitType = re.sub(patt2, "", NewsTime)
            if timeUnitType == "天前":
                NewsDate = (datetime.now() + timedelta(days=-timeNum)).strftime('%Y%m%d')
            else:
                NewsDate = datetime.now().strftime('%Y%m%d')

            print("第 {} 个 :".format(i))
            print("标题 ：", NewsTitle)
            print("详情URL ：", NewsUrl)
            print("新闻来源 ：", NewsSource)
            print("评论数 ：", commentNum)
            print("日期 ：", NewsDate)

            one = (NewsID,NewsTitle, NewsUrl, NewsSource, commentNum, NewsDate)
            my_mysql.insertTable('tb_toutiao', one)
            print('-------------------------------------------------------------------')
endTime = datetime.now()
print("结束时间：",endTime)
timeDuration = (endTime - startTime).seconds
print("抓完咯")
print("关闭浏览器")
print('耗时 {} 秒'.format(timeDuration))
browser.quit()

# Copyright 2018 Figo Individual. All Rights Reserved.
# Copyright 2018 Figo Individual. All Rights Reserved.
import sqlite3 #数据模块
from bs4 import BeautifulSoup #解析网址模块
import time #时间模块
from selenium import webdriver #浏览器模块
import xlwt

word=input() #手动输入关键词，如果你有固定的关键词可以替换成‘word='keyword'’
urls='https://www.wukong.com/search/?keyword={}'.format(word) #关键词对应的网址
driv = webdriver.Chrome() ##启动谷歌浏览器
driv.get(urls) #在谷歌浏览器中打开网址
# driv.set_page_load_timeout(30) #设定时间，然后捕获timeout异常
js="""  
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
    """
driv.execute_script(js)
#创建一个模拟滚动条滚动到页面底部函数
def scroll(driv):  
    driv.execute_script()
print("开始模拟鼠标拉到文章底部")
b=0
c=0
while b<5: #设置循环，可替换这里值来选择你要滚动的次数
    scroll(driv) #滚动一次
    b=b+1
    print('拉动{}次'.format(b))
    c=c+3
    time.sleep(c) #休息c秒的时间
    
#这个时候页面滚动了多次，是你最终需要解析的网页了

workbook = xlwt.Workbook(encoding='utf-8')
worksheet1 = workbook.add_sheet("悟空问答")
title = ['序号','问题网址','关键词','问题','回答数','收藏数','获赞数','评论数']
for i in range(8):
    worksheet1.write(0, i, title[i])

soup = BeautifulSoup(driv.page_source, "lxml") #解析当前网页
a=1 
for li in  soup.find_all('div',class_="question-v3"):
    channels=word
    url='www.wukong.com'+li.a['href'] #每个文章的地址
    question=li.find('a',target="_blank").text
    answer=li.find('span',class_="question-answer-num").text
    follow=li.find('span',class_="question-follow-num").text
    try:  #捕获异常
        like=li.find('span',class_="like-num").text  #检验语句
    except BaseException:  #异常类型
        like=0  #如果检验语句有异常，那么执行这一句
    else:  #如果没有异常，那么执行下一句
        like=li.find('span',class_="like-num").text 
    try: #同上
        review=li.find('span',class_="comment-count").text
    except BaseException:
        review=0
    else: 
        review=li.find('span',class_="comment-count").text
        
    one = (None,url,channels,question,answer,follow,like,review)
 
    if follow=='暂无收藏': #如果问题没人收藏，那么跳过该问题
        continue
    elif question=='': #如果问题没有文字，跳过该问题
        continue
    elif int(like)==0: #如果点赞人数为0，那么跳过该问题，在这里可以设置
        continue
    elif int(review)==0:
        continue
    elif a<50: #这里可以你需要爬取的问题的个数，如果已经爬取小于50个问题，那么爬下这个问题。
        print("正在爬取第{}篇文章".format(a))
        for i in range(8):
            if i == 0:
                worksheet1.write(a, i, a)
            else:
                worksheet1.write(a, i, one[i])
        a=a+1
        
    else: #如果不满足以上条件，直接跳出循环，停止爬虫
        break
        
workbook.save("C:/Users/Administrator/Desktop/wukong.xls")
print("抓完咯")
print("关闭浏览器")
driv.quit()
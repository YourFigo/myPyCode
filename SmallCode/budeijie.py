# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 09:16:21 2018

@author: Figo
"""
import requests
import re
import os
import urllib.request as urlreq

#获取网页源代码
def get_reponse(url):
    response = requests.get(url).text
    return response

#把包含视频的html返回
def get_content(html):
    # . 匹配任意字符
    # * 匹配匹配前面的元字符的0到n次
    # ? 匹配前面的子表达式0次或1次
    # .* 贪婪模式 
    # .*? 非贪婪模式（最小匹配）
    # re.S 正则表达式可以匹配到换行
    reg = re.compile(r'(<div class="j-r-list-tool-ct-fx">.*?</div>.*?</div>)',re.S)
    return re.findall(reg,html)

#获取图片url
def get_img_url(response):
    reg = r'data-pic="(.*?)"'
    return re.findall(reg,response)

#获取图片名字
def get_img_name(response):
    print(response)
    reg = r'data-text="(.*?)">'
    return re.findall(reg,response)

#下载图片并保存    
def download_img(img_url,path):
    #path先拆分后拼接
    path = ''.join(path.split())
    path = 'D:/reptile/budeijie/{}.jpg'.format(path)
    #    content = get_reponse(img_url)  #另一种下载图片方法
    #    with open(path,'wb') as f:
    #        f.write(content)
    if not os.path.exists(path):
        try:
            urlreq.urlretrieve(img_url,path) #下载图片urlretrieve
            print('download ok !!')
        except:
            print('download fail !!!')
    else:
        print('file already exist !!!')

def run_curr_web(url):
    content = get_content(get_reponse(url))
    #print(content)
#    img_url_list = []
#    img_name_list = []
    count = 0
    for i in content:
        img_url = get_img_url(i)
        if img_url:
            count = count + 1
            print(count)
            img_name = get_img_name(i)
#            img_url_list.append(img_url[0])
#            img_name_list.append(img_name[0])
            try:
                download_img(img_url[0],img_name[0])
#                print(img_name[0],img_url[0])
            except:
                continue
#    print(img_name_list)
#    print(img_url_list)

def main():
    for start_url in start_urls:
        run_curr_web(start_url)

if __name__ == '__main__':
    start_urls = ['http://www.budejie.com/{}'.format(i) for i in range(1,2)]
    main()
    
    


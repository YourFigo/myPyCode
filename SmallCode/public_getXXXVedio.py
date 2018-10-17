# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 09:16:21 2018
@author: Figo
"""
import requests
import re
import os
import urllib.request as urlreq

def get_response(url):
    response = requests.get(url)
    response.encoding = 'utf-8' 
    return response.text

def get_vedio_content(html):
    reg = re.compile(r'(<li><a href="/move/3/2.*?</h3>)',re.S)
    return re.findall(reg,html)

def get_vedio_name(response):
    reg = r'<h3>(.*?)</h3>'
    return re.findall(reg,response)

def get_end_path(response):
    reg = r'<li><a href="/move/3/(.*?)"'
    return re.findall(reg,response)

def get_vedio_path(response):
    reg = r'<td bgcolor="#F4F9FD"><a target="_blank" href="(.*?)" ><b><font color="#0000ff">'
    return re.findall(reg,response)
  
def download_vedio(vedio_url,vedio_name):
    vedio_name = ''.join(vedio_name.split())
    print(vedio_name)
    path = save_path + '/{}.mp4'.format(vedio_name)
    #    content = get_reponse(vedio_url)  #另一种下载方法
    #    with open(path,'wb') as f:
    #        f.write(content)
    if not os.path.exists(path):
        try:
            urlreq.urlretrieve(vedio_url,path)
            print('下载成功 !!')
        except:
            print('下载失败 !!!')
    else:
        print('该文件已存在 !!!')

def run_curr_web(vedio_content,vedio_type_name):
    count_curr_page_vedio = 0
    for one_vedio_content in vedio_content:
        try:
            count_curr_page_vedio = count_curr_page_vedio + 1
            print('  ***** 正在处理第 ',count_curr_page_vedio,' 个视频 ****')
            vedio_name = get_vedio_name(one_vedio_content)[0]
            end_path = get_end_path(one_vedio_content)[0]
            if end_path != '':
                one_path = web_str + str(vedio_type) + '/' + end_path
                vedio_path = get_vedio_path(get_response(one_path))[0]
                download_vedio(vedio_path,vedio_name)
        except:
            continue

def main(start_urls,vedio_type_name):
    count_page = 0
    for start_url in start_urls:
        try:
            count_page = count_page + 1
            print('--------------- 当前进行第 ',count_page,' 页 -----------------')
            html_text = get_response(start_url)
            vedio_content = get_vedio_content(html_text)
            run_curr_web(vedio_content,vedio_type_name)
        except:
            continue


if __name__ == '__main__':
    vedio_type = 3
    type_dict = {1:'yzwm',3:'zptp',7:'sjsp'}
    max_page = 3
    web_str = 'https://www.xxx.com/move/'
    start_urls = [web_str + str(vedio_type) + 
                  '/index_{}.html'.format(i) for i in range(2,max_page)]
    start_urls.insert(0,web_str + '3/index.html')
    save_path = 'F:/小游戏/没视频/真的木有/有了有了/好家伙/藏在这里了/' + type_dict[3]
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path) 
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")
    
    main(start_urls,type_dict[3])
    
#    一天爬虫的成果，spider爬取某网站small视频并保存本地
#    以上代码仅需将 web_str 中的 xxx 替换，
#    以及将 download_vedio() 中的保存地址 save_path 修改即可使用
#    2018-06-09 亲测可用，最简单的串行下载，没事了挂着就可以

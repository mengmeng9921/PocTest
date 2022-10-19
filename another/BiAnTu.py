# 学习python，自己写的彼岸图网的爬虫，仅供学习参考，请勿用于非法用途，产生的法律风险由您自己负责。
import argparse
import re
import time
import os
import requests
from bs4 import BeautifulSoup

# sleep 请求间隔
# startpage 从哪页开始爬取 endpage 结束到哪页
# bianurl 爬取彼岸网哪个网页
# cookie 你登录的cookie
# path 文件保存的路径
# example：python3 main.py -u https://pic.netbian.com/ -c "yourcookie" -t 6 -p "/Users/administrator/Desktop/img/img/" -s 1 -e 2
sleep = 5
startpage = 1
endpage = 1
bianurl = "https://pic.netbian.com/"
cookie = ""
save_path = "/Users/administrator/Desktop/img/"

# 正则预编译
obj = re.compile(r"ViewMore\.php\?classid=(?P<classid>.*?)\&id=(?P<id>.*?)\&")


def downloadImg(url, name):
    print(url)
    head = {
        "Cookie": cookie,
        "Referer": "https://pic.netbian.com/tupian/"
    }
    img_resp = requests.get(url, headers=head)
    # 获得图片字节码
    # print(img_resp.content)
    # 以classid+id的形式命名图片
    img_name = str(name) + ".jpeg"
    print(img_name)
    with open(save_path + img_name, mode="wb") as f:
        f.write(img_resp.content)
        print(name + ".jpeg保存成功")
    f.close()


# 处理子页面的url内容
def babyurl(url):
    # 获取子页面内容并进行gbk编码
    resp = requests.get(url)
    resp.encoding = 'gbk'
    print(url)
    # print(resp.text)
    # 使用预编译的正则表达式找出id和classid
    result = obj.finditer(resp.text)
    # 提取id和classid，并拼接URL
    for i in result:
        url = "https://pic.netbian.com/downpic.php?id=" + i.group("id") + "&classid=" + i.group("classid")
        downloadImg(url, i.group("id") + i.group("classid"))


# 彼岸图网，搜索url内的图片href地址，并拼接为完整url
def baseurl(url):
    # 请求彼岸图网地址
    resp = requests.get(url)
    resp.encoding = 'gbk'
    # print(resp.text)
    # 创建bs4对象
    page = BeautifulSoup(resp.text, "html.parser")
    # 搜索ul标签，并找到内部的a标签
    a = page.find('ul', class_="clearfix").find_all('a')
    # 遍历a标签，组成完整的彼岸图网地址
    for i in a:
        babyurl("https://pic.netbian.com" + i.get('href'))
        time.sleep(sleep)


def pagego(bianurl):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if startpage == 1:
        if endpage == 1:
            baseurl(bianurl)

        else:
            baseurl(bianurl)
            for i in range(startpage + 1, endpage + 1):
                baseurl(bianurl + "index_" + str(i) + ".html")

    else:
        for i in range(startpage, endpage + 1):
            baseurl(bianurl + "index_" + str(i) + ".html")


def cmdline(known=False):
    global sleep
    global startpage
    global endpage
    global bianurl
    global cookie
    global save_path
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help='input your url: -u http://test.com',
        type=str,
        default="https://pic.netbian.com/"
    )
    parser.add_argument(
        '-c',
        '--cookie',
        help='set your cookie: --cookie yourcookie',
        type=str,
        default=""
    )
    parser.add_argument(
        '-t',
        '--time',
        help='sleep 5s: --time 5 ',
        type=int,
        default=5
    )
    parser.add_argument(
        '-p',
        '--path',
        help='imgfile save path: --path /User/name/Desktop/img/ ',
        type=str,
        default="/Users/administrator/Desktop/img/img/"
    )
    parser.add_argument(
        '-s',
        '--start',
        help='startpage : --start 1 ',
        type=int,
        default=1
    )
    parser.add_argument(
        '-e',
        '--end',
        help='endpage: --end 1 ',
        type=int,
        default=1
    )
    opt = parser.parse_args()
    sleep = opt.time
    startpage = opt.start
    endpage = opt.end
    bianurl = opt.url
    cookie = opt.cookie
    save_path = opt.path


if __name__ == '__main__':
    cmdline()
    pagego(bianurl)
# 学习python，自己写的彼岸图网的爬虫，仅供学习参考，请勿用于非法用途，产生的法律风险由您自己负责。

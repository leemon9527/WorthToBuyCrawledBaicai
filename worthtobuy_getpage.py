# -*- coding: utf-8 -*-
__author__ = 'leemon'
import urllib2
from lxml import etree
import re
import time
import MySQLdb
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getPage(target_url,hdr):
    url=[]
    req = urllib2.Request(target_url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
        return
    content = page.read()
    content_html=etree.HTML(content)
    conn = mysql_conn()
    for list in content_html.xpath('//div[@class="leftWrap"]/div[@class="list list_preferential "]'):
        tmp=[]
        baicai_url = list.xpath('a/@href')[0]
        baicai_title = list.xpath('a/@title')[0]
        baicai_date = list.xpath('div[@class="listTitle"]/h2/a/span[@class="red"]/text()')[0]
        baicai_time = list.xpath('div[@class="listRight"]/div[@class="lrTop"]/span[@class="lrTime"]/text()')[0]
        try:
            float(baicai_date)
            baicai_flag=True
        except:
            baicai_flag=False
        if len(baicai_time)<11:
            baicai_time=time.strftime("%m-%d ")+baicai_time
        tmp.append(baicai_url)
        tmp.append(baicai_title)
        tmp.append(baicai_time)
        tmp.append(baicai_flag)
        url.append(tmp)
        data = mysql_select(conn,r"select * from page_info where page_url='%s'" % baicai_url)
        if data:
            continue
        else:
            mysql_insert(conn,r"INSERT INTO page_info(page_url,is_crawled,release_time) values('%s','%s','%s')" %(baicai_url,'False',baicai_time))
    conn.close()
    return url
def getPageInfo(urlinfo,hdr):
    target_url=urlinfo[0]
    req = urllib2.Request(target_url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
        return
    content = page.read()
    content_html=etree.HTML(content)
    regex = re.compile('\((.*)\)')
    i=0
    if not len(content_html.xpath('//div[@class="news_content"]/div[@class="siteWrap"]')):
        for list in content_html.xpath('//div[@class="inner-block"]/div[@class="siteWrap"]'):
            i+=1
            goods_info = dict(eval(regex.findall(list.xpath('div/a/@onclick')[0])[0]))
            url = list.xpath('div/a/@href')[0]
            pic_url = list.xpath('div/a/img/@src')[0]
            goods_info['url'] = url
            goods_info['pic_url'] = pic_url
            goods_info['release_time'] = urlinfo[2]
            print i,goods_info
            dumpToMySQL(goods_info)
    else:
        for list in content_html.xpath('//div[@class="news_content"]/div[@class="siteWrap"]'):
            i+=1
            goods_info = dict(eval(regex.findall(list.xpath('div/a/@onclick')[0])[0]))
            url = list.xpath('div/a/@href')[0]
            pic_url = list.xpath('div/a/img/@src')[0]
            goods_info['url'] = url
            goods_info['pic_url'] = pic_url
            goods_info['release_time'] = urlinfo[2]
            dumpToMySQL(goods_info)
def getPageInfoSingle(urlinfo,hdr):
    target_url=urlinfo[0]
    req = urllib2.Request(target_url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
        return
    content = page.read()
    content_html=etree.HTML(content)
    regex = re.compile('\((.*)\)')
    goods_info = dict(eval(regex.findall(content_html.xpath('//div[@class="article-top-box clearfix"]/a/@onclick')[0])[0]))
    url = content_html.xpath('//div[@class="article-top-box clearfix"]/a/@href')[0]
    pic_url = content_html.xpath('//div[@class="article-top-box clearfix"]/a/img/@src')[0]
    goods_info['url'] = url
    goods_info['pic_url'] = pic_url
    goods_info['release_time'] = urlinfo[2]
    dumpToMySQL(goods_info)
def mysql_select(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return  data
def mysql_insert(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
def mysql_update(conn,sql):
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
def mysql_conn():
    conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="worthtobuy",charset="utf8")
    return conn
def getFloatPrice(price):
    try:
        FloatPrice=float(price)
    except:
        FloatPrice=0
    return FloatPrice
def dumpToMySQL(goods_info):
    conn = mysql_conn()
    # data = mysql_select(conn,r"select * from lottery where issue=%s" % (issue))
    data = mysql_select(conn,r"select * from worthtobuy where id=%s" % goods_info['id'])
    if data:
        return
    else:
        mysql_insert(conn,r"INSERT INTO worthtobuy values('%s','%s',%f,'%s','%s','%s','%s','%s')" %
                     (goods_info['id'],MySQLdb.escape_string(goods_info['name']),getFloatPrice(goods_info['price']),
                      goods_info['mall'],goods_info['category'],goods_info['url'],
                      goods_info['pic_url'],goods_info['release_time']))
    conn.close()
def checkIsCrawled(url):
    conn = mysql_conn()
    data = mysql_select(conn,r"select is_crawled from page_info where page_url='%s'" % url)
    conn.close()
    #返回data为tunple,因为返回值只有一个，所以取tunple[0][0]
    return  eval(data[0][0])

def setCrawled(url):
    conn = mysql_conn()
    mysql_update(conn,r"UPDATE page_info SET is_crawled='True' where page_url='%s'" % url)
    conn.close()

if __name__ == '__main__':
    i=1
    while i<10:
        target_url = u"http://www.smzdm.com/youhui/tag/%E7%99%BD%E8%8F%9C%E5%85%9A/p"+str(i)+"/"
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        page_url=getPage(target_url,hdr)
        #检测每次传入的链接是否被爬过，如果爬过就跳过
        if len(page_url):
            for urlinfo in page_url:
                if urlinfo[3]:
                    if not checkIsCrawled(urlinfo[0]):
                        print u"Crawled MultiGoodsPage:"+urlinfo[0]
                        getPageInfo(urlinfo,hdr)
                        setCrawled(urlinfo[0])
                else:
                    if not checkIsCrawled(urlinfo[0]):
                        print u"Crawled SingleGoodsPage:"+urlinfo[0]
                        getPageInfoSingle(urlinfo,hdr)
                        setCrawled(urlinfo[0])
        else:
            errorMsg="Page: "+target_url+"getGoodsinfo failed!"
            with open('error.log','a') as f:
                f.write(errorMsg+'\n')
            f.close()
        i+=1


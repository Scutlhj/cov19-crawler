import os
import re
import csv
import json
import time
import jieba
import random
import pymssql
import datetime
import requests
import pandas as pd
import tkinter as tk
from bs4 import BeautifulSoup
from time import sleep
from tkinter import messagebox
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from pyecharts.charts import Map
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from snapshot_phantomjs import snapshot
from stylecloud import gen_stylecloud


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "www.baidu.com",
    # cookies要打开百度定时改
    "Cookie": 'BIDUPSID=172029B5E75768BCDD39A34FF2896A06; PSTM=1595486180; __yjs_duid=1_f24883a0baf670f2c1c802b4d085a75e1620128903890; BD_UPN=12314753; sugstore=0; sug=3; ORIGIN=0; bdime=0; BDUSS=RtRm9nTXl0Tm5jZHZwM0xVUzF0Q05UdmlRTVFYdnVkUkRQUG5ldnA0ajRwS2hpRVFBQUFBJCQAAAAAAQAAAAEAAAB4ZCtjbGhqeXlkczEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPgXgWL4F4FiRV; BDUSS_BFESS=RtRm9nTXl0Tm5jZHZwM0xVUzF0Q05UdmlRTVFYdnVkUkRQUG5ldnA0ajRwS2hpRVFBQUFBJCQAAAAAAQAAAAEAAAB4ZCtjbGhqeXlkczEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPgXgWL4F4FiRV; H_WISE_SIDS_BFESS=110085_127969_164326_177990_178384_178610_179345_179435_179623_180276_181133_181135_181487_181588_182000_182235_182531_182848_183035_183227_183329_183750_183976_184009_184267_184321_184440_184560_184793_184810_184826_185029_185036_185268_185363_185517_185880_186318_186412_186595_186636_186682_186833_186841_187023_187042_187054_187062_187091_187189_187287_187433_187529_187533_187563_187669_187726_187816_187928_187936_187963_188039_188181_188333_188341_188426_188467_188721_188732_188742_188786_188830_188844_188873_188899_188941; newlogin=1; BAIDUID=97503019492655AC6334D328BEB15E79:FG=1; ZFY=5:ALhlMGGMkldu2J8PZSrGiR0ruDhYH:B4mWrqLENq46M:C; BAIDUID_BFESS=97503019492655AC6334D328BEB15E79:FG=1; B64_BOT=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1667649028,1667788872,1668351736,1669011222; BA_HECTOR=80a00ha185a58h0g0kah8n5c1hnmo0o1e; baikeVisitId=9ba4e166-6073-4a20-89f1-f41cdeb38c5c; COOKIE_SESSION=33192_0_7_8_8_23_1_0_7_7_1_2_658702_0_0_0_1669011236_0_1669044424|9#207050_27_1663512961|9; __bid_n=1849ae34797e80bb3e4207; RT="z=1&dm=baidu.com&si=z7oag45kfl&ss=laqytzj6&sl=8&tt=4as&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=akds&ul=cgbv&hd=cge4"; BDRCVFR[-BxzrOzUsTb]=mk3SLVN4HKm; BD_HOME=1; H_PS_PSSID=26350'

}

headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"
}

headers3 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "zhidao.baidu.com",
    # cookies要打开百度定时改
    "Cookie": 'BIDUPSID=172029B5E75768BCDD39A34FF2896A06; PSTM=1595486180; __yjs_duid=1_f24883a0baf670f2c1c802b4d085a75e1620128903890; BDUSS=RtRm9nTXl0Tm5jZHZwM0xVUzF0Q05UdmlRTVFYdnVkUkRQUG5ldnA0ajRwS2hpRVFBQUFBJCQAAAAAAQAAAAEAAAB4ZCtjbGhqeXlkczEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPgXgWL4F4FiRV; BDUSS_BFESS=RtRm9nTXl0Tm5jZHZwM0xVUzF0Q05UdmlRTVFYdnVkUkRQUG5ldnA0ajRwS2hpRVFBQUFBJCQAAAAAAQAAAAEAAAB4ZCtjbGhqeXlkczEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPgXgWL4F4FiRV; H_WISE_SIDS_BFESS=110085_127969_164326_177990_178384_178610_179345_179435_179623_180276_181133_181135_181487_181588_182000_182235_182531_182848_183035_183227_183329_183750_183976_184009_184267_184321_184440_184560_184793_184810_184826_185029_185036_185268_185363_185517_185880_186318_186412_186595_186636_186682_186833_186841_187023_187042_187054_187062_187091_187189_187287_187433_187529_187533_187563_187669_187726_187816_187928_187936_187963_188039_188181_188333_188341_188426_188467_188721_188732_188742_188786_188830_188844_188873_188899_188941; newlogin=1; FPTOKEN=30$y3IVmyTFfywuggN14sYgKIdWwHFEHL6uey1tNJj1/4N0uoVAQLpaxnWzbkV5DTfe7YORCgLfuoDpKtDrBT6OoqrU6sGuX5tzSdjAfuMBJY3z3eH51g5vKiFBCHu3TqUE4AdC5hQHKeWFCQVdmUVmicfDAIzO5hH2xZvFQGz24t6x8tQRoG+Q31/cwVHKqx8Rrmnd267euchmHJK59BfBpCY6Iqh+HCje209rDWDIEccipbArlgFBr+3S2T3bsw7K7NG6yYPpIOpEQlI/jyznng2pBxj0JZc779WMSY9EOq7mvKF4uqDnkVKF68pxW3VGROuT5ZsJihYWLYmURIpXnEKoL+VPLw/YZWFLfnyBxCrKJPFaMTE0gtcz+WtRQ/P5|N9J7AYfcKCgKK2uBfd8R5mMAxqYuAcLYrT/YrB3Yg6M=|10|bfe10905d485388614cc6056230eb986; BAIDUID=97503019492655AC6334D328BEB15E79:FG=1; ZFY=5:ALhlMGGMkldu2J8PZSrGiR0ruDhYH:B4mWrqLENq46M:C; BAIDUID_BFESS=97503019492655AC6334D328BEB15E79:FG=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=80a00ha185a58h0g0kah8n5c1hnmo0o1e; RT="z=1&dm=baidu.com&si=z7oag45kfl&ss=laqytzj6&sl=8&tt=4as&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=akds&ul=cgbv&hd=cge4"; BDRCVFR[-BxzrOzUsTb]=mk3SLVN4HKm; H_PS_PSSID=26350; ZD_ENTRY=empty; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1668669020,1668752231,1669010751,1669095532; shitong_key_id=2; __bid_n=1849df1f8e084c3acd4207; session_id=1669099278560557791815750627; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1669099279; ab_sr=1.0.1_OWIxZWRiNjc3MDhjYjAzNTYxYjVkZGEzNzkzNDAyNjk4MjJjZTk5MmQ3NGM1YTQ2NmNiMTdkYzYyZTYzY2Q1NjUzZTc5ODkxYjNkYjAyODRjZmI2M2Y5MWMwZjU3MWMyODFlNzA2MDBmMDA4ZmYxMTFhMDU4ZmRiOTAyNzI3OGJjNjJkMzkwN2I4MWQ3NTFiODMwNWI3YmQyNjVkN2FhNTU0YmNkNjkyNjBiY2RhZmU2NGZiNGIxODY1MTM0YjFj; shitong_data=4b5104486ce0fdae7a7dc97ac282845064416793b1789d6ae00f27c68e67e0a0c0d18e6142af4e7d4cb10c3139e39180648f72d6628744ea774964cacdf32de1ae4573bd6f98f13d9b7f262fed0d44525a2f62ded8c2310400695305212b2953; shitong_sign=37a2fd34'
}

#  -------------------------------------------------------------------------------------------
user = 'covid-19'  # 数据库的登录名
password = 'root'  # 数据库的密码
id = 'LAPTOP-QUUOMBBH'  # 数据库服务器名称，备选值：LAPTOP-QUUOMBBH | LAPTOP-NTOQ1RLL
name = 'data of covid-19'  # 建立的新冠数据库名称，没有的话得提前建好数据库
#  -------------------------------------------------------------------------------------------

filename = "{}国内疫情数据.csv".format(datetime.datetime.now().strftime("%Y-%m-%d"))
f_folder = os.getcwd() + '\\国内疫情数据\\' + filename
foreign_filename = "{}国外疫情数据.csv".format(datetime.datetime.now().strftime("%Y-%m-%d"))
foreign_folder = os.getcwd() + '\\国外疫情数据\\' + foreign_filename


# 百度知道词云
def search_for_ciyun(key, numbers):
    answer_list = []
    url_list = []
    for i in range(0, numbers):
        url_root = "https://zhidao.baidu.com/search?word=" + key + "&pn=" + str(i * 10)
        req = requests.get(url_root, headers=headers3)
        req.encoding = 'gbk'
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        html_list = soup.find_all('a', class_='ti')
        for j in html_list:
            url_list.append(j['href'])
        time.sleep(random.uniform(0.5, 1))
    for new_url in url_list:
        new_req = requests.get(new_url, headers=headers3)
        new_req.encoding = 'gbk'
        new_html = new_req.text
        new_soup = BeautifulSoup(new_html, 'html.parser')
        answer_list.append(new_soup.find('div', class_='rich-content-container rich-text-').text.replace('\n', ''))
        time.sleep(random.uniform(0.5, 1))
    wordlist = jieba.cut_for_search(''.join(answer_list))
    results = ' '.join(wordlist)
    folder_path = os.getcwd() + '\\词云结果'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    gen_stylecloud(text=results, icon_name='fas fa-flag', font_path='C:/Windows/Fonts/STXINWEI.TTF',
                   background_color='white', output_name='词云结果\\' + '{}.jpg'.format(key),
                   custom_stopwords=['你', '我', '的', '了', '在', '吧', '相信', '是', '也', '都', '不', '吗', '就',
                                     '我们',
                                     '还', '大家', '你们', '就是', '以后']
                   )


# 搜索功能的实现
def search(keyword, result_file, max_page):
    for page in range(0, max_page):
        print('开始爬取第{}页'.format(page + 1))
        wait_times = random.uniform(1, 2)  # 等待时长
        print('需要等待{}秒'.format(wait_times))
        sleep(wait_times)  # 等待，防止过度爬取IP被封禁
        url = 'https://www.baidu.com/s?wd=' + keyword + '&pn=' + str(page * 10)  # 核心
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        html = r.text
        print(html)
        print('响应码是:{}'.format(r.status_code))
        soup = BeautifulSoup(html, 'html.parser')
        result_list = soup.find_all(class_='result c-container xpath-log new-pmd')
        print('正在爬取:{},共查询到{}个结果'.format(url, len(result_list)))
        title_list = []  # 标题
        real_url_list = []  # 真链
        desc_list = []  # 简介
        date_list = []  # 发布日期
        auditor_list = []  # 发布的网站
        for result in result_list:
            title = result.find('a').text
            print('网页标题:', title)
            href = result.find('a')['href']
            real_url = get_real_url(url=href)
            try:
                desc = result.find(class_='content-right_8Zs40').text
            except:
                desc = ""
            try:
                auditor = result.find(class_='c-color-gray').text
            except:
                auditor = ""
            try:
                date = result.find(class_='c-color-gray2').text
            except:
                date = ""
            title_list.append(title)
            real_url_list.append(real_url)
            desc_list.append(desc)
            date_list.append(date)
            auditor_list.append(auditor)
        df = pd.DataFrame(
            {
                'title': title_list,
                'datetime': date_list,
                'auditorsite': auditor_list,
                'url': real_url_list,
                'content': desc_list,
            }
        )
        if os.path.exists(result_file):
            header = None
        else:
            header = ['网页标题', '发布时间', '发布网站', '链接', '网页简介']  # csv文件标头
        df.to_csv(result_file, mode='a+', index=False, header=header, encoding='utf-8')


# 搜索功能中提取真实url
def get_real_url(url):
    r = requests.get(url, headers=headers, allow_redirects=False)  # 不允许重定向
    if r.status_code == 302:  # 如果返回302，就从响应头获取真实地址
        real_url = r.headers.get('Location')
    else:  # 否则从返回内容中用正则表达式提取出来真实地址
        real_url = re.findall("URL='(.*?)'", r.text)[0]
    print('链接:', real_url)
    return real_url


# 更新今日国内疫情数据
def got_province_data():
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner&city="
    req = requests.get(url)
    req.encoding = "UTF-8"
    text = req.text
    soup = BeautifulSoup(text, 'html.parser')
    str_list = soup.find("script", id="captain-config").text
    str_list = str_list.replace('\'', '')  # 去掉单引号
    str_list = str_list.encode('utf-8')
    js_list = json.loads(str_list)
    connect = pymssql.connect(id, user, password, name, charset='UTF-8')
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    # 创建表的语句,第一次使用时取消注释并运用
    '''
    create_table = "CREATE TABLE Table2([省/自治区/直辖市] nvarchar(50),新增确诊 int,新增本土 int,新增境外 int,新增无症状 int,现有确诊 int,累计确诊 int,累计死亡 int,累计治愈 int,统计时间 datetime)"
    cursor.execute(create_table)
    connect.commit()
    '''
    delect_data = "DELETE FROM Table2"  # 清除老数据
    cursor.execute(delect_data)
    connect.commit()

    domestic = js_list['component'][0]['caseList']
    for province in domestic:
        province_data = [province['confirmedRelative'], province['nativeRelative'], province['overseasInputRelative'],
                         province['asymptomaticRelative'], province['curConfirm'], province['confirmed'],
                         province['died'], province['crued']]

        # 给空数据赋默认值
        for i in range(0, 8):
            if province_data[i] == '':
                province_data[i] = 0

        # 编写 存入省的数据 sql脚本
        sql = "insert into Table2([省/自治区/直辖市],新增确诊,新增本土,新增境外,新增无症状,现有确诊,累计确诊,累计死亡,累计治愈,统计时间) " \
              "values('{}',{},{},{},{},{},{},{},{},'{}')".format(province["area"], province_data[0], province_data[1],
                                                                 province_data[2], province_data[3], province_data[4],
                                                                 province_data[5], province_data[6], province_data[7],
                                                                 datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        cursor.execute(sql)
        connect.commit()

    with open("{}国内疫情数据.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), 'w', encoding='UTF-8',
              newline='') as f:
        # 可能会报错的写法： result = pandas.read_sql("select * from Table2 order by 新增确诊 desc", connect)
        cursor.execute("""select * from Table2 order by 新增确诊 desc""")
        raw = cursor.fetchall()
        index = ['省/自治区/直辖市', '新增确诊', '新增本土', '新增境外', '新增无症状', '现有确诊', '累计确诊', '累计死亡', '累计治愈', '统计时间']
        result = pd.DataFrame(columns=index, data=raw)
        #print(result)
        folder_path = os.getcwd() + '\\国内疫情数据'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        result_file = folder_path + '\\' + f.name
        result.to_csv(result_file, sep=',', header=True, index=False)

    os.remove(f.name)
    cursor.close()
    connect.close()


# 更新国外今日数据
def got_foreign_data():
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner&city="
    req = requests.get(url)
    req.encoding = "UTF-8"
    text = req.text
    soup = BeautifulSoup(text, 'html.parser')
    str_list = soup.find("script", id="captain-config").text
    str_list = str_list.replace('\'', '')  # 去掉单引号
    str_list = str_list.encode('utf-8')
    js_list = json.loads(str_list)

    connect = pymssql.connect(id, user, password, name, charset='UTF-8')
    cursor = connect.cursor()
    # 创建表的语句,第一次使用时取消注释并运用
    '''
    create_table = "CREATE TABLE Table3([国家/地区] nvarchar(50),新增确诊 int,现有确诊 int,累计确诊 int,新增死亡 int,累计死亡 int,累计治愈 int,统计时间 datetime)"
    cursor.execute(create_table)
    connect.commit()
    '''
    delete_data = "DELETE FROM Table3"  # 清除老数据
    cursor.execute(delete_data)
    connect.commit()

    # 外国数据部分不统计，因此数据仅供参考
    foreign = js_list['component'][0]['caseOutsideList']
    for country in foreign:
        sql = "insert into Table3([国家/地区],新增确诊,现有确诊,累计确诊,新增死亡,累计死亡,累计治愈,统计时间) values('{}',{},{},{},{},{},{},'{}')".format(
            country['area'], country['confirmedRelative'], country['curConfirm'], country['confirmed'],
            country['diedRelative'],
            country['died'], country['crued'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(sql)
        connect.commit()

    with open(foreign_filename, 'w', encoding='UTF-8', newline='') as f:
        cursor.execute("""select * from Table3 order by 新增确诊 desc""")
        raw = cursor.fetchall()
        index = ['国家/地区', '新增确诊', '现有确诊', '累计确诊', '新增死亡', '累计死亡', '累计治愈', '统计时间']
        result = pd.DataFrame(columns=index, data=raw)
        #print(result)
        folder_path = os.getcwd() + '\\国外疫情数据'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        result_file = folder_path + '\\' + f.name
        result.to_csv(result_file, sep=',', header=True, index=False)

    os.remove(f.name)
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接


# 画各省新增直方图
def show_province_data():
    df = pd.read_csv(f_folder)
    df.drop(axis=0, index=0, inplace=True)
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px",
                                    height="600px")).add_xaxis(df['省/自治区/直辖市'].tolist()).add_yaxis("新增确诊",
                                                                                                   df['新增确诊'].tolist()).set_global_opts(title_opts=opts.TitleOpts(title='今日疫情数据',
                                                                                                                                                                  subtitle="{}疫情数据".format(
                                                                                                                                                                      datetime.datetime.now().strftime("%Y-%m-%d"))), xaxis_opts=opts.AxisOpts(name="省", axislabel_opts={"rotate": 45, "interval": 0}))
    )
    make_snapshot(snapshot, bar.render(), os.getcwd() + '\\国内疫情数据\\' + "{}国内新增.png".format(datetime.datetime.now().strftime("%Y-%m-%d")), is_remove_html=True)


# 画国内新冠感染分布图
def draw_map():
    df = pd.read_csv(f_folder)
    province_data = []
    for data in zip(df['省/自治区/直辖市'].tolist(), df['累计确诊'].tolist()):
        list(data)
        province_data.append(data)
    provice_map = (
        Map(init_opts=opts.InitOpts(theme=ThemeType.ESSOS, width="1000px",
                                    height="600px")).add("累计感染人数", province_data, "china", is_map_symbol_show=False,
                                                         zoom=1.2).set_global_opts(title_opts=opts.TitleOpts(title="中国疫情感染人数分布图",
                                                                                                             subtitle='更新日期:{}'.format(datetime.datetime.now().strftime("%Y-%m-%d"))),
                                                                                   visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                                                                                     pieces=[
                                                                                                                         {
                                                                                                                             "min": 20001,
                                                                                                                             "label": '>20000人',
                                                                                                                             "color": "#6F171F"},
                                                                                                                         {
                                                                                                                             "min": 10001,
                                                                                                                             "max": 20000,
                                                                                                                             "label": '10001-20000人',
                                                                                                                             "color": "#C92C34"},
                                                                                                                         {
                                                                                                                             "min": 5001,
                                                                                                                             "max": 10000,
                                                                                                                             "label": '5001-10000人',
                                                                                                                             "color": "#E35B52"},
                                                                                                                         {
                                                                                                                             "min": 1001,
                                                                                                                             "max": 5000,
                                                                                                                             "label": '1001-5000人',
                                                                                                                             "color": "#F39E86"},
                                                                                                                         {
                                                                                                                             "min": 1,
                                                                                                                             "max": 1000,
                                                                                                                             "label": '1-1000人',
                                                                                                                             "color": "#FDEBD0"}]))
    )
    make_snapshot(snapshot, provice_map.render(), os.getcwd() + '\\国内疫情数据\\' + "疫情累计感染人数分布图.png", is_remove_html=True)


# 画近60天国内新增折线图
def draw_inner_line_chart():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    req = requests.get(url)
    req.encoding = "UTF-8"
    text = req.json()
    json_data = json.loads(text['data'])
    inner_data = json_data['chinaDayAddList']
    date = []
    confirm = []
    for num in range(len(inner_data)):
        if inner_data[num]['confirm'] <= 1e7:
            date.append(inner_data[num]['date'])
            confirm.append(inner_data[num]['confirm'])
        else:
            # url中11月5日数据出现问题，不可能单日新增74328643例，数据为本人上网查询得到
            date.append(inner_data[num]['date'])
            confirm.append(26180)

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, width="1000px", height="600px")).set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category", name="日期"),
            # axislabel_opts={"rotate": 45, "interval": 0}),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name='新增人数',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        ).add_xaxis(xaxis_data=date).add_yaxis(
            series_name="全国近60天新增病例折线图(包括港澳台地区)",
            y_axis=confirm,
            symbol="circle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    make_snapshot(snapshot, line.render(), os.getcwd() + '\\国内疫情数据\\' + "疫情近期新增折线图.png", is_remove_html=True)


# 查询某省或某市的数据
def search_city(province, city):
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner&city="
    req = requests.get(url)
    req.encoding = "UTF-8"
    text = req.text
    soup = BeautifulSoup(text, 'html.parser')
    str_list = soup.find("script", id="captain-config").text
    str_list = str_list.replace('\'', '')  # 去掉单引号
    str_list = str_list.encode('utf-8')
    js_list = json.loads(str_list)
    domestic = js_list['component'][0]['caseList']
    # 获取该省的字典
    province_data = list(filter(lambda item: item['area'] == province, domestic))
    if not province_data:
        return False
    else:
        province_data = province_data[0]
        if city == '':
            return {'地区': province_data['area'], '新增本土': province_data['nativeRelative'],
                    '新增本土无症状': province_data['asymptomaticLocalRelative'],
                    '现有确诊': province_data['curConfirm'],
                    '累计确诊': province_data['confirmed'], '累计死亡': province_data['died'],
                    '累计治愈': province_data['crued']}
        else:
            city_data = list(filter(lambda item: item['city'] == city, province_data['subList']))
            if not city_data:
                return False
            else:
                city_data = city_data[0]
                return {'地区': city_data['city'], '新增本土': city_data['nativeRelative'],
                        '新增本土无症状': city_data['asymptomaticLocalRelative'], '现有确诊': city_data['curConfirm'],
                        '累计确诊': city_data['confirmed'], '累计死亡': city_data['died'],
                        '累计治愈': city_data['crued']}


# 画国外top10新增直方图,使用前得提前更新csv
def draw_foreign_chart():
    top5 = pd.read_csv(foreign_folder)
    country = list(top5[0:10]['国家/地区'])
    country_add = list(top5[0:10]['新增确诊'])
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="800px",
                                    height="500px")).add_xaxis(country).add_yaxis("新增确诊",
                                                                                  country_add).set_global_opts(title_opts=opts.TitleOpts(title='今日国外疫情数据top5',
                                                                                                                                         subtitle="统计时间:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                                                                                                               xaxis_opts=opts.AxisOpts(name="国家", axislabel_opts={"interval": 0}))
    )
    make_snapshot(snapshot, bar.render(), os.getcwd() + '\\国外疫情数据\\'"{}国外新增top10.png".format(datetime.datetime.now().strftime("%Y-%m-%d")),
                  is_remove_html=True)


# 查看某个国家死亡人数占比饼图
def foreign_pie_chart(countryname):
    api = 'https://apis.tianapi.com/ncovabroad/index?key=c9a379ee6f95f7e0153935bad5757b2c'
    req = requests.get(api)
    data = req.json()['result']['list']
    country_data = list(filter(lambda item: item['provinceName'] == countryname, data))
    if len(country_data) == 0:
        return False
    else:
        country_data = country_data[0]
        time_local = time.localtime(country_data['modifyTime'] / 1000)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        title_name = ["现有确诊", "累计死亡", "累计治愈"]
        numbers = [country_data['currentConfirmedCount'], country_data['deadCount'], country_data['curedCount']]
        pie = (
            Pie().add("",
                      [list(z) for z in zip(title_name, numbers)]).set_global_opts(title_opts=opts.TitleOpts(title='{}新冠死亡、治愈人数占患病比重'.format(countryname),
                                                                                                             subtitle='截止{}'.format(dt))).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        folder_path = os.getcwd() + '\\国外疫情数据'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        make_snapshot(snapshot, pie.render(), os.getcwd() + '\\国外疫情数据\\' + "{}新冠饼状图.png".format(countryname),
                      is_remove_html=True)
        return True


# SARS相关数据
def get_SARS_data():
    url = 'https://baiyunju.cc/3864'
    req = requests.get(url)
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')
    province_data = BeautifulSoup(str(table[0]), 'html.parser').find_all('tr')
    country_data = BeautifulSoup(str(table[1]), 'html.parser').find_all('tr')
    province_list = []
    country_list = []
    for data in province_data:
        children_list = []
        data_ = BeautifulSoup(str(data), 'html.parser').find_all('td')
        for data__ in data_:
            children_list.append(data__.text)
        province_list.append(children_list)

    list1 = []
    country = BeautifulSoup(str(country_data[0]), 'html.parser').find_all('th', scope='col')
    for i in country:
        list1.append(i.text)
    country_list.append(list1)

    for data1 in range(1, len(country_data)):
        children_list1 = []
        data1_ = BeautifulSoup(str(country_data[data1]), 'html.parser').find_all('td')
        for data1__ in data1_:
            children_list1.append(data1__.text)
        country_list.append(children_list1)

    folder_path = os.getcwd() + '\\SARS数据'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open('SARS数据\\SARS国内数据.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in province_list:
            writer.writerow(row)

    with open('SARS数据\\SARS全球数据.csv', 'w', newline='', encoding='utf-8') as csvfile1:
        writer1 = csv.writer(csvfile1)
        for row in country_list:
            writer1.writerow(row)

    # 生成SARS各省感染人数直方图
    df = pd.read_csv('SARS数据\\SARS国内数据.csv')
    df.drop(axis=0, index=0, inplace=True)
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_xaxis(df['省份'].tolist())
        .add_yaxis("感染病例", df['病例'].tolist())
        .add_yaxis("死亡人数", df['死亡人数'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title='SARS各省感染人数'),
                         xaxis_opts=opts.AxisOpts(name="省份", axislabel_opts={"rotate": 45, "interval": 0}))

    )
    make_snapshot(snapshot, bar.render(), "SARS数据\\SARS各省感染及死亡人数直方图.png",
                  is_remove_html=True)
    # 去除数字中逗号
    df1 = pd.read_csv('SARS数据\\SARS全球数据.csv')
    df1.drop(axis=0, index=0, inplace=True)
    for j in range(len(df1)):
        df1.iat[j, 1] = df1.iat[j, 1].replace(',', '')
    bar1 = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_xaxis(df1['国家/地区'].tolist())
        .add_yaxis("感染病例", df1['确诊'].tolist())
        .add_yaxis("死亡人数", df1['死亡'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title='SARS各国感染人数及死亡人数'),
                         xaxis_opts=opts.AxisOpts(name="国家/地区", axislabel_opts={"rotate": 45, "interval": 0}))
    )
    make_snapshot(snapshot, bar1.render(), "SARS数据\\SARS各国感染及死亡人数直方图.png",
                  is_remove_html=True)


if __name__ == '__main__':
    window = tk.Tk()
    # 设置窗口的标题
    window.title('疫情信息系统')
    # 设置并调整窗口的大小、位置
    window.geometry('600x520+300+200')


    def click_button1():
        got_province_data()
        messagebox.showinfo(title='温馨提示', message='{}国内疫情数据.csv已生成，请在对应python路径查看'.format(
            datetime.datetime.now().strftime("%Y-%m-%d")))

    # 点击按钮时执行的函数
    def click_button2():
        got_foreign_data()
        messagebox.showinfo(title='温馨提示', message='{}国外疫情数据.csv已生成，请在对应python路径查看'.format(
            datetime.datetime.now().strftime("%Y-%m-%d")))


    def click_button3():
        show_province_data()
        messagebox.showinfo(title='温馨提示', message='{}国内疫情新增数据图已生成'.format(
            datetime.datetime.now().strftime("%Y-%m-%d")))


    def click_button4():
        draw_map()
        messagebox.showinfo(title='温馨提示', message='疫情累计感染地图已生成')


    def click_button5():
        master = tk.Tk()
        master.title("搜索省市疫情数据")
        master.geometry('300x100+450+300')
        tk.Label(master, text="输入省名:").grid(row=0)
        tk.Label(master, text="输入市名:").grid(row=1)
        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e1.grid(row=0, column=1, padx=10, pady=5)
        e2.grid(row=1, column=1, padx=10, pady=5)

        def show__():
            province = e1.get()
            city = e2.get()
            if province == '':
                messagebox.showerror('错误', '省名不可为空')
            else:
                search_data = search_city(province, city)
                if not search_data:
                    messagebox.showerror(title='错误', message='对应省市名称存在错误', parent=master)
                else:
                    messagebox.showinfo(title='温馨提示',
                                        message='地区:{}\n新增本土:{:10}新增本土无症状:{}\n现有确诊:{:10}累计确诊:{}\n累计治愈:{:10}累计死亡:{}'.format(
                                            search_data['地区'], search_data['新增本土'], search_data['新增本土无症状'],
                                            search_data['现有确诊'], search_data['累计确诊'], search_data['累计治愈'],
                                            search_data['累计死亡']),
                                        parent=master)
                    e1.delete(0, "end")
                    e2.delete(0, "end")

        tk.Button(master, text="获取信息", width=10, command=show__).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Button(master, text="退出", width=10, command=master.destroy).grid(row=3, column=1, sticky='e', padx=10,
                                                                            pady=5)
        master.mainloop()


    def click_button6():
        draw_inner_line_chart()
        messagebox.showinfo(title='温馨提示', message='60天内疫情新增折线图已生成')


    def click_button7():
        draw_foreign_chart()
        messagebox.showinfo(title='温馨提示', message='今日国外新增top10直方图已生成')


    def click_button8():
        master = tk.Tk()
        master.title("请输入国外国家名称")
        master.geometry('300x70+450+300')
        tk.Label(master, text="搜索国家:").grid(row=0)
        e1 = tk.Entry(master)
        e1.grid(row=0, column=1, padx=10, pady=5)

        def show_():
            search_keyword = e1.get()
            if search_keyword == '':
                messagebox.showerror('错误', '输入不可为空')
            else:
                if foreign_pie_chart(search_keyword):
                    messagebox.showinfo(title='温馨提示', message='对应国外疫情饼图已完成', parent=master)
                    e1.delete(0, "end")
                else:
                    messagebox.showerror(title='错误', message='不存在该国家', parent=master)

        tk.Button(master, text="获取图像", width=10, command=show_).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Button(master, text="退出", width=10, command=master.destroy).grid(row=3, column=1, sticky='e', padx=10,
                                                                            pady=5)
        master.mainloop()


    def click_button9():
        get_SARS_data()
        messagebox.showinfo(title='温馨提示', message='SARS相关数据csv文件及数据图已生成')


    def click_button10():
        master = tk.Tk()
        master.title("搜索生成词云")
        master.geometry('300x100+450+300')
        tk.Label(master, text="搜索词:").grid(row=0)
        tk.Label(master, text="搜索页数:").grid(row=1)
        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e1.grid(row=0, column=1, padx=10, pady=5)
        e2.grid(row=1, column=1, padx=10, pady=5)

        def show():
            key_value = e1.get()
            numbers_value = e2.get()
            if key_value == '' or numbers_value == '':
                messagebox.showerror('错误', '输入不可为空')
            else:
                search_for_ciyun(key_value, eval(numbers_value))
                messagebox.showinfo(title='温馨提示', message='对应词云图已生成', parent=master)
                e1.delete(0, "end")
                e2.delete(0, "end")

        tk.Button(master, text="生成", width=10, command=show).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Button(master, text="退出", width=10, command=master.destroy).grid(row=3, column=1, sticky='e', padx=10, pady=5)
        master.mainloop()


    def click_button11():
        master = tk.Tk()
        master.title("搜索系统")
        master.geometry('300x100+450+300')
        tk.Label(master, text="搜索关键词:").grid(row=0)
        tk.Label(master, text="搜索页数:").grid(row=1)
        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e1.grid(row=0, column=1, padx=10, pady=5)
        e2.grid(row=1, column=1, padx=10, pady=5)

        def show():
            search_keyword = e1.get()
            max_page = e2.get()
            if search_keyword == '' or max_page == '':
                messagebox.showerror('错误', '输入不可为空')
            else:
                folder_path = os.getcwd() + '\\搜索结果'
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                result_file = folder_path + '\\{}.csv'.format(search_keyword)
                if os.path.exists(result_file):
                    os.remove(result_file)
                search(keyword=search_keyword, result_file=result_file, max_page=eval(max_page))
                messagebox.showinfo(title='温馨提示', message='对应搜索结果已生成csv文件', parent=master)
                e1.delete(0, "end")
                e2.delete(0, "end")

        tk.Button(master, text="获取信息", width=10, command=show).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Button(master, text="退出", width=10, command=master.destroy).grid(row=3, column=1, sticky='e', padx=10, pady=5)
        master.mainloop()


    tk.Button(window, text='更新今日国内疫情数据', bg='#7CCD7C', width=50, height=2,
              command=click_button1).pack()
    tk.Button(window, text='更新今日国外疫情数据', bg='#7CCD7C', width=50, height=2,
              command=click_button2).pack()
    tk.Button(window, text='生成国内今日新增直方图(使用前请先更新国内疫情数据)', bg='#7CCD7C', width=50, height=2,
              command=click_button3).pack()
    tk.Button(window, text='生成国内疫情累计感染人数地图(使用前请先更新国内疫情数据)', bg='#7CCD7C', width=50,
              height=2,
              command=click_button4).pack()
    tk.Button(window, text='查询市级新冠疫情数据', bg='#7CCD7C', width=50,
              height=2,
              command=click_button5).pack()
    tk.Button(window, text='生成国内近60天新增折线图', bg='#7CCD7C', width=50, height=2,
              command=click_button6).pack()
    tk.Button(window, text='生成国外top10新增直方图(使用前请先更新今日国外疫情数据)', bg='#7CCD7C', width=50, height=2,
              command=click_button7).pack()
    tk.Button(window, text='生成国外新冠治愈、死亡、目前确诊人数饼图', bg='#7CCD7C', width=50, height=2,
              command=click_button8).pack()
    tk.Button(window, text='获取SARS相关数据及其数据图', bg='#7CCD7C', width=50, height=2, command=click_button9).pack()
    tk.Button(window, text='爬取百度知道生成相关词云图(等待时间较长)', bg='#7CCD7C', width=50, height=2, command=click_button10).pack()
    tk.Button(window, text='搜索相关信息', bg='#7CCD7C', width=50, height=2, command=click_button11).pack()
    # 显示窗口
    window.mainloop()

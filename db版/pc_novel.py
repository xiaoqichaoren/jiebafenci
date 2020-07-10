import os
import re
import requests
import sqlite3
from bs4 import BeautifulSoup


class PC:
    __url = os.getcwd()+'\\database\\实训.db'

    def __init__(self, url):
        self.__con = sqlite3.connect(PC.__url)
        self.__cur = self.__con.cursor()

        self.html = requests.get(url+'#Catalog').text
        self.soup = BeautifulSoup(self.html, 'html.parser')

        self.name = self.GetName()  # 小说的书名

        self.lis = self.GetUrls()   # 每一章的url的列表

        self.SaveDB()   # 存储在数据库中

    def close(self):
        self.__con.commit()
        self.__cur.close()
        self.__con.close()

    def GetName(self):
        book = re.findall('<em>(.*?)</em>', self.html)[0]
        return book

    def GetUrls(self):
        hrefs = self.soup.find_all('a', href=re.compile('chapter'))
        urls = []
        [urls.append(i.get('href')) for i in hrefs if i.get('href') not in urls]    # 带有href的，即为正确的url地址。去重
        return urls

    def SaveDB(self):
        self.__cur.execute('delete from novel')     # 先清空表
        for i in self.lis:
            html = requests.get('https:'+i).text
            title = re.findall('"content-wrap">(.*?)<', html)[0]
            passages = re.findall('>(.*?)<p', html)     # 得到一个本章所有段落的列表

            passage = ''
            for i in passages:
                passage += i    # 把列表拼接成字符串
            self.__cur.execute('insert into novel (title, passage) values (?,?)', (title, passage))     # 将本章作为一条新数据添加到表中
            print(title+'----已保存')
        self.close()


if __name__ == '__main__':
    test = PC('https://book.qidian.com/info/1017694591')

import os
import re
import requests
from bs4 import BeautifulSoup


class PC:
    def __init__(self, url, n=1):
        self.html = requests.get(url+'#Catalog').text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.name = self.GetName()
        self.lis = self.GetUrls()

        self.SaveTxt()

    def GetUrls(self):
        hrefs = self.soup.find_all('a', href=re.compile('chapter'))
        urls = []
        [urls.append(i.get('href')) for i in hrefs if i.get('href') not in urls]
        return urls

    def GetName(self):
        book = re.findall('<em>(.*?)</em>', self.html)[0]
        return book

    def SaveTxt(self):
        with open('{}\\novel\\{}.txt'.format(os.getcwd(), self.name), 'w+', encoding='utf-8') as f:
            f.close()
        for i in self.lis:
            html = requests.get('https:'+i).text
            title = re.findall('"content-wrap">(.*?)<', html)[0]
            passages = re.findall('>(.*?)<p', html)
            with open('{}\\novel\\{}.txt'.format(os.getcwd(), self.name), 'a+', encoding='utf-8') as f:
                f.writelines(title+'\n')
                for passage in passages:
                    f.writelines(passage+'\n')
                print(title+'----已保存')


if __name__ == '__main__':
    test = PC('https://book.qidian.com/info/1017694591')

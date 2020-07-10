from pc_novel import PC
from jieba_novel import JIEBA

if __name__ == '__main__':
    url = 'https://book.qidian.com/info/1017694591'
    down = PC(url)  # 爬取小说
    cut = JIEBA(down.name)  # 分析小说结构

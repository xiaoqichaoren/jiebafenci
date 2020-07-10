import sqlite3
import jieba
import jieba.posseg as poss
import os


class JIEBA:
    jieba.load_userdict(os.getcwd()+'\\dict\\dict.txt')  # 加载字典
    __url = os.getcwd()+'\\database\\实训.db'

    def __init__(self, name):
        self.__con = sqlite3.connect(JIEBA.__url)
        self.__cur = self.__con.cursor()

        self.name = name
        self.nr_lis_lines = self.getnrll()  # 每行词性为nr的词的(列表的列表)
        self.nr_dict = self.getnrd()   # 所有nr的字典
        self.relation_dict = self.getrd()     # 关系字典

        self.GetNode()
        self.GetEdge()

    def close(self):
        self.__con.commit()
        self.__cur.close()
        self.__con.close()

    def getnrll(self, nr_lis_lines=[]):
        # 生成nr_lis_lines
        sql_passage = self.__cur.execute('select passage from novel')
        passage_list = list(sql_passage)
        line_list = []
        for i in passage_list:
            line_list += i[0].split()
        for i in line_list:     # 每一段的列表
            nr_lis_lines.append([])
            for j in poss.cut(i):
                if j.flag == 'znr':
                    nr_lis_lines[-1].append(j.word)
        self.close()
        nr_lis_lines = [x for x in nr_lis_lines if x != []]  # 去掉空列表
        return nr_lis_lines     # 返回每行的nr

    def getnrd(self, nr_dict={}):
        # 生成nr_dict
        for lis_line in self.nr_lis_lines:
            for nr in lis_line:
                if nr not in nr_dict:
                    nr_dict[nr] = 0
                nr_dict[nr] += 1
        return nr_dict

    def getrd(self, relation_dict={}):
        # 生成relation_dict
        for nr_line in self.nr_lis_lines:
            for nr1 in nr_line:
                for nr2 in nr_line:
                    if nr1 == nr2:
                        continue
                    if nr1 not in relation_dict:
                        relation_dict[nr1] = {}
                    if nr2 not in relation_dict[nr1]:
                        relation_dict[nr1][nr2] = 1
                    relation_dict[nr1][nr2] += 1
        return relation_dict

    def GetNode(self):  # 生成node
        with open('{}\\csv\\{}_node.csv'.format(os.getcwd(), self.name), 'w+', encoding='utf-8') as f:
            f.writelines('Id,Label,Weight\n')
            for i in self.nr_dict:
                if self.nr_dict[i] > 1:
                    f.writelines('{},{},{}\n'.format(i, i, self.nr_dict[i]))
        print('node已识别')

    def GetEdge(self):  # 生成edge
        with open('{}\\csv\\{}_edge.csv'.format(os.getcwd(), self.name), 'w+', encoding='utf-8') as f:
            f.writelines('Source,Target,Weight\n')
            for i in self.relation_dict:
                for j in self.relation_dict[i]:
                    if self.relation_dict[i][j] > 1:
                        f.writelines('{},{},{}\n'.format(i, j, self.relation_dict[i][j]))
        print('edge已识别')


if __name__ == '__main__':
    a = JIEBA('超品命师')

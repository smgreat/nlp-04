import  random
import re
import pandas as pd
from collections import Counter
import jieba
###################################################################
simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>  蓝色的 | 好看的 | 小小的
"""
human = """
human = 自己 寻找 活动
自己 = 我 | 俺 | 我们 
寻找 = 找找 | 想找点 
活动 = 乐子 | 玩的
"""
host = """
host = 寒暄 报数 询问 业务相关 结尾 
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = null
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？
"""
programmingprogramm  = """
stmt => if_exp | while_exp | assignment 
assignment => var = var
if_exp => if ( var ) { /n .... stmt }
while_exp=> while ( var ) { /n .... stmt }
var => chars number
chars => char | char char
char => student | name | info  | database | course
number => 1 | 2 | 3
"""
##################################################################
# def adj():
#     return random.choice('蓝色的 | 好看的 | 小小的'.split('|')).split()[0]
# def adj_star():
#     return random.choice([lambda :'',lambda :adj()+adj_star()])()
def create_grammar(grammar_str,split='=>',line_split='\n'):
    grammar={}
    for line in grammar_str.split(line_split):
        if not line.split():continue
        else:
            exp,stmt=line.split(split)
            grammar[exp.strip()]=[s.split() for s in stmt.split('|')]
    return grammar
choice=random.choice
def generate(gram,target):
    if target not in gram:return target#终止符
    expand=[generate(gram,t) for t in choice(gram[target])]
    #print(expand)
    return ''.join([e if e!='/n'else '\n' for e in expand if e!='null'])

# exzample_grammar=create_grammar(simple_grammar,split='=>')
# print(exzample_grammar)
# for i in range(5):
#     sentence=generate(gram=exzample_grammar,target='sentence')
#     print(sentence)

######################计算生成的句子的概率
filename='H:/资料/NLP&CV/nlp/lesson1/sqlResult_1558435.csv'
content=pd.read_csv(filename,encoding='gb18030',engine='python')

#['id', 'author', 'source', 'content', 'feature', 'title', 'url']
articles=content['content'].tolist()
#print(articles[0])
#print(len(articles))
#89611
def token(string):
    #获得中文字符串
    return re.findall('\w+',string)
with_jieba_cut=Counter(jieba.cut(articles[0]))
#print(with_jieba_cut.most_common()[:10])
#print(''.join(token(articles[0])))
articles_clean=[''.join(token(str(a))) for  a in articles]
#print(len(articles_clean))
#89611
# with open('article_9k.txt','w')as f:
#     for a in articles_clean:
#         f.write(a+'\n')
def cut(string): return list(jieba.cut(string))
TOKEN=[]
for i,line in enumerate((open('article_9k.txt'))):
    if i%100==0:    print(i)
    if i>1000: break
    TOKEN+=cut(line)
wordscount=Counter(TOKEN)
print(wordscount['我们'])
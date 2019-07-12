import  random
import re
import pandas as pd
from collections import Counter
import jieba
from functools import reduce
from  operator import add, mul
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
    return ''.join([e if e!='/n'else '\n' for e in expand if e!='null'])

# exzample_grammar=create_grammar(simple_grammar,split='=>')
# print(exzample_grammar)
# for i in range(5):
#     sentence=generate(gram=exzample_grammar,target='sentence')
#     print(sentence)

######################计算生成的句子的概率

def generate_article_txt(filename):
    content = pd.read_csv(filename, encoding='gb18030', engine='python')
    # ['id', 'author', 'source', 'content', 'feature', 'title', 'url']   ,row is :89611
    articles = content['content'].tolist()
    articles_clean = [''.join(token(str(a))) for a in articles]
    with open('article_9k.txt', 'w')as f:
        for a in articles_clean:
            f.write(a + '\n')

def token(string):
    #获得中文字符串
    return re.findall('\w+',string)
def cut(string): return list(jieba.cut(string))
TOKEN=[]
for i,line in enumerate((open('article_9k.txt'))):
    if i%100==0:    print(i)
    if i>1000: break
    TOKEN+=cut(line)
words_count=Counter(TOKEN)
def prob_1(word):
    return words_count[word] / len(TOKEN)
print(words_count['我们'])
TOKEN = [str(t) for t in TOKEN]
TOKEN_2_GRAM = [''.join(TOKEN[i:i+2]) for i in range(len(TOKEN[:-2]))]
words_count_2 = Counter(TOKEN_2_GRAM)
def prob_1(word): return words_count[word] / len(TOKEN)
def prob_2(word1, word2):
    if word1 + word2 in words_count_2: return words_count_2[word1+word2] / len(TOKEN_2_GRAM)
    else:
        return 1 / len(TOKEN_2_GRAM)
def get_probablity(sentence):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probability = prob_2(word, next_)
        sentence_pro *= probability
    return sentence_pro
if __name__ == '__main__':
    #filename = 'H:/资料/NLP&CV/nlp/lesson1/sqlResult_1558435.csv'
    # articles=generate_article_txt(filename)
    exzample_grammar=create_grammar(host,split='=')
    for sen in [generate(gram=exzample_grammar, target='host') for i in range(10)]:
        print('sentence: {} with Prb: {}'.format(sen, get_probablity(sen)))


    #test
    # need_compared = [
    #     "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    #     "真事一只好看的小猫 真是一只好看的小猫",
    #     "今晚我去吃火锅 今晚火锅去吃我",
    #     "洋葱奶昔来一杯 养乐多绿来一杯"
    # ]
    # for s in need_compared:
    #     s1, s2 = s.split()
    #     p1, p2 = get_probablity(s1), get_probablity(s2)
    #     better = s1 if p1 > p2 else s2
    #     print('{} is more possible'.format(better))
    #     print('-' * 4 + ' {} with probility {}'.format(s1, p1))
    #     print('-' * 4 + ' {} with probility {}'.format(s2, p2))
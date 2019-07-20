from collections import defaultdict
from functools import wraps
from functools import lru_cache
import time
original_price = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 35]
price=defaultdict(int)
for i, p in enumerate(original_price):
    price[i + 1] = p
call_time_with_arg=defaultdict(int)
def get_call_time(f):
    @wraps(f)
    def wrap(n):
        global call_time_with_arg
        result=f(n)
        call_time_with_arg[(f.__name__,n)]+=1
        print('function called time is :{}'.format(call_time_with_arg[f.__name__,n]))
        return result
    return wrap
def call_time(f,arg):
    start=time.time()
    f(arg)
    print('usedtime is {}'.format(time.time()-start))


def memo(func):
    cache = {}
    @wraps(func)
    def _wrap(n): ## ? *args, **kwargs
        if n in cache: result = cache[n]
        else:
            result = func(n)
            cache[n] = result
        return result
    return _wrap
solution={}
@memo
def r(n):
    maxprice,split_point=max(
        [(price[n],0)]+[(r(i)+r(n-i),i) for i  in range(1,n)],key=lambda x :x[0]
    )
    solution[n]=(split_point,n-split_point)
    return maxprice


def parse_solution(target_length):
    left,right=solution[target_length]
    if left==0:
        return [right]
    else:
        return parse_solution(left)+parse_solution(right)
# print(r(36),solution)
#print(parse_solution(6))




#Edit  Distance
solution2={}
@lru_cache(maxsize=2**10)
def edit_distance(string1,string2):
    if len(string1)==0 :return len(string2)
    if len(string2)==0: return len(string1)
    tail_s1=string1[-1]
    tail_s2=string2[-1]

    #操作步长
    candidates=[
        (edit_distance(string1[:-1],string2)+1,'DEL {}'.format(tail_s1)),
        (edit_distance(string1,string2[:-1])+1,'ADD {}'.format(tail_s2)),
    ]

    if tail_s1==tail_s2:
        both_forward=(edit_distance(string1[:-1],string2[:-1])+0,'both forward')
    else:
        both_forward=(edit_distance(string1[:-1],string2[:-1])+1,'SUB {}=>{}'.format(tail_s1,tail_s2))
    candidates.append(both_forward)
    mindistance,operation=min(candidates,key=lambda x:x[0])
    solution2[(string1,string2)]=operation
    #print('solution2:',solution2)
    print(string1, string2, candidates)
    return mindistance
str1='ACD'
str2='SBTC'
edit_distance(str1, str2)
#print('solution2:',solution2)
stack=[]
sum=0

def get_parse(str1,str2,solution):
    global sum


    if str1=='' and str2!='':
        sum+=len(str1)
        stack.append('ADD {}'.format(str2))
    if str2=='' and str1!='':
        sum+=len(str2)
        stack.append('DEL {}'.format(str1))
    if str1=='' and str2=='':
        return
    else:
        op = solution[(str1, str2)]
        if op[:3]=='DEL':
            stack.append(op)
            str1=str1[:-1]
            sum+=1
            get_parse(str1, str2, solution)
        elif op[:3]=='ADD':
            stack.append('{} on the next location '.format(op))
            str2=str2[:-1]
            sum+=1
            get_parse(str1, str2, solution)
        elif op=='both forward':
            str1=str1[:-1]
            str2=str2[:-1]
            get_parse(str1, str2, solution)
        elif op[:3]=='SUB':
            stack.append(op)
            str1=str1[:-1]
            str2=str2[:-1]
            get_parse(str1,str2,solution)

get_parse(str1,str2,solution2)
print('the match from {} to {}'.format(str1,str2))
print(sum)
for i in range (len(stack)-1,-1,-1):
    print(stack[i])

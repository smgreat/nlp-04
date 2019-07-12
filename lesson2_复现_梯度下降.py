from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import random
import numpy as np
dataset=load_boston()
X,y=dataset['data'],dataset['target']
price=y
room_num=X[:,5]

plt.scatter(X[:,5],y)
plt.show()

def func(age,k,b):
    return k*age+b

def loss(y,yhat):
    #MAE
    #return np.mean(np.abs(y - yhat))
    #MSE
     return np.mean(np.square(y - yhat))
    #RMSE
    # return np.mean(np.sqrt(y - yhat))
loop_times=10000
losses=[]
learning_rate=1e-1
def derivate_k(y,y_hat,x):
    abs_values=[  1 if (y_i-yhat_i)>0 else -1 for  y_i,yhat_i  in zip(y,y_hat)   ]
    return np.mean([a*-x_i for a,x_i in zip(abs_values,x)])
def derivate_b(y, yhat):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]
    return np.mean([a * -1 for a in abs_values])

k_hat = random.random() * 20 - 10
b_hat = random.random() * 20 - 10
while loop_times>0:
    #求导数
    k_delta=-1*learning_rate*derivate_k(price,func(room_num,k_hat,b_hat),room_num)
    b_delta = -1 * learning_rate * derivate_b(price, func(room_num, k_hat, b_hat))
    k_hat += k_delta
    b_hat += b_delta
    estimated_price = func(room_num, k_hat, b_hat)
    error_rate = loss(y=price, yhat=estimated_price)
    print('loop == {}'.format(loop_times))
    print('f(age) = {} * age + {}, with error rate: {}'.format(k_hat, b_hat, error_rate))
    losses.append(error_rate)
    loop_times -= 1
plt.plot(range(len(losses)), losses)
plt.show()



# dataset = load_boston()
# X, y = dataset['data'], dataset['target']
# room_num = X[:, 5]
# price = y
# def func(age, k, b): return k * age + b
#
# def loss(y, yhat):
#     #return np.mean(np.abs(y - yhat))
#      return np.mean(np.square(y - yhat))
#     # return np.mean(np.sqrt(y - yhat))
#
# min_error_rate = float('inf')
# loop_times = 10000
# losses = []
#
# k_hat = random.random() * 20 - 10
# b_hat = random.random() * 20 - 10
#
#
#
# def derivate_k(y, yhat, x):
#     abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]
#     return np.mean([a * -x_i for a, x_i in zip(abs_values, x)])
#
# def derivate_b(y, yhat):
#     abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]
#     return np.mean([a * -1 for a in abs_values])
#
# learing_rate = 1e-1
# while loop_times > 0:
#
#     k_delta = -1 * learing_rate * derivate_k(price, func(room_num, k_hat, b_hat), room_num)
#     b_delta = -1 * learing_rate * derivate_b(price, func(room_num, k_hat, b_hat))
#
#     k_hat += k_delta
#     b_hat += b_delta
#     estimated_price = func(room_num, k_hat, b_hat)
#     error_rate = loss(y=price, yhat=estimated_price)
#
#     print('loop == {}'.format(loop_times))
#     print('f(age) = {} * age + {}, with error rate: {}'.format(k_hat, b_hat, error_rate))
#     losses.append(error_rate)
#     loop_times -= 1
#
#
# # plt.scatter(sub_age, sub_fare)
# # plt.plot(sub_age, func(sub_age, best_k, best_b), c='r')
# # plt.plot(sub_age, func(sub_age, k_hat, b_hat), c='r')
# # plt.show()
# plt.plot(range(len(losses)), losses)
# plt.show()
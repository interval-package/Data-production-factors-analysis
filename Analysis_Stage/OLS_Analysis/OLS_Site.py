import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# OLS 回归
nsample = 100
# x1 的值从 0 到 10 等差排列
x = np.linspace(0, 10, nsample)
# 在 array 上加入一列常项1。
X = sm.add_constant(x)
beta = np.array([1, 10])
e = np.random.normal(size=nsample)
y = np.dot(X, beta) + e
model = sm.OLS(y, X)
results = model.fit()
print(results.params)
print(results.summary())

y_fitted = results.fittedvalues
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, 'o', label='data')
ax.plot(x, y_fitted, 'r--.', label='OLS')
ax.legend(loc='best')
ax.axis((-0.05, 2, -1, 25))
plt.show()

# 高次模型的回归
nsample = 100
X = np.column_stack((x, x ** 2))
X = sm.add_constant(X)
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=nsample)
y = np.dot(X, beta) + e
model = sm.OLS(y, X)
results = model.fit()
print(results.params)
print(results.summary())

y_fitted = results.fittedvalues
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, 'o', label='data')
ax.plot(x, y_fitted, 'r--.', label='OLS')
ax.legend(loc='best')
ax.axis((-0.05, 2, -1, 25))
plt.show()

# 哑变量
nsample = 50
groups = np.zeros(nsample, int)
groups[20:40] = 1
groups[40:] = 2
dummy = sm.categorical(groups, drop=True)
x = np.linspace(0, 20, nsample)
X = np.column_stack((x, dummy))
X = sm.add_constant(X)
beta = [10, 1, 1, 3, 8]
e = np.random.normal(size=nsample)
y = np.dot(X, beta) + e
result = sm.OLS(y, X).fit()
print(result.summary())

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, 'o', label="data")
ax.plot(x, result.fittedvalues, 'r--.', label="OLS")
ax.legend(loc='best')
plt.show()

# data = \
#     get_price(
#         ['000001.XSHG', '399001.XSHE'],
#         start_date='2015-01-01', end_date='2016-01-01', frequency='daily',fields=['close'])['close']
# x_price = data['000001.XSHG'].values
# y_price = data['399001.XSHE'].values
#
# x_pct, y_pct = [], []
# for i in range(1, len(x_price)):
#     x_pct.append(x_price[i] / x_price[i - 1] - 1)
# for i in range(1, len(y_price)):
#     y_pct.append(y_price[i] / y_price[i - 1] - 1)
#
# x = np.array(x_pct)
# X = sm.add_constant(x)
# y = np.array(y_pct)
# results = sm.OLS(y, X).fit()

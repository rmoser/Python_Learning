# Showing how to use linear algebra to do regression
# Comparing vs polyfit results

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

df = pd.DataFrame()

# Synthesize data based on these coefficients
# y = mx + b
m = 0.5
b = 1

N = 10000
df['x'] = np.random.normal(size=N)
df['n'] = np.random.normal(size=N)
df['y'] = m * df.x + b + df.n

# Sorting makes plot easier later
df.sort_values('x', inplace=True)

# Create matrix with ones in column 0, and x-values in column 1
x = np.ones((N, 2))
x[:, 1] = df.x.values

# Row vector with y-values
y = df.y.values.reshape(N, 1)

# Show some sample values
# print("x: ", x[:20])
# print("y: ", y[:20])

# Use polyfit order=1 to get coefficients
# model returned is a tuple with (slope, offset)
model = np.polyfit(df.x, df.y, 1)
print("model: y = {}x + {}".format(model[0], model[1]))

# Now use linear algebra to do the same
B = np.dot(np.dot(np.linalg.inv(np.dot(x.T, x)), x.T), y)
print("Linalg: ", B)

plt.scatter(df.x, df.y, label="data", s=1)
plt.plot(df.x, df.x * model[0] + model[1], label="polyfit", color='red', linewidth=4)
plt.plot(df.x, x.dot(B), label="linear algebra", color='black')
# plt.scatter(df.x, 0.880914241898232 * df.x)
plt.legend()
plt.grid(True)
plt.show()

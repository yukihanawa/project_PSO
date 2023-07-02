#rosenbock関数
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# rosenbrock関数の定義 (N次元対応)
def rosenbrock(x):
    n = len(x)
    return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(n-1))

# xとyの値の範囲を設定 (2次元の例)
x = np.linspace(-2.048, 2.048, 100)
y = np.linspace(-2.048, 2.048, 100)

# グリッドを作成
X, Y = np.meshgrid(x, y)

# Zを計算 (2次元の例)
Z = np.array([[rosenbrock([xi, yi]) for xi, yi in zip(x_row, y_row)] for x_row, y_row in zip(X, Y)])

# 3Dプロットを作成
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# グラフのタイトルとラベルを設定
ax.set_title("Rosenbrock Function")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("f(X, Y)")

# カラーバーを追加
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

# グラフを表示
plt.show()

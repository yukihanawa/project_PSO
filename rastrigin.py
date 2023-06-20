import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Rastrigin関数の定義
def rastrigin(x, y, A=10):
    return 2 * A + x**2 - A * np.cos(2 * np.pi * x) + y**2 - A * np.cos(2 * np.pi * y)

# xとyの値の範囲を設定
x = np.linspace(-5.12, 5.12, 100)
y = np.linspace(-5.12, 5.12, 100)

# グリッドを作成
X, Y = np.meshgrid(x, y)
Z = rastrigin(X, Y)

# 3Dプロットを作成
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# グラフのタイトルとラベルを設定
ax.set_title("Rastrigin Function")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("f(X, Y)")

# カラーバーを追加
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

# グラフを表示
plt.show()

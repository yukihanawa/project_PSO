import numpy as np
import csv

def fitness(position, function_name):
    if function_name == "rastrigin":
        D = len(position)
        return D * 10 + np.sum(position ** 2 - 10 * np.cos(2 * np.pi * position))
    elif function_name == "rosenbrock":
        return np.sum(100.0 * (position[1:] - position[:-1]**2.0)**2.0 + (1 - position[:-1])**2.0)
    else:
        raise ValueError("Invalid function name")

# いくつかの座標をテスト
positions = [
    np.array([1, 2]),
    np.array([-1, 1]),
    np.array([0, -1])
]

# 関数の名前（"rastrigin"または"rosenbrock"）
function_name = "rosenbrock" # 例としてrastrigin関数を使用

# 結果を保存するためのリスト
results = []

# 各座標での関数の値を計算
for position in positions:
    value = fitness(position, function_name)
    # 結果をリストに追加
    results.append([position.tolist(), value])

# 結果をCSVファイルに書き込む
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # ヘッダーを書き込む
    writer.writerow(["Position", "Value"])
    # 結果を書き込む
    writer.writerows(results)

import pandas as pd
import glob
import numpy as np

# CSVファイルが格納されているディレクトリ
directory_path = 'rastrigin' # 例: '/path/to/your/csv/files'

# CSVファイルを検索
csv_files = glob.glob(f"{directory_path}/*.csv")

# 各CSVファイルを読み込む
dataframes = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    dataframes.append(df)

# 全てのデータフレームを結合 (iterationごとに)
merged_df = pd.concat(dataframes).groupby('iteration').agg({'g_best': ['mean', 'std']}).reset_index()

# 結果を新しいCSVファイルに保存
merged_df.to_csv('output.csv', index=False)

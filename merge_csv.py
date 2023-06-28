import pandas as pd
import glob
import numpy as np
def make_csv():
    function_name = ["rastrigin", "rosenbrock"]

    for function in function_name:
        # CSVファイルが格納されているディレクトリ
        directory_path = function

        csv_files = glob.glob(f"{directory_path}/*.csv")

        # 各CSVファイルを読み込む
        dataframes = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            # ファイル名を新しい列として追加
            df['source'] = csv_file.split('/')[-1]  # ファイル名のみを取得
            dataframes.append(df)

        # 全てのデータフレームを結合
        merged_df = pd.concat(dataframes)

        # 各ファイルのg_bestデータを別の列にし、平均と標準偏差も計算
        output_df = pd.pivot_table(merged_df, values='gbest_fitness', index='iteration', columns='source', aggfunc=np.mean)
        output_df['中央値'] = merged_df.groupby('iteration')['gbest_fitness'].median()
        output_df['平均値'] = merged_df.groupby('iteration')['gbest_fitness'].mean()
        output_df['標準偏差'] = merged_df.groupby('iteration')['gbest_fitness'].std()

        # 結果を新しいCSVファイルに保存
        output_df.to_csv(f'{function}_output.csv')

import os
import pandas as pd

function = {"rastrigin", "rosenbrock"}

for fun in function:
    # プログラムと同じディレクトリを指定
    directory = os.path.dirname(os.path.realpath(__file__))

    # 新しいExcelファイルを作成
    excel_writer = pd.ExcelWriter(f'output_{fun}.xlsx', engine='openpyxl')

    # 中央値、平均値、標準偏差のデータを格納するためのリスト
    medians = []
    means = []
    std_devs = []

    # ディレクトリ内のCSVファイルをループで処理
    for filename in os.listdir(directory):
        # ファイル名に特定の文字列が含まれているかチェック
        if fun in filename and filename.endswith('.csv'):
            # CSVファイルを読み込む
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)
            
            # DataFrameをExcelの新しいシートに書き込む
            data.to_excel(excel_writer, sheet_name=os.path.splitext(filename)[0], index=False)
            
            # 中央値, 平均値, 標準偏差をリストに追加
            medians.append(data['中央値'].rename(f'中央値_{filename}'))
            means.append(data['平均値'].rename(f'平均値_{filename}'))
            std_devs.append(data['標準偏差'].rename(f'標準偏差_{filename}'))

    # 中央値、平均値、標準偏差の順に連結
    summary_data = pd.concat([pd.DataFrame(data) for data in medians + means + std_devs], axis=1)
    summary_data.insert(0, 'iteration', data['iteration'])

    # サマリーを別のシートとして追加
    summary_data.to_excel(excel_writer, sheet_name='summary', index=False)

    # Excelファイルを保存
    excel_writer.save()

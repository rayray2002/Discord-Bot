import pandas as pd
import glob

df_new = pd.read_csv('./save_csv/popularity.csv')

for file in glob.iglob('./save_csv/' + '**/*' + '.csv', recursive=True):
    if str(file) == './save_csv/popularity.csv':
        continue
    print(file)
    df_old = pd.read_csv(file)
    df_old['流水號'] = df_old['流水號'].fillna(0).astype(int)
    # print(df_old.head())

    df_new = df_new.astype(int)

    df = pd.merge(df_old, df_new, on='流水號', how='left')
    df = df.drop_duplicates(subset=['流水號'], keep='last')
    print(df)
    file_name = file.split('/')[-1]
    df = df.sort_values(by=['登記人數'], ascending=False)
    df.to_csv(f'./new_csv/{file_name}', encoding='utf-8-sig', index=False)

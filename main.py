import pandas as pd
# class Game:  # Class for running the game
#     @staticmethod
#     def get_csv_data_to_dict(source):
#         df = pd.read_csv(source, encoding='utf-8-sig', header=0)
#         df_rows = df.to_dict(orient='records')
#
#
#
#
#     item_data = get_csv_data_to_dict('items.csv')
#     monster_data = get_csv_data_to_dict('monsters.csv')

hi_df = pd.read_csv('tiles.csv')

key = hi_df.columns[0]
key_name_type = key.split('/')

hi_df_rows = hi_df.to_dict(orient='records')

hi_dict = {}

for h in hi_df_rows:
    new_key = eval(key_name_type[1] + '(' + h[key] + ')')

    value = {}

    for (k, v) in h.items():
        if k != key:
            k_name_type = k.split('/')

            new_value = None if pd.isna(v) else eval(k_name_type[1] + '(' + v + ')')
            value[k_name_type[0]] = new_value


    hi_dict[new_key] = value

print(hi_dict)
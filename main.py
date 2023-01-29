import pandas as pd

class Game:  # Class for running the game
    @staticmethod
    def convert_correct_data_type(string: str, data_type: str):
        if string[0] == '"' and string[-1] == '"':
            string = string[1:-1]

        if data_type in ['list', 'tuple']:
            corrected_data_type = eval(data_type + '(' + string + ')')

        else:
            corrected_data_type = eval(data_type + '(' + '"' + string + '"' + ')')

        return corrected_data_type


    @staticmethod
    def csv_to_dict_keys_unique_column(source, unique_column_index):
        df = pd.read_csv(source).astype(str)

        key_column_head = df.columns[unique_column_index]
        key_name_type = key_column_head.split('/')

        df_rows = df.to_dict(orient='records')

        hi_dict = {}

        for row in df_rows:
            new_key_str = row[key_column_head]

            new_key = Game.convert_correct_data_type(new_key_str, key_name_type[1])

            new_value = {}

            for (k, v) in row.items():
                if k != key_column_head:
                    k_name_type = k.split('/')

                    corrected_value = None if pd.isna(v) else Game.convert_correct_data_type(v, k_name_type[1])

                    new_value[k_name_type[0]] = corrected_value

            hi_dict[new_key] = new_value

        return hi_dict


print(type(Game.csv_to_dict_keys_unique_column('tiles.csv', 0)[(0,1)]['items']))


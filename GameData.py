import pandas as pd

class GameData:  # Class for running the game
    @staticmethod
    def convert_correct_data_type(string: str, data_type: str):
        if string == 'nan':
            return None

        if string[0] == '"' and string[-1] == '"':
            string = string[1:-1]

        if data_type in ['list', 'tuple']:
            corrected_data_type = eval(data_type + '(' + string + ')')
        else:
            corrected_data_type = eval(data_type + '(' + '"' + string + '"' + ')')

        return corrected_data_type

    @staticmethod
    def csv_to_dict_keys_unique_column(source: str, unique_column_index: int) -> dict:
        df = pd.read_csv(source).astype(str)

        key_column_head = df.columns[unique_column_index]
        key_name_type = key_column_head.split('/')

        df_rows = df.to_dict(orient='records')

        df_dict = {}

        for row in df_rows:
            new_key_str = row[key_column_head]

            new_key = GameData.convert_correct_data_type(new_key_str, key_name_type[1])

            new_value = {}

            for (k, v) in row.items():
                k_name_type = k.split('/')

                corrected_value = None if pd.isna(v) else GameData.convert_correct_data_type(v, k_name_type[1])
                new_value[k_name_type[0]] = corrected_value

            df_dict[new_key] = new_value

        return df_dict

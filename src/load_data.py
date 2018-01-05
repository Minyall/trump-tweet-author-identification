import pandas as pd


def main():
    pass


def load_json_list(list):
    '''
    takes a list of json files, loads them, and concatenates them
    INPUT: a list of json files
    OUTPUT: a single concatenated DataFrame
    '''

    files = []
    for file in list:
        df = pd.read_json(file)
        files.append(df)
    return pd.concat(files)


def apply_date_mask(df, date_column, start_date, end_date):
    '''
    applies mask to a df to include only dates within the given date range
    INPUT: a DataFrame, the name of the datetime column, start and end dates
    OUTPUT: a DataFrame with a datetime index, sorted by datetime
    '''

    mask = (df[date_column] > start_date) & (df[date_column] <= end_date)
    return df.loc[mask]


def sort_by_date(df, date_column):
    '''
    takes a DataFrame with a column in datetime format and sorts by date_column
    INPUT: a DataFrame and the name of a column in datetime format
    OUTPUT: a DataFrame with a datetime index
    '''

    sorted_data = df.sort_values(date_column)
    data = sorted_data.set_index(date_column)
    return data


if __name__ == '__main__':

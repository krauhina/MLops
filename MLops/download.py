import pandas as pd
from sklearn.preprocessing import OrdinalEncoder


def download_data():
    return pd.read_csv("new_car_price", index_col=0)


def clear_data(file_name):
    data = pd.read_csv(file_name)

    df = data.copy()
    cat_columns = ['fueltype', 'carbody', 'drivewheel', 'CarName']

    ordinal = OrdinalEncoder()
    ordinal.fit(df[cat_columns])

    Ordinal_encoded = ordinal.transform(df[cat_columns])
    df_ordinal = pd.DataFrame(Ordinal_encoded, columns=cat_columns)
    df[cat_columns] = df_ordinal[cat_columns]

    # удаление пропусков
    df = df.dropna()

    df.to_csv('result_dataset.csv')
    return True


download_data()
clear_data("new_car_price.csv")
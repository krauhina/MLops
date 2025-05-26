import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from train_model import train


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


dag_cars = DAG(
    dag_id="train_pipeline",
    start_date=datetime(2025, 5, 26),
    concurrency=4,
    schedule_interval=timedelta(minutes=5),
    #    schedule="@hourly",
    max_active_runs=1,
    catchup=False,
)

download_task = PythonOperator(python_callable=download_data, task_id="download_cars", dag=dag_cars)
clear_task = PythonOperator(python_callable=clear_data, task_id="clear_cars", dag=dag_cars)
train_task = PythonOperator(python_callable=train, task_id="train_cars", dag=dag_cars)

download_task >> clear_task >> train_task
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from datetime import datetime
from sklearn.datasets import load_iris
import pandas as pd
import logging

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False,
    'params': {
        # tolérance maximale sur la différence de moyenne/variance
        'tol_mean': 0.01,
        'tol_var': 0.01
    }
}

# Valeurs de référence pour Iris (calculées a priori)
REFERENCE_STATS = {
    'sepal length (cm)': {'mean': 5.843333333333334, 'var': 0.6856935123042506},
    'sepal width (cm)':  {'mean': 3.054     , 'var': 0.18997941834451923},
    'petal length (cm)': {'mean': 3.758666666666666, 'var': 3.116277845316228},
    'petal width (cm)':  {'mean': 1.1986666666666668, 'var': 0.5810063186813187},
}

def load_data(**context):
    iris = load_iris(as_frame=True)
    df = iris.frame
    # push DataFrame dans XCom pour usage ultérieur
    context['ti'].xcom_push(key='df', value=df.to_json())
    return True

def compute_stats(**context):
    # récupère le DataFrame depuis XCom
    df_json = context['ti'].xcom_pull(key='df')
    df = pd.read_json(df_json)
    stats = {}
    for col in iris.feature_names:
        stats[col] = {
            'mean': df[col].mean(),
            'var': df[col].var(ddof=0)
        }
    context['ti'].xcom_push(key='stats', value=stats)
    return stats

def validate_stats(**context):
    params = context['params']
    stats = context['ti'].xcom_pull(key='stats')
    errors = []
    for col, vals in stats.items():
        ref = REFERENCE_STATS[col]
        if abs(vals['mean'] - ref['mean']) > params['tol_mean']:
            errors.append(f"{col} mean diff {abs(vals['mean'] - ref['mean']):.4f}")
        if abs(vals['var'] - ref['var']) > params['tol_var']:
            errors.append(f"{col} var diff {abs(vals['var'] - ref['var']):.4f}")
    if errors:
        logging.error("Validation failed:\n" + "\n".join(errors))
        raise AirflowException("Données non conformes aux statistiques de référence")
    logging.info("Validation OK. Statistiques dans la tolérance.")
    return True

with DAG(
    dag_id='validation_dag',
    default_args=default_args,
    schedule_interval=None,
    description='Validation des stats moyennes/variance',
    tags=['validation']
) as dag:

    t1 = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True
    )

    t2 = PythonOperator(
        task_id='compute_stats',
        python_callable=compute_stats,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id='validate_stats',
        python_callable=validate_stats,
        provide_context=True
    )

    t1 >> t2 >> t3

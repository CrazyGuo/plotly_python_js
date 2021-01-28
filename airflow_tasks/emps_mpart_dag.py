from datetime import datetime
import os

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

#docker voulme location: /home/wuzlxadmin/airflow_server/airflow_dags  -->  /usr/local/airflow/dags
PYTHON_TARGET_File = "/usr/local/airflow/dags" + "/invoked_files/emps_mpart_items.py"

default_args = {
    "owner": "huanhuan.guo",
    "start_date": datetime(2021, 1, 26)
}

dag = DAG("eMPS_Mpart_Items", 
        description="Get mpart items from baan, insert to FlexPsApp.dbo.FlexMpsMpartItems",
        default_args=default_args, 
        schedule_interval='30 06 * * *')

def invoke_python_file():
    cmmd = "%s %s" % ("python", PYTHON_TARGET_File)
    os.system(cmmd)

t1 = PythonOperator(task_id="emps_mpart_item_task", python_callable=invoke_python_file, retries=0, dag=dag)
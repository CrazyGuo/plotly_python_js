import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime,Float, Integer, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
BATCH_INSERT_COUNT = 500


class FlexMpsMpartItem(Base):
    __tablename__ = 'FlexMpsMpartItems'

    id = Column(Integer, primary_key=True, index=True)
    Item = Column(String(20))
    CreatedBy = Column(Integer, default=1)
    CreatedTime = Column(DateTime, default=datetime.datetime.utcnow)
    UpdatedBy = Column(Integer, default=1)
    UpdatedTime = Column(DateTime, default=datetime.datetime.utcnow)


def get_oracle_data():
    db_engine = create_engine('oracle://user:password@ip:port/db', encoding="utf-8", max_identifier_length=30)
    sql = """
                select trim(A.item) as item
                from bo_read898.tcibd001 A
                where A.kitm = '2'
                and (trim(A.item) not like 'HPM%'
                and trim(A.item) not like 'DEL%'
                and trim(A.item) not like 'LNV%')
                and (A.csig = 'IAI' or A.csig = '   ' or A.csig = 'CAH')
    """

    connection = db_engine.connect()
    result = connection.execute(sql)
    return result

def insert_to_mssql(data_list):
    db_engine = create_engine('mssql+pymssql://gm:flex@gmwz@10.201.152.22/FlexPSApp', encoding="utf-8")
    db_session = sessionmaker(bind=db_engine)
    session = db_session() 

    truncate_table_sql = "truncate table FlexMpsMpartItems"
    session.execute(truncate_table_sql, params={})

    length = 0
    for row in data_list:
        item = FlexMpsMpartItem(Item=row['item'])
        session.add(item)
        length += 1

        if length == BATCH_INSERT_COUNT:
            session.flush()
            session.commit()
            length = 0
    if length > 0 :
        session.flush()
        session.commit() 
    session.close() 

def task_job():
    data_list = get_oracle_data()
    insert_to_mssql(data_list)

if __name__ == '__main__':
    task_job()
else:
    task_job()
import sys, os
import fileinput
import datetime, time
import configparser
import traceback
from dateutil.parser import parse

import pymssql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, DateTime,BigInteger,Text, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#pywin32 service
import servicemanager
import win32event
import win32service
import win32serviceutil
import win32timezone

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class IISLog(Base):
    __tablename__ = "iislog"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    time = Column(String(20), index=True)
    s_ip = Column(String(20), index=True)
    cs_method = Column(String(10), index=True)
    cs_uri_stem = Column(String(500))
    cs_uri_query = Column(Text)
    s_port = Column(Integer)
    cs_username = Column(String(20))
    c_ip = Column(String(20), index=True)
    cs_user_agent = Column(String(500))
    sc_status = Column(String(500))
    sc_substatus = Column(Integer)
    sc_win32_status = Column(Integer)
    sc_bytes = Column(BigInteger)
    cs_bytes = Column(Integer)
    time_taken = Column(Integer, nullable=True)

def init_sqlalchemy(dbname='mssql+pymssql://gm:flex@gmwz@10.201.152.22/Test?charset=utf8'):
    global DBSession
    engine = create_engine(dbname)
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)


def read_log_file1(file_path):
    header = ['date', 'time', 's-ip', 'cs-method', 'cs-uri-stem', 'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(User-Agent)', 'sc-status', 'sc-substatus', 'sc-win32-status', 'sc-bytes', 'cs-bytes', 'time-taken']
    l = []
    count = 0
    for line in fileinput.input(file_path):
        if not line.startswith('#'):
            fields = line.split()
            d = dict(zip(header, fields))
            l.append(d)
            count += 1
        if len(l) == 500:
            batch_insert(l)
            l.clear()
    if len(l) > 0:
        batch_insert(l)
        l.clear()

def read_log_file(file_path):
    header = ['date', 'time', 's-ip', 'cs-method', 'cs-uri-stem', 'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(User-Agent)', 'sc-status', 'sc-substatus', 'sc-win32-status', 'sc-bytes', 'cs-bytes', 'time-taken']
    l = []
    count = 0
    
    with open(file_path,'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if line and not line.startswith('#'):
                fields = line.split()
                d = dict(zip(header, fields))
                l.append(d)
                count += 1
            if len(l) == 500:
                batch_insert(l)
                l.clear()
    if len(l) > 0:
        batch_insert(l)
        l.clear()


def batch_insert(data_list):
    log_list = []
    for data in data_list:
        log = IISLog(date=data['date'],time=data['time'],
        s_ip=data['s-ip'],cs_method=data['cs-method'],
        cs_uri_stem=data['cs-uri-stem'],cs_uri_query=data['cs-uri-query'],
        s_port=data['s-port'],cs_username=data['cs-username'],
        c_ip=data['c-ip'],cs_user_agent=data['cs(User-Agent)'],
        sc_status=data['sc-status'],sc_substatus=data['sc-substatus'],
        sc_win32_status=data['sc-win32-status'],sc_bytes=data['sc-bytes'],
        cs_bytes=data['cs-bytes'],time_taken=data.get('time-taken', 0),
        )
        DBSession.add(log)
    DBSession.flush()
    DBSession.commit()


def start_task(last_dict, log_dir):
    last_date = datetime.datetime.now() + datetime.timedelta(days=-1)
    target_date_format = "u_ex%s.log" % last_date.strftime("%y%m%d")
    file_path = os.path.join(log_dir, target_date_format)
    if target_date_format not in last_dict and os.path.exists(file_path):
        read_log_file(file_path)
        last_dict.add(target_date_format)


def read_config(base_path=None, filename='iis_log_parse_service.ini'):
    '''
    Reads the configuration file containing processes to spawn information
    '''
    if not base_path:
        exe_file = os.path.realpath(sys.executable)
        base_path = os.path.abspath(os.path.dirname(exe_file)) 
    config = configparser.ConfigParser()
    config.optionxform = str
    path = os.path.join(base_path, filename)
    config.read(path)
    return config['DEFAULT']


class ParseIISLogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ParseIISLogService"
    _svc_display_name_ = "ParseIISLogService"
    _svc_description_ = "parse iis log"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        self.iis_log_dir = None
        self.job_log_dir = None
        self.db = None
        self.last_dict = set()
        self.begin_time = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.prepare_task()
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            try:
                if self.check_can_start():
                    start_task(self.last_dict, self.iis_log_dir)
            except Exception as ex:
                tem_log(traceback.format_exc())
                self.write_log(traceback.format_exc())
            # hang for 10 minute or until service is stopped - whichever comes first
            rc = win32event.WaitForSingleObject(self.hWaitStop, 10 * 60 * 1000)

    def prepare_task(self):
        try:
            config = read_config()
            self.iis_log_dir = config["iis_log_dir"]
            self.job_log_dir = config["job_log_dir"]
            self.db = config["db"]
            self.begin_time = config["begin_time"]
            self.write_log("read config success.")
            init_sqlalchemy(dbname=self.db)
            self.write_log("init db success.")
        except Exception as ex:
            tem_log(traceback.format_exc())
    
    def check_can_start(self,):
        now = datetime.datetime.now()
        target_time = now.strftime('%Y-%m-%d ') + self.begin_time
        if now > parse(target_time):
            return True
        else:
            return False


    def write_log(self, info):
        log_file = datetime.datetime.now().strftime("%y%m%d.log")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        file_path = os.path.join(self.job_log_dir, log_file)
        with open(file_path, 'a') as f:
            content = "%s\r\n%s\r\n" % (timestamp, info)
            f.write(content)

def tem_log(info):
    with open('D:\\IISLOG\\parseapp\\log\\temp.log', 'a') as f:
        content = "%s\r\n" % info
        f.write(content)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ParseIISLogService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ParseIISLogService)
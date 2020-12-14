import os
import datetime
import time
import configparser
import traceback

import serial
import serial.tools.list_ports

import pymysql
from sqlalchemy import Column, String, DateTime,Float, create_engine
from sqlalchemy.orm import sessionmaker

#pywin32 service
import servicemanager
import win32event
import win32service
import win32serviceutil
import win32timezone

last_time_upload = {}


class Communication():
    #初始化
    def __init__(self,com,bps,timeout, valid_cars, wait_write_interval, db, log_func):
        self.port = com
        self.bps = int(bps)
        self.timeout = float(timeout)
        
        self.valid_cars = [car for car in valid_cars.split(',') ]
        self.wait_write_interval = int(wait_write_interval)
        self.db = db
        self.log_func = log_func
        try:
            # 打开串口，并得到串口对象
             self.main_engine= serial.Serial(self.port,self.bps,timeout=self.timeout)
        except Exception as e:
            self.log_func(traceback.format_exc())

    # 打印设备基本信息
    def Print_Name(self):
        print(self.main_engine.name) #设备名字
        print(self.main_engine.port)#读或者写端口
        print(self.main_engine.baudrate)#波特率
        print(self.main_engine.bytesize)#字节大小
        print(self.main_engine.parity)#校验位
        print(self.main_engine.stopbits)#停止位
        print(self.main_engine.timeout)#读超时设置
        print(self.main_engine.writeTimeout)#写超时
        print(self.main_engine.xonxoff)#软件流控
        print(self.main_engine.rtscts)#软件流控
        print(self.main_engine.dsrdtr)#硬件流控
        print(self.main_engine.interCharTimeout)#字符间隔超时

    #打开串口
    def Open_Engine(self):
        self.main_engine.open()

    #关闭串口
    def Close_Engine(self):
        self.main_engine.close()
        print(self.main_engine.is_open)  # 检验串口是否打开

    # 打印可用串口列表
    @staticmethod
    def Print_Used_Com():
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)


    #接收指定大小的数据
    #从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def Read_Size(self,size):
        return self.main_engine.read(size=size)

    #接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def Read_Line(self):
        return self.main_engine.readline()

    #发数据
    def Send_data(self,data):
        self.main_engine.write(data)

    def Recive_data(self):
        # 循环接收数据，此为死循环，可用线程实现
        self.log_func("开始接收数据")
        while True:
            try:
                # 一个字节一个字节的接收
                count = self.main_engine.in_waiting
                l_data = []
                for i in range(count):
                    data = self.Read_Size(1)
                    if data:
                        str_data = "%s" % data.hex().upper()
                    else:
                        str_data = ''
                    #str_data = data
                    l_data.append(str_data)
                if len(l_data) > 0:
                    self.process_all_data(l_data)
                time.sleep(0.3)
            except Exception as e:
                self.log_func(traceback.format_exc())

    def process_all_data(self, data_list):
        length = len(data_list)
        group_len = 22
        group_count = length // group_len

        msg = ''.join(data_list)
        self.log_func("receive data: %s, group count: %d" % (msg, group_count))

        for group_index in range(group_count):
            start_index = group_index * group_len 
            end_index = (group_index + 1) * group_len 
            val_list = data_list[start_index:end_index]
            self.InsertToDB(val_list)

    def process_serial_data(self):
        try:
            # 一个字节一个字节的接收
            count = self.main_engine.in_waiting
            l_data = []
            for i in range(count):
                if i < 22: #只读取前22个字节
                    str_data = "%s" % self.Read_Size(1).hex().upper()
                    l_data.append(str_data)
                else:
                    self.Read_Size(1) #读取但不再分析
            if len(l_data) > 0:
                self.InsertToDB(l_data)
        except Exception as e:
            self.log_func(traceback.format_exc())


    def InsertToDB(self, data_list):
        data = ' '.join(data_list)
        if data_list[0]=='01' and data_list[1]=='16':
            car_no = ''.join(data_list[2:6])
            data_flag = ''.join(data_list[6:])
            end_flag = ''.join(data_list[-2:])
            upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            if car_no not in self.valid_cars or end_flag !='01FF':
                self.log_func('skip %s, car_no not configured or not end whith 01FF' % data)
            else:
                last_time = last_time_upload.get(car_no, None)
                diff_seconds = float("inf")
                if last_time:
                    diff_seconds = (datetime.datetime.now() - last_time).seconds
                if diff_seconds > self.wait_write_interval:
                    #记录最近一次的写入时间
                    last_time_upload[car_no] = datetime.datetime.now()

                    sql = '''insert into iccard(zgbAddr, data,uploadtime,actioncode,actiondesc)
                            VALUES(:car_no, :data_flag, :upload_time, '1', 'warehouse by python')
                    '''

                    # 初始化数据库连接:
                    engine = create_engine(self.db, encoding="utf-8")
                    # 创建DBSession类型:
                    session = sessionmaker(bind=engine)
                    # 创建Session:
                    session = session()
                    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
                    session.execute(sql, params={'car_no':car_no, 'data_flag':data_flag, 'upload_time':upload_time})
                    session.commit() 
                    self.log_func('insert %s success' % data)
                else:
                    self.log_func('skip %s, casue the in the interval.' % data)
        else:
            self.log_func('skip %s, cause not begin with 0116' % data)


def get_app_path():
    exe_file = os.path.realpath(sys.executable)
    base_path = os.path.abspath(os.path.dirname(exe_file)) 
    return base_path


def read_config(base_path=None, filename='etc.ini'):
    '''
    Reads the configuration file containing processes to spawn information
    '''
    if not base_path:
        base_path = get_app_path()
    config = configparser.ConfigParser()
    config.optionxform = str
    path = os.path.join(base_path, filename)
    config.read(path)
    return config['DEFAULT']


def print_log(info):
    print(info)


class ParseSerialService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ParseSerialService"
    _svc_display_name_ = "ParseSerialService"
    _svc_description_ = "parse serial etc"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        self.com_port = None
        self.bps = None
        self.timeout = None
        self.cars = None
        self.wait_write_interval = None
        self.db = None
        self.job_log_dir = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.prepare_task()
        engine = Communication(self.com_port, self.bps , self.timeout, self.cars, self.wait_write_interval, self.db, self.write_log)
        #rc = None
        #while rc != win32event.WAIT_OBJECT_0:
        try:
            #engine.process_serial_data()
            engine.Recive_data()
        except Exception as ex:
            self.write_log(traceback.format_exc())
        # hang for 0.3 minute or until service is stopped - whichever comes first
        #rc = win32event.WaitForSingleObject(self.hWaitStop, 0.3 * 60 * 1000)

    def prepare_task(self):
        try:
            config = read_config()
            self.com_port = config["com_port"]
            self.bps = config["bps"]
            self.timeout = config["timeout"]
            self.cars = config["cars"]
            self.wait_write_interval = config["wait_write_interval"]
            self.db = config["db"]
            self.job_log_dir = config["job_log_dir"]
            self.write_log("read config success.")
        except Exception as ex:
            self.write_log(traceback.format_exc())

    def write_log(self, info):
        log_file = datetime.datetime.now().strftime("%y%m%d.log")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        if self.job_log_dir:
            file_path = os.path.join(self.job_log_dir, log_file)
        else:
            file_path = os.path.join(get_app_path(), log_file)
        with open(file_path, 'a', encoding="utf-8") as f:
            content = "%s:%s\r\n" % (timestamp, info)
            f.write(content)


def main_service():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ParseSerialService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ParseSerialService)


def main_app():
    try:
        config = read_config()
        engine = Communication(config['com_port'], config['bps'] , config['timeout'], config['cars'], config['wait_write_interval'], config['db'], print_log)
        engine.Recive_data()
    except Exception as ex:
        print_log(traceback.format_exc())

if __name__ == '__main__':
    main_service()
    '''
    while True:
        is_service = True
        if is_service:
            main_service()
        else:
            main_app()
        time.sleep(0.5)
    '''
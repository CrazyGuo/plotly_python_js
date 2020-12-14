import os
import sys
import datetime
import time
import configparser
import traceback
import base64
#ftp
import ssl
from ftplib import FTP_TLS

#pywin32 service
import servicemanager
import win32event
import win32service
import win32serviceutil
import win32timezone

#连接IIS的问题解决
#https://stackoverflow.com/questions/55374840/python-ftplib-and-tls-issues-with-data-connection/55375191#55375191
#https://www.kodfor.com/Automating-file-transfer-via-FTP-over-TLS-using-Python
class iisFTP_TLS(FTP_TLS):
    ssl_version=ssl.PROTOCOL_TLS
    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        """Store a file in binary mode.  A new port is created for you.

        Args:
        cmd: A STOR command.
        fp: A file-like object with a read(num_bytes) method.
        blocksize: The maximum data size to read from fp and send over
            the connection at once.  [default: 8192]
        callback: An optional single parameter callable that is called on
            each block of data after it is sent.  [default: None]
        rest: Passed to transfercmd().  [default: None]

        Returns:
        The response code.
        """
        self.voidcmd('TYPE I')
        with self.transfercmd(cmd, rest) as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
            ## shutdown ssl layer
            #if _SSLSocket is not None and isinstance(conn, _SSLSocket):
            #   conn.unwrap()
        return self.voidresp()

def get_app_path():
    exe_file = os.path.realpath(sys.executable)
    base_path = os.path.abspath(os.path.dirname(exe_file)) 
    return base_path

def read_config(base_path=None, filename='ftp.ini'):
    '''
    Reads the configuration file containing processes to spawn information
    '''
    if not base_path:
        base_path = get_app_path()
        base_path = "C:\\Users\\wuzhuguo\\Desktop\\test"
    config = configparser.ConfigParser()
    config.optionxform = str
    path = os.path.join(base_path, filename)
    config.read(path)
    return config['DEFAULT']
 
def print_log(info):
        print(info)
 

class SSHManager:
    def __init__(self, host,port, usr, passwd, func):
        self._host = host
        self.port = int(port)
        self._usr = usr
        self._passwd = passwd
        self.log_func = func
        self.ftps = None
        self.ftp_connect_login()

    def ftp_connect_login(self):
        try:
            self.ftps = iisFTP_TLS()                         #设置变量
            self.ftps.set_debuglevel(2)
            self.ftps.set_pasv(False)
            self.ftps.connect(self._host, self.port)          #连接的ftp sever和端口
            
            # enable TLS
            self.ftps.login(self._usr, self._passwd)      #连接的用户名，密码
            self.ftps.prot_p()
            self.log_func("ftp connect and login success")
        except Exception as e:
            self.log_func(traceback.format_exc())
            raise RuntimeError("sftp connect failed [%s]" % str(e))
 
    def handle(block, p2):
        print(p2)

    def _upload_file(self, local_file, remote_file):
        is_success = True
        try:
            fp = open(local_file, "rb")
            res = self.ftps.storbinary('STOR {}'.format(remote_file), fp, callback=self.handle)
            if not res.startswith('226 Transfer complete'):
                print('Upload failed')
                print(res)
            else:
                is_success = True
        except Exception as e:
            self.log_func(traceback.format_exc())
            is_success = False
        return is_success


    def auto_upload(self, file_dir, ftp_path):
        target_list = []
        hash_name = {}
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.txt':  #目标文件
                    fi = os.path.join(root, file)
                    file_name = os.path.splitext(file)[0]  + ".bak"
                    local_renamed_file =  os.path.join(root, file_name)
                    hash_name[fi] = (local_renamed_file, file)

                    target_list.append(fi)

        self.ftps.cwd(ftp_path)
        success_list = []
        for local_file in target_list:
            file_info = hash_name[local_file]
            is_success = self._upload_file(local_file, file_info[1])
            if is_success:
                msg = "upload %s success" % local_file
                success_list.append((local_file, file_info[0]))
            else:
                msg = "upload %s fail" % local_file
            self.log_func(msg)

        self.close()

        for item in success_list:
            os.rename(item[0], item[1])
            log_msg = "%s --> %s" % item
            self.log_func(log_msg)
            
 
    def close(self):
        try:
            self.ftps.close()
        except Exception as e:
            self.log_func(traceback.format_exc())


class FtpUploadService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FtpUploadService"
    _svc_display_name_ = "FtpUploadService"
    _svc_description_ = "upload employee data to ftp"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.host = None
        self.port = None
        self.user = None
        self.pwd = None
        self.local_dir = None
        self.ftp_dir = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.prepare_task()
        
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            try:
                engine = SSHManager(self.host,self.port, self.user , self.pwd, self.write_log)
                engine.auto_upload(self.local_dir, self.ftp_dir)
            except Exception as ex:
                self.write_log(traceback.format_exc())
            # hang for 5 minute or until service is stopped - whichever comes first
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5 * 60 * 1000)

    def prepare_task(self):
        try:
            config = read_config()
            self.host = config["host"]
            self.port = config['port']
            self.user = config["user"]
            self.pwd = config["pwd"]
            self.local_dir = config["local_dir"]
            self.ftp_dir = config["ftp_dir"]
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
        with open(file_path, 'a') as f:
            content = "%s:%s\r\n" % (timestamp, info)
            f.write(content)


def main_service():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FtpUploadService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FtpUploadService)


def main_app():
    try:
        config = read_config()
        engine = SSHManager(config['host'], config['port'], config['user'] , config['pwd'], print_log)
        engine.auto_upload(config["local_dir"], config["ftp_dir"])
    except Exception as ex:
        print_log(traceback.format_exc())
        while True:
            print("...")
            time.sleep(10000)

if __name__ == '__main__':
    main_app()
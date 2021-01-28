import os, sys
import datetime
import time
import json
import configparser
import traceback

from selenium import webdriver
from selenium.webdriver.support.ui import Select#select类，下拉菜单使用
from selenium.webdriver.common.action_chains import ActionChains#鼠标操作包
from selenium.webdriver.support.wait import WebDriverWait#等待时间包，在限定时间内查找元素
from selenium.webdriver.common.keys import Keys

def get_app_path():
    exe_file = os.path.realpath(sys.executable)
    base_path = os.path.abspath(os.path.dirname(exe_file)) 
    return base_path


def read_config(base_path=None, filename='auto_delete.ini'):
    '''
    Reads the configuration file containing processes to spawn information
    '''
    if not base_path:
        base_path = get_app_path()
        #base_path = "C:\\Users\\wuzhuguo\\Desktop\\test\\auto"
    config = configparser.ConfigParser()
    config.optionxform = str
    path = os.path.join(base_path, filename)
    config.read(path)
    return config['DEFAULT']


def get_employees(file_path):
    result, done = [], False
    with open(file_path, encoding='utf8') as fd:
        while not done:
            employee = fd.readline()
            if employee:
                print(employee)
                result.append(employee.strip())
            else:
                done = True
    return result

def print_log(info):
    print(info)

class AutoDelete:
    def __init__(self, login, pwd, file_path, show_browser, driver_path):
        self.login_url = 'https://192.168.209.18/WPMS/'
        self.login = login
        self.pwd = pwd
        self.file_path = file_path
        self.show_browser = int(show_browser)
        self.chromeDriverPath = driver_path


    def start(self):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--start-maximized')
        option.add_argument('lang=zh_CN.UTF-8')
        if self.show_browser > 0 :
            pass
        else:
            option.add_argument('--headless') #浏览器不提供可视化页面.
        browser = webdriver.Chrome(chrome_options=option, executable_path=self.chromeDriverPath)
        browser.get(self.login_url)
        time.sleep(2)
        #登录操作
        browser.find_element_by_id('user-name').send_keys(self.login)
        browser.find_element_by_id('password').send_keys(self.pwd)
        browser.find_element_by_id('login-submit').click()
        time.sleep(1)
        #关闭对话框
        browser.find_element_by_xpath("//div[@class='ui_buttons']//input[@value='确定']").click()
        time.sleep(1)

        leave_employees = get_employees(self.file_path)
        self.delete_employee(browser, leave_employees)
        self.delete_card(browser, leave_employees)
        self.delete_employee_info(browser, leave_employees)


    def delete_employee(self, browser, employee_list):
        #点击菜单显示 门禁管理 部分
        men1 = browser.find_element_by_id("home-page")
        ActionChains(browser).move_to_element(men1).perform()#将鼠标放置到“业务导航”按钮上
        men2 = men1.find_element_by_xpath("//a[@name='一卡通应用']")
        ActionChains(browser).move_to_element(men2).perform()#将鼠标放置到“一卡通应用”按钮上
        men3 = men2.find_element_by_xpath("//a[@name='门禁管理']")
        men3.click()
        time.sleep(2)
        #iframe切换
        iframe = browser.find_element_by_xpath("//div[@id='system-content']//iframe[@id='iframe-101']")
        browser.switch_to_frame(iframe)
        #找到 按人授权 菜单并点击
        browser.find_element_by_xpath("//div[@id='accordion-west']//div[text()='按人授权']").click()
        time.sleep(2)

        #找到人员编号并查询
        employee_text = browser.find_element_by_id('accessAuth-personCode')
        serach_btn = browser.find_element_by_id('accessAuth-search-button')
        for employee_no in employee_list:
            employee_text.send_keys(Keys.CONTROL, 'a') #清空对话框
            employee_text.send_keys(employee_no)
            serach_btn.click()
            time.sleep(2)
            #查询表格 找到第一条的删除按钮
            table = browser.find_element_by_id("accessAuthInfo")
            try:
                span_node = table.find_element_by_xpath("//tbody/tr[1]//td[position()=last()-2]//span")
                if span_node.text == '已授权':
                    table.find_element_by_xpath("//tbody/tr[1]//td//a[@handle='delete']").click()
                else:
                    continue
            except Exception as e:
                employee_text = browser.find_element_by_id('accessAuth-personCode')
                serach_btn = browser.find_element_by_id('accessAuth-search-button')
                continue
            time.sleep(2)
            #确认删除对话框按钮
            browser.find_element_by_xpath("//div[@aria-describedby='delete-accesControlAuth']//span[text()='确定删除']").click()
            msg = "1:%s" % employee_no
            print(msg)
            time.sleep(10)
        #切换到主档 
        browser.switch_to.default_content()

    def delete_card(self, browser, employee_list):
        #点击菜单显示 人卡管理 部分
        men1 = browser.find_element_by_id("home-page")
        ActionChains(browser).move_to_element(men1).perform()#将鼠标放置到“业务导航”按钮上
        men2 = men1.find_element_by_xpath("//a[@name='一卡通应用']")
        ActionChains(browser).move_to_element(men2).perform()#将鼠标放置到“一卡通应用”按钮上
        men3 = men2.find_element_by_xpath("//a[@name='人卡管理']")
        men3.click()
        time.sleep(20)
        #iframe切换
        iframe = browser.find_element_by_xpath("//div[@id='system-content']//iframe[@id='iframe-108']")
        browser.switch_to_frame(iframe)
        #找到 卡片管理 菜单并点击
        browser.find_element_by_xpath("//div[@id='card-manage']").click()
        time.sleep(8)

        #找到人员编号并查询
        employee_text = browser.find_element_by_id('personCode-searchActive')
        serach_btn = browser.find_element_by_id('active-card-search-button')
        for employee_no in employee_list:
            employee_text.send_keys(Keys.CONTROL, 'a') #清空对话框
            employee_text.send_keys(employee_no)
            serach_btn.click()
            time.sleep(2)
            #查询表格 找到第一条的删除按钮
            table = browser.find_element_by_xpath("//div[@id='activeInfo_wrapper']//table[@id='activeInfo']")
            try:
                table.find_element_by_xpath("//tbody/tr[1]//td//a[@handle='return']").click()
            except Exception as e:
                employee_text = browser.find_element_by_id('personCode-searchActive')
                serach_btn = browser.find_element_by_id('active-card-search-button')
                continue
            time.sleep(2)
            #确认删除对话框按钮
            browser.find_element_by_xpath("//div[@aria-describedby='activeCard-return-dialog']//span[text()='确定']").click()
            msg = "2:%s" % employee_no
            print(msg)
            time.sleep(10)
        #切换到主档 
        browser.switch_to.default_content()
        
    def delete_employee_info(self, browser, employee_list):
        #iframe切换
        iframe = browser.find_element_by_xpath("//div[@id='system-content']//iframe[@id='iframe-108']")
        browser.switch_to_frame(iframe)
        #找到 人员管理 菜单并点击
        browser.find_element_by_xpath("//div[@name='person-manage']").click()
        time.sleep(8)
        #找到人员编号并查询
        cnt = browser.find_element_by_id('table-control-person')
        employee_text = cnt.find_element_by_id("personCode-search")
        serach_btn = cnt.find_element_by_id("person-search-button")
        for employee_no in employee_list:
            employee_text.send_keys(Keys.CONTROL, 'a') #清空对话框
            employee_text.send_keys(employee_no)
            serach_btn.click()
            time.sleep(3)
            #查询表格 找到第一条的删除按钮
            table = browser.find_element_by_xpath("//div[@id='userInfo_wrapper']//table[@id='userInfo']")
            try:
                table.find_element_by_xpath("//tbody/tr[1]//td//a[@handle='delete']").click()
            except Exception as e:
                employee_text = cnt.find_element_by_id("personCode-search")
                serach_btn = cnt.find_element_by_id("person-search-button")
                continue
            time.sleep(3)
            #确认删除对话框按钮
            browser.find_element_by_xpath("//div[@aria-describedby='delete-person']//span[text()='确定删除']").click()
            msg = "2:%s" % employee_no
            print(msg)
            time.sleep(10)        


def start_app():
    config = read_config()
    auto = AutoDelete(config['login'], config['pwd'] , config['file_path'], config['show_browser'], config['driver_path'])
    print("start")
    auto.start()
    print("end")

if __name__ == '__main__':
    try:
        start_app()
    except Exception as ex:
        print_log(traceback.format_exc())
    print("Fnished")
    time.sleep(1005)
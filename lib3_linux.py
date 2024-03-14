from selenium import webdriver
from time import sleep
import time
import threading
import random
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date, timedelta
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
dev = 1
url_global = 'https://libzwxt.ahnu.edu.cn/SeatWx/login.aspx?url=https%3a%2f%2flibzwxt.ahnu.edu.cn%2fSeatWx%2findex.aspx'
url_entry = 'https://libzwxt.ahnu.edu.cn/SeatWx/index.aspx'
url_seat = 'https://libzwxt.ahnu.edu.cn/SeatWx/Seat.aspx?'
classroom = ['0', '1', '1', '3', '3', '3', '3', '3']
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"


def loadtime():
    now_time = datetime.datetime.now()
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    return next_day,next_month,next_year,now_time

class Sele:
    def __init__(self, username, password, st1, st2, et1, et2, next, next_day, next_month, next_year):
        self.nexttime = str(
            datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 01:00:00",
                                       "%Y-%m-%d %H:%M:%S")).split(' ')[0]
        self.url = url_global
        self.entryurl = url_entry
        self.seaturl = url_seat
        self.username = username
        self.password = password
        self.user_header = (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--window-size=1920,1080")
        self.option.add_argument("--start-maximized")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        self.option.add_argument('disable-infobars')
        self.option.add_argument('log-level=3')
        self.option.add_argument('user-agent={}'.format(self.user_header))
        self.driver = webdriver.Chrome(options=self.option)
        # self.driver = webdriver.Chrome()
        with open('logs.txt', 'a+', encoding='utf-8') as file:
            file.write('预约的日期：' + self.nexttime + '\n')
        file.close()
        try:
            self.driver.get(url_global)
        except:
            return -2
        self.st1 = st1
        self.st2 = st2
        self.et1 = et1
        self.et2 = et2
        self.next = next

    def login(self):

        name = self.driver.find_element(By.ID, 'tbUserName')
        pwd = self.driver.find_element(By.ID, 'tbPassWord')
        name.send_keys(self.username)
        pwd.send_keys(self.password)
        self.driver.find_element(By.ID, 'Button1').click()
        print('\nlog success')

    def chooseseat(self, st, et, num):
        print('\n########')
        nextstr = self.nexttime

        for seatsid in range(st , et, random.randint(1, 10)):
            flag = True
            print("the seat is:{}".format(seatsid), end=' ')
            seturl = self.seaturl + 'fid=' + classroom[num] + '&sid=' + seatsid.__str__()
            print("\ntrying")
            self.driver.get(seturl)
            # sleep(1)
            data = self.driver.find_element(By.ID, 'OrderDate')
            stTime1 = self.driver.find_element(By.ID, 'stTime1')
            stTime2 = self.driver.find_element(By.ID, 'stTime2')
            etTime1 = self.driver.find_element(By.ID, 'etTime1')
            etTime2 = self.driver.find_element(By.ID, 'etTime2')
            clickon = self.driver.find_element(By.CLASS_NAME, 'apply-btn')
            clickpop = self.driver.find_element(By.CLASS_NAME, 'pop-btn')
            if int(self.next) == 1:
                js = "document.getElementById('OrderDate').value='{}';".format(nextstr)
                self.driver.execute_script(js)

            stTime1.send_keys(self.st1)
            stTime2.send_keys(self.st2)
            etTime1.send_keys(self.et1)
            etTime2.send_keys(self.et2)
            # 预约
            clickon.click()
            # 确认
            clickpop.click()

            log = self.driver.switch_to.alert.text
            with open('logs.txt', 'a+', encoding='utf-8') as file:
                file.write(log)
            file.close()
            if "成功" in log:
                print("完成")
                flag = True
            elif "已过" in log:
                print("时间已过")
                self.driver.quit()
                return -1
            elif "你的两次预约时间间隔太短了" in log:
                print("你预约时间间隔太短")
                self.driver.quit()
                return 2
            elif "冲突" in log:
                print("你预约时间有重复")
                self.driver.quit()
                return 2
            else:
                flag = False
            self.driver.switch_to.alert.accept()
            if flag == True:
                print("预约成功")
                self.driver.quit()
                return seatsid - st + 1
            print('failure')
        print("$$$$$$ over")
        with open('logs.txt', 'a+', encoding='utf-8') as file:
            file.write('#################\n')
        file.close()
        return 9999

    # 0-1.2楼- 报刊    1-
    # 2.2楼- 电子阅览室 fid=1&sid=2876 to fid=1&sid=3063
    # 3.3楼- 社科 fid=1&sid=1096 to fid=3 sid=1409
    # 4.3楼- 自然            1438 to 1772
    # 5.3楼- 公共-东      2434 to 2690
    # 6.3楼- 公共-西

    def choose(self, room):
        num = int(room)
        if num == 1:
            return self.chooseseat(1, 407, num)
        elif num == 2:
            return self.chooseseat(2876, 3063, num)
        elif num == 3:
            return self.chooseseat(1096, 1409, num)
        elif num == 4:
            return self.chooseseat(1438, 1773, num)
        elif num == 5:
            return self.chooseseat(2434, 2690, num)
        elif num == 6:
            return self.chooseseat(2522, 2617, num)


def func():
    i = 0
    dev = 1
    nowtime = time.strftime('%H:%M:%S', time.localtime())
    print('开始预约时间：{}'.format(nowtime))
    next_day, next_month, next_year, now_time = loadtime()
    with open('logs.txt', 'a+', encoding='utf-8') as file:
        file.write('开始预约时间：'+nowtime+'\n')
    file.close()
    if dev:
        username = '19111301135'
        password = '135tsg!!'
        room = '2'#预约的教室
        st1 = '14'#预约开始小时
        st2 = '00'#预约开始分钟
        et1 = '22'#预约结束小时
        et2 = '00'#预约结束分钟
        tom = 1 #1就是预约明天的位置，0是预约今天的座位，一般当天电子阅览室很难预约了，基本满的
    while i < 60:#尝试60次
        i = i + 1
        try:#可能出现未知错误，如果图书馆服务器关机了，那算60次也是要j
            dd = Sele(username, password, st1, st2, et1, et2, tom, next_day, next_month, next_year)
        except:
            sleep(30)
            continue
        break
    print("初始化完成>>Login")
    dd.login()
    print("Choose")
    result = dd.choose(room)
    print("座位：{}".format(result))
    nowtime = time.strftime('%H:%M:%S', time.localtime())#下次预约时间，倒计时
    with open('logs.txt', 'a+', encoding='utf-8') as file:
        file.write('完成预约时间：'+nowtime+'\n')
    file.close()
    print("Now:{},线程数：{}".format(nowtime,threading.active_count()))
    # 如果需要循环调用，就要添加以下方法,间隔一天
    t = threading.Timer(86400, ti)
    t.start()

def ti():
    func()

if __name__ == "__main__":
    # 获取现在时间
    now_time = datetime.datetime.now()
    print("现在：" + str(now_time))
    # 获取明天时间
    next_day, next_month, next_year, now_time = loadtime()

    # 获取明天点时间，参数中定在6：05开始进入func函数进入选座
    next_time = datetime.datetime.strptime(
        str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 06:05:00", "%Y-%m-%d %H:%M:%S")
    print("明天：" + str(next_time) + "预约")
    # # 获取昨天时间
    # last_time = now_time + datetime.timedelta(days=-1)
    # 获取距离明天3点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    print("时差：" + str(timer_start_time))
    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, func)#timer_start_time决定程序什么时候进入func函数，即预约座位
    timer.start()

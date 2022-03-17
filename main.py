import unittest
import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction
import time
import datetime
import pandas as pd



class ConnMon(unittest.TestCase):

    def setUp(self):
        # Set up appium
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4723/wd/hub',
            desired_capabilities={
                "platformName": "Android",
                "platformVersion": "11",# 실행할 폰에 맞추어 정보 수정 필요
                "deviceName": "A40",# 실행할 폰에 맞추어 정보 수정 필요
                "automationName": "Appium",
                "newCommandTimeout": 3000,
                "appPackage": "com.koamtac.ktsync",
                "appActivity": "com.koamtac.ktsync.MainActivity",
                "udid": "R59M702GR4B",# 실행할 폰에 맞추어 정보 수정 필요
                "noReset": "True"  # app 데이터 유지
            })


    def test_search_field(self):
        # appiun의 webdriver를 초기화 합니다.
        driver = self.driver
        # KTSync 실행하고 10초 대기
        sleep(10)

        #연결 끊김 이벤트 저장용 데이터 프레인 생성
        df = pd.DataFrame(columns={"Time", "Event"})

        #모니터링 종료시간(현재시간 + 10시간) 설정
        time_mon_end = time.time() + 36000
        time_now = time.time()

        #KDC장치 이름 선언
        conn_stat = driver.find_element(By.XPATH,
                                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView[2]").text
        device_name = conn_stat[0:14]

        #모니터링 시간 동안 연결 상태 확인
        while time_mon_end > time_now :
            conn_stat = driver.find_element(By.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView[2]").text
            conn = conn_stat[-9:]
            #연결중 상태가 아닐 시 데이터 프레임에 결과 저장 & 재연결
            if conn != "Connected":
                discon_stat = driver.find_element(By.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView[2]").text
                now = datetime.datetime.now()
                discon_time = now.strftime('%Y-%m-%d %H:%M:%S')
                discon_event = {
                    "Time": [discon_time],
                    "Event": [discon_stat]
                }
                df_discon = pd.DataFrame(discon_event)
                df = pd.concat([df, df_discon])
                df.to_csv(device_name + "_ConnMon" + ".csv")
                #재연결
                driver.find_element(By.XPATH,
                                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.LinearLayout[2]/android.widget.TextView[1]").click()
                sleep(2)
                # 페어링 된 KDC 선택
                driver.find_element(By.XPATH,
                                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout").click()
                # 10초 대기
                sleep(10)
            else :
                pass
            time_now = time.time()
            time_remain = time_mon_end - time_now
            print("남은 시간 : " + str(datetime.timedelta(seconds = time_remain)))

        # now = datetime.datetime.now()
        # now_date = now.strftime('%Y%m%d%H%M%S')
        # df.to_csv(device_name + "_" + now_date + ".csv")








def tearDown(self):
    self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ConnMon)
    unittest.TextTestRunner(verbosity=2).run(suite)
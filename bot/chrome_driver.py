from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller as auto_install
import time
import re
import os

class Driver:
    
    def __init__(self):
        chrome_ver = auto_install.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

        if os.path.isdir(f'./{chrome_ver}/'):
            pass
        else:
            auto_install.install(True)
        
        dr = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')   
        dr.set_window_size(1920,500)
        totalWidth = dr.execute_script("return document.body.offsetWidth")
        totalHeight = dr.execute_script('return document.body.parentNode.scrollHeight')
        # 화면의 실제 사이즈로 변경합니다.
        dr.set_window_size(totalWidth, totalHeight)
        dr.implicitly_wait(10)
        
        
    
    def execute_element(selenium_class):
        results = ''
        for element in selenium_class:
            results = element.text
        return results

    

        
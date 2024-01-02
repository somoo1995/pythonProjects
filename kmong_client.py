from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
import time
import configparser
import tkinter as tk
from tkinter import Scrollbar, Text
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import sys , numpy as np
import os
from ctypes import *
import random
import pyperclip
from urllib.parse import quote
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
import pyautogui
from datetime import datetime, timedelta
import psutil
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import font
import webbrowser
from selenium.webdriver.chrome.service import Service



# pyinstaller -F --icon=myicon.ico --add-data="logo.jpg;." kmong_client.py
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def open_link(event):
    # webbrowser를 사용하여 링크 열기
    webbrowser.open('https://cafe.naver.com/oolife?tc=shared_link')

def open_web_link():
    webbrowser.open("https://pf.kakao.com/_sjeUxj")

def log_message(message):
    """ 로그 메시지를 Text 위젯에 기록하는 함수 """
    log_text.insert(tk.END, f"{message}\n")

    log_text.see(tk.END)
    main_window.update_idletasks()

def check_expiry(expiry_date_str):
    # 현재 날짜 구하기
    current_date = datetime.now().date()
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
    # 만료일과 현재 날짜의 차이 계산
    days_until_expiry = (expiry_date - current_date).days
    
    if days_until_expiry > 0:
        print(f"유효 기간이 {days_until_expiry}일 남았습니다.")
        log_message(f"유효 기간이 {days_until_expiry}일 남았습니다.")

    elif days_until_expiry == 0:
        print("오늘까지가 유효 기간입니다.")
        log_message("오늘까지가 유효 기간입니다.")
        messagebox.showerror("Warning", "유효기간이 오늘까지입니다.")
    else:
        print("유효 기간이 이미 만료되었습니다.")
        log_message("유효 기간이 이미 만료되었습니다.")
        return False



def naver_login(driver, id, password):
    url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/'
    driver.get(url)
    driver.implicitly_wait(10)


    # 웹 요소를 클릭합니다.
    element = driver.find_element(By.CSS_SELECTOR, "#id")

    # 해당 웹 요소에 포커스를 줍니다. # 아이디 입력
    driver.execute_script("arguments[0].focus();", element)
    print("아이디 입력")
    log_message("아이디입력")
    pyperclip.copy(f'{id}')
    pyautogui.hotkey('ctrl', 'v')
    print("비밀번호 입력")
    log_message("비밀번호 입력")



    # 해당 웹 요소에 포커스를 줍니다.
    time.sleep(1)
    element = driver.find_element(By.CSS_SELECTOR, "#pw")
    driver.execute_script("arguments[0].focus();", element)
    pyperclip.copy(f'{password}')
    pyautogui.hotkey('ctrl', 'v')
    print("엔터 누르기 전")
    time.sleep(0.2)
    pyautogui.press('enter')


    try:
        element = driver.find_element(By.CSS_SELECTOR, "#new\.dontsave").click()
    except:
        pass

    time.sleep(int(naver_id_wait.get()))

#__________________________________________________________________블로그 id 얻는 기능_________________________________________________________________________________
def get_blog_ids(driver, keyword, page_no):
    # 키워드를 URL 인코딩
    encoded_keyword = quote(keyword)
    

    # URL 업데이트
    if sel_ac.get() == "1":
        sel_ac_time = "sim"
        url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_no}&rangeType=ALL&orderBy={sel_ac_time}&keyword={encoded_keyword}"
        driver.get(url)
    elif sel_ac.get() == "2":
        sel_ac_time = "recentdate"
        url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_no}&rangeType=ALL&orderBy={sel_ac_time}&keyword={encoded_keyword}"
        driver.get(url)
    
    print(f"{page_no}번째 페이지에서 블로그 아이디를 얻어옵니다!")
    log_message(f"{page_no}번째 페이지에서 아이디를 얻어옵니다!")
    driver.implicitly_wait(10)
    blog_ids = []
    for i in range(1, 8):  # 페이지에는 최대 7개의 게시물이 있습니다.
        try:
            selector = f"#content > section > div.area_list_search > div:nth-child({i}) > div > div.info_post > div.writer_info > a"
            element = driver.find_element(By.CSS_SELECTOR, selector)
            
            blog_url = element.get_attribute("href")
            blog_id = blog_url.split('/')[-1]
            blog_ids.append(blog_id)
        except:
            break
    return blog_ids
#___________________________________________________________________________________________________________________________________________________

def get_blog_id_by_id(driver,id_list):
    blog_ids = []
    for doit in id_list:
        for i in range(1, 6):  # 5개의 tr
            try:
                driver.get(f"https://blog.naver.com/{doit}/1")
                driver.implicitly_wait(1)
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    pass
                try:
                    driver.find_element(By.CSS_SELECTOR,f'#toplistSpanBlind').click()
                except:
                    pass
                driver.switch_to.frame('mainFrame')
                wait = WebDriverWait(driver, 10)
                anchor = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'table > tbody > tr:nth-child({i}) > td.title > div > span > a'))
                )
                anchor.click()
                time.sleep(1)
                current_url = driver.current_url
                match = re.search(r"/(\d+)$", current_url)
                if match:
                    log_no = match.group(1)
                    print(f"{i}번째임 {log_no}")  
                else:
                    print("logNo not found in the URL.")
                anchor = driver.find_element(By.CSS_SELECTOR,f'#Sympathy{log_no}').click()
                driver.implicitly_wait(10)
                driver.switch_to.frame(f"sympathyFrm{log_no}")
                driver.implicitly_wait(10)
                j=1
                while True:
                    driver.implicitly_wait(10)
                    try:
                        selector = f' #post-area > ul > li:nth-child({j}) > div > div.bloger > span.area_text.pcol2 > strong > span > a'
                        element = driver.find_element(By.CSS_SELECTOR, selector)
                        blog_url = element.get_attribute("href")
                        blog_id = blog_url.split('/')[-1]
                        blog_ids.append(blog_id)
                        j=j+1
                    except Exception as e:
                        driver.switch_to.default_content()
                        break
            except Exception as e:
                print(f'{e}')
                print('페이지 완료')
                log_message("페이지 완료\n")



        print(blog_ids)
        log_message( f"{blog_ids}\n")
        return blog_ids
        pass


#_______________________________________________________친구 요청하는 기능____________________________________________________________________________________________
def send_friend_requests(driver, keyword, max_requests,select):
    page_no = 1
    sent_requests = 0
    while sent_requests < max_requests:
        if selected_option.get() == "1":
            print("keyword로 시작합니다.")
            log_message(f"keyword로 시작합니다.\n")
            
            blog_ids = get_blog_ids(driver, keyword, page_no) # page_no에는 entry에서 가져온 정보들ㅇ르 가져온다, keyword 에도 마찬가지다
        elif selected_option.get() == "2":
            print("아이디로 가져옵니다.")
            log_message(f"입력받은 아이디로 시작합니다.\n")
            ids = keyword_id_text.get("1.0","end-1c")
            id_list =  [item.strip() for item in ids.split("||")]# 여기에서는 gui에서 얻어온 정보들을 적어준다
            blog_ids = get_blog_id_by_id(driver,id_list)

      

        for blog_id in blog_ids:
            try:
                driver.get(f"https://m.blog.naver.com/BuddyAddForm.naver?blogId={blog_id}&returnUrl=https%253A%252F%252Fm.blog.naver.com%252FPostList.naver%253FblogId%253{blog_id}")
                driver.implicitly_wait(10)

                try:
                    element = driver.find_element(By.CSS_SELECTOR, "#lyr4 > div > div.txt_area > p") 
                    print("친구추가 할 수 없는 상태")
                    log_message( f"친구추가 할 수 없는 상태. 다음 아이디로 넘어갑니다.\n")
                    continue
                except: 
                    print("라디오버튼 접근 가능")

                time.sleep(0.5)
                element = driver.find_element(By.CSS_SELECTOR, "#bothBuddyRadio")
                disabled_value = element.get_attribute("disabled")

                if disabled_value is not None:
                    print("'disabled' 속성이 있습니다.")
                    print("다음 목록으로")
                    continue
                else:
                    print("'disabled' 속성이 없습니다.")
                    print("친구추가가 가능합니다!")
                    log_message( f"친구추가 가능합니다!\n")
                    element.click()
                    textarea_element = driver.find_element(By.CSS_SELECTOR, '#buddyAddForm > fieldset > div > div.set_detail_t1 > div.set_detail_t1 > div > textarea')

                    # textarea의 내용을 지웁니다.
                    textarea_element.clear()

                    # 원하는 문자열을 입력합니다. 여기서는 "새로운 메시지"라는 문자열을 입력했습니다.
                    send_ments = text_widget_ment.get("1.0","end-1c")
                    send_ment_list = [item.strip() for item in send_ments.split("||")]
                    ment = random.choice(send_ment_list)

                    ## 랜덤으로 보내주기
                    textarea_element.send_keys(f"{ment}")
                    element = driver.find_element(By.CSS_SELECTOR, "body > ui-view > div.head.type1 > a.btn_ok")
                    element.click()
                    time.sleep(1)
                    sent_requests += 1
                    print(f"{sent_requests}번째 요청 완료!")
                    log_message( f"{sent_requests}번째 요청 완료!\n")
                    print('여기까지가 요청 완료한 시점')
                    #______________________________게시글 좋아요, 댓글달기 __________________________________________________________________ 여기에 체크박스 조건문
                    #여기에 이제 gui에서 가져오는 조건들을 가져온다, 
                    if var_comment.get() == 1 or var_like.get() == 1:
                        driver.implicitly_wait(1)
                        for i in range(1, int(spinbox_comment.get())+1):  # 5개의 tr 여기에는 gui에서 가져오는 실행횟수를 가져온다.
                            send_comments = comment_text.get("1.0","end-1c")
                            send_comments_list = [item.strip() for item in send_comments.split("||")]
                            
                            try:
                                driver.get(f"https://blog.naver.com/PostList.naver?blogId={blog_id}&categoryNo=0&from=postList")
                                
                                try:
                                    det = driver.find_element(By.CSS_SELECTOR,"#category-name > div > table.post-body > tbody > tr > td.bcc > div > a")
                                    det.click()
                                except:
                                    print("못찾았어요.")
                                try:
                                    anchor = driver.find_element(By.CSS_SELECTOR,f'#postBottomTitleListBody > :nth-child({i}) a')
                                    anchor.click()
                                except:
                                    pass
                                try:
                                    anchor = driver.find_element(By.CSS_SELECTOR,f'#listTopForm > table > tbody > tr:nth-child({i}) > td.title > div > span > a')
                                    anchor.click()
                                except:
                                    pass
                                
                                current_url = driver.current_url
                                
                                match = re.search(r"logNo=(\d+)", current_url)
                                if match:
                                    log_no = match.group(1)
                                    print(log_no)  
                                else:
                                    print("logNo not found in the URL.")

                                ##################### 블로그의 고유 게시글 번호 가져오기###############################

                                if var_like.get()== 1:
                                    print(f"{i}번째 좋아요 누르기")
                                    log_message( f"{i}좋아요 누르기 시작\n")

                                    anchor = driver.find_element(By.CSS_SELECTOR,f'#area_sympathy{log_no} > div > a > span.u_ico._icon.pcol3').click()
                                    
                                    try:
                                        alert = driver.switch_to.alert
                                        alert.accept()
                                    except:
                                        pass


                                if var_comment.get() == 1:
                                ###### 체크박스 조건문 ,댓글 쓰기 체크박스######################################################################################

                                    anchor = driver.find_element(By.CSS_SELECTOR,f'#Comi{log_no}').click()
                                    time.sleep(1)
                                    log_message( f"{i}번째 게시글 댓글 달기 시작\n")
                                    print('댓글창 누르기 성공')
                                    
                                    element = driver.find_element(By.XPATH, "//*[contains(text(), '블로그가 더 훈훈해지는 댓글 부탁드립니다. @별명을 입력하면 서로이웃이 소환됩니다.')]")
                                    element.click()
                                    print("댓글창 활성화 성공")
                                    textarea_element = driver.find_element(By.ID, f"naverComment_201_{log_no}__write_textarea")
                                    ## 여기서 수정해줘야하고 랜덤으로 넣기
                                    comment = random.choice(send_comments_list)
                                    textarea_element.send_keys(f"{comment}")
                                    try:
                                        send_comments_list.remove(comment)
                                    except:
                                        send_comments = comment_text.get("1.0","end-1c")
                                        send_comments_list = [item.strip() for item in send_comments.split("||")]
                                        comment = random.choice(send_comments_list)
                                    comment_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no} > div > div.u_cbox_write_wrap.u_cbox_writing > div.u_cbox_write_box.u_cbox_type_logged_in > form > fieldset > div > div > div.u_cbox_upload > button")
                                    comment_button.click()
                                ##########체크박스 조건문, 좋아요 누르기 체크박스####################################################################################

                               
                                
                                ##############################################################################################################################
                            except Exception as e:
                                print(f"An error occurred: {e}")
                                print(f"Error on {i}th tr.")
                                print("게시물이 더는 없네요!")
                                log_message( f"게시글이 더는 없습니다!\n")
                                break
                    #__________________________________________좋아요, 댓글달기____________________________________________________________________________

                    if sent_requests >= max_requests:
                        log_message( f"{max_requests}만큼 완료 했습니다.\n")
                        return
                    elif sent_requests == len(blog_ids) and select == "get_by_id":
                        log_message( f"{max_requests}만큼 완료 했습니다.\n")
                        return

            except Exception as e:
                print(f"Error with blog_id {blog_id}: {e}")

        # 다음 페이지로 이동
        page_no += 1

#___________________________________________________________________________________________________________________________________________________

time.sleep(3)
service = Service(executable_path=resource_path('files/chromedriver.exe'))
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])

## fire base 초기화 부분
mykey={
    "type": "service_account",
  "project_id": "blog-95f26",
  "private_key_id": "7f4a8211fa7ad9c5c520c8eefdb2928056e144b1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDTizivADcfHaxw\n39EFyWTHej+zh6a72UjiamuMH1cwVmcNXENRcPThvbmDWctlpsoZWfHG6SogCWYs\nIO1Pwmy6WebPoIT2UBECPVm9IBZdAAdAZe6oidOv8tUWBqCuFS48SJfhD85VVAPT\nBzmHSx1dcVgHu+w4EMnhBBkwsl4XryIsgMDX2oOZADkFGFFZ1KcKWIdcJubRDYh1\n12DSGsrERfr7yOjUm5zoKnZsIYfBRPKd3AcBRGAwGD+sgjJjg0PxVJC3h1GNO/Ik\nLfIB9eAcQcO+UJ0R4QZ9Kf9UwmAJvRz5Je4wMG9MZ7eTap2jqMeIEPWLpWuollen\nvfWbGDExAgMBAAECggEAIrlAES26Xo+q3g5HC6messWkzi3OlxgYCB5K0AHW+Ha+\nTKmf3S7q62EOofpr0iA6HUYv0yQzx3VzgXvYKFb0LPST1/Hz0VCcMh9q6wno0dQu\n3Im+zohtKHz2MDrfRiPw5nFOCOHkzwnO5OVTMpuIUu3HcuGMaTmMQbTAA8fLfRx0\nRDpUrpYnkMfRns13fCGzu1VtSeBMRsSfVCqhLjpUa5y2xYXMsyE2xTT/qS1V2y8N\ntdApGqV9HuzQlfBFjEklGbTAiNcVFydfOrFVeCEAV0Wr8x8a6kEHYp0N3LOLAU3W\nPB3MjZpIVqthxAaOjI3Ic54KP9MBtKcBcdM8HssaKQKBgQD0hsFCAdBpLlkrIPRE\nukE6F+YANZuao08ItEiw4eDMbxrA5jElVbwk4CRwNQvHnQL61ZGnBYGjvkPQDJ+S\nUFB7tABkSOD2rNLYn6XzbTUX6HFJYi/RsuWBUOFPFB1Rp9jo5w3e57/a9gP1VYeo\nKIylug0jwgx4hfnIbn5tPiNxRQKBgQDdeEfnbWsV7q7Zqj1i+0lS6XK9PBcvyXDS\new8Hrr91GEGfeq6pztudt2E7E6mmecmaeeSqwmIQnjCLHcndTeDHe0npQxL3vj0K\nqqcwXbLWZyUbo7KEQYjce2lc4mK9bWzMnOEbins3374kg93sitgMNgV9DGDuGSiz\nI0p0+sBA/QKBgQDhsgdqr1X33ym6Xx5W2TsfLbPC+bf30Ug/lneJm9Lrnpko9s7h\n0PJpbuDzGGMZCVkYwEtByBlSU2kv/JbEa5D9vLSn24SY6gdqnmCEAIaC3K7DtvbA\nLMkcxNRRMxWkqrHQtoLc/TbeGTiqFxmxIkw/IyzBlngAPljAoQvcNQBtqQKBgCXP\npE8RskezUWzeEM72YgViz/EY8kh5VubIlb9VCWD/fCyzMGDTbVFW/qWsbLl8b3wN\nNYol18JIj7cgpdc/tZG5LdxCVFmxxBAvJI4wYRkT0RUP9Kl52tjxxQJTsFHw/bNN\nUW13TiQy8e6gCOKardof2v4HgAEGkJlM/ChOq0YtAoGAYL2lfVIwNcmpTcw9JJWp\ne0OB1BLo+pNnrjkT1TCEeimifrHRq61LGAGcrSQUi0W7AuLQqiPXiOLdkqMYTHMP\nx33ARRZvUblcdXPieXe3pKTM+lDsF7+YinTTLCxWLPligXmgASgmW2Vy1DEMD9zN\nG8iaAsPkxBYlsFGYVXTere4=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-uynfm@blog-95f26.iam.gserviceaccount.com",
  "client_id": "102933009012528563811",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-uynfm%40blog-95f26.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


config = configparser.ConfigParser()
cred = credentials.Certificate(mykey)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://blog-95f26-default-rtdb.firebaseio.com/'
})



ref = db.reference("/user_info")
data = ref.get()

def get_motherboard_serial():
    result = subprocess.check_output('wmic baseboard get serialnumber', shell=True).decode()
    serial = result.split('\n')[1].strip()
    return serial
       




def save_config():
    config['USER_ID'] = {
        'user_id': user_id,
        'naver_id': naver_id_entry.get(),
        'naver_password' : naver_pw_entry.get(),
        'send_comment' : text_widget_ment.get("1.0","end-1c"),
        'comments' : comment_text.get("1.0","end-1c"),
        'requests_num' : spinbox_send_num.get(),
        'doit_num' : spinbox_comment.get(),
        'comment_checkbox' : var_comment.get(),
        'like_checkbox' : var_like.get(),
        'keyword_radio' : selected_option.get(),
        'sel_radio' : sel_ac.get(),
        'wait_time' : naver_id_wait.get()
    }
    
    with open(('settings.ini'), 'w', encoding="utf-8") as configfile:
        config.write(configfile)

def close_app():
    save_config()
    main_window.destroy()

def load_config():
    config = configparser.ConfigParser()
    
    if os.path.exists('settings.ini'):
        config.read('settings.ini', encoding='utf-8')
    else:
        # If not, read from the default settings bundled with the application
        config.read(resource_path('files/settings.ini'), encoding='utf-8')
    
    config_user_id = config['USER_ID']['user_id']
    config_naver_id = config['USER_ID']['naver_id']
    config_naver_password = config['USER_ID']['naver_password']
    config_send_comment = config['USER_ID']['send_comment']
    config_comments = config['USER_ID']['comments']  
    config_requests_num = config['USER_ID']['requests_num']
    config_doit_num = config['USER_ID']['doit_num']
    config_comment_checkbox = config['USER_ID']['comment_checkbox']
    config_like_checkbox = config['USER_ID']['like_checkbox']
    config_keyword_radio = config["USER_ID"]['keyword_radio']
    config_sel_radio = config["USER_ID"]['sel_radio']
    config_naver_wait = config["USER_ID"]['wait_time']
    return (config_user_id, config_naver_id, config_naver_password, config_send_comment,
             config_comments,config_requests_num,config_doit_num,
             config_comment_checkbox,config_like_checkbox,
             config_keyword_radio,config_sel_radio,config_naver_wait)


(config_user_id, config_naver_id, config_naver_password, config_send_comment,
  config_comments,config_requests_num,config_doit_num
 ,config_comment_checkbox,config_like_checkbox,config_keyword_radio,
 config_sel_radio,config_naver_wait) = load_config()


def login():
    global user_data
    global user_id
    user_id = user_id_entry.get()
    all_users_data = ref.get()

    user_data = None
    for unique_key, data in all_users_data.items():
        if user_id in data:
            user_data = data[user_id]
            user_unique_key = unique_key
            break

    print(user_data)
    print("=====================")

    if not user_data:
        messagebox.showerror("Error", "Invalid user ID!")
        return

    current_serial = get_motherboard_serial()
    serial_list = user_data.get('computer_serial', [])
    date = user_data.get('date', '')
    permissioned_computer = user_data.get('permissioned_computer', 0)
    print(current_serial)
    print(serial_list)
    print(date)
    print(permissioned_computer)
    extracted_serials = [serial.split('/')[0] for serial in serial_list]

    if current_serial in extracted_serials:
        login_window.destroy()
        index = extracted_serials.index(current_serial)
        current_serial_nickname = serial_list[index].split('/')[1]
        show_main_gui(user_id, user_data,current_serial_nickname)
    elif "None" in serial_list:
        response = messagebox.askyesno("Register?", "컴퓨터를 등록할 수 있습니다. 등록을 시작합니다.")
        if response:
            register_new_computer(user_id,user_unique_key)  # 이 함수는 컴퓨터 등록 기능을 구현해야 합니다.
    else:
        messagebox.showerror("Error", "등록되지 않은 컴퓨터! 추가등록은 관리자에게 문의하세요.")


def register_new_computer(user_id,user_unique_key):
    top = tk.Toplevel()
    top.title("New Computer Registration")
    top.iconbitmap(resource_path('files/myicon.ico'))
    top.configure(bg="#dfe6e9")

    label = tk.Label(top, 
                     text="등록할 컴퓨터의 닉네임:", 
                     bg="#dfe6e9",  # 라벨 배경색
                     fg="#2d3436",  # 라벨 글자색
                     font=(custom_font, 10))
    label.place(x=20, y=10)

    nickname_entry = tk.Entry(top, 
                              bg="#ffffff",  # 엔트리 배경색
                              fg="#2d3436",  # 엔트리 글자색
                              font=(custom_font, 10))
    nickname_entry.place(x=20, y=40)



    def register_to_server():
        nickname = nickname_entry.get().strip()
        if not nickname:
            messagebox.showerror("Error", "닉네임을 입력해주세요!")
            return

        # 메인보드 시리얼 가져오기
        current_serial = get_motherboard_serial()
        stored_data = f"{current_serial}/{nickname}"

        # DB에서 사용자의 computer_serial 리스트 가져오기
        user_ref = ref.child(f"{user_unique_key}/{user_id}/computer_serial")
        serials = user_ref.get()

        print(serials)
        print(user_unique_key)



        # None 값을 찾아 그 위치에 새로운 데이터 저장
        for i, serial in enumerate(serials):
            if serial == "None":
                user_ref.child(str(i)).set(stored_data)
                messagebox.showinfo("Success", "등록이 완료되었습니다!")
                top.destroy()
                return

        # 만약 여기까지 코드가 진행되면 None 값이 없다는 것을 의미합니다.
        messagebox.showerror("Error", "더 이상 컴퓨터를 추가할 수 없습니다.")

    register_button = tk.Button(top, text="등록", 
                            command=register_to_server, 
                            bg="blue",  # 배경색
                            fg="white",  # 글자색
                            activebackground="darkblue",  # 활성화될 때의 배경색
                            activeforeground="lightgray",  # 활성화될 때의 글자색
                            relief="raised",  # 테두리 스타일
                            bd=3,  # 테두리 두께
                            font=(custom_font, 10, "bold"))  # 폰트 스타일)
    register_button.place(x=65,y=80)
    
def main_start():
    naver_id_list = user_data.get('naver_id_list', []) 
    if naver_id_entry.get() in naver_id_list:
        pass   
    else:
        messagebox.showerror("Error", "등록되지 않은 네이버아이디! 등록은 관리자에게 문의하세요.")
        return
    if not keyword_id_text.get("1.0","end-1c").strip():
    # 에러 메시지 띄우기
        messagebox.showerror("Error", "키워드 혹은 아이디를 입력해주세요!")
        return
    if check_expiry(user_data['date']) == False:
        messagebox.showerror("Error", "유효기간 만료! 관리자에게 문의하세요!")
        return


    driver = webdriver.Chrome(options=options)
    naver_login(driver,naver_id_entry.get(),naver_pw_entry.get())
    time.sleep(1)
    print(select)
    ids = keyword_id_text.get("1.0","end-1c")
    id_list =  [item.strip() for item in ids.split("||")]#
    keyword = id_list[0]
    send_friend_requests(driver,keyword,int(spinbox_send_num.get()),select)

def start_threaded_task():
    """ main_start 함수를 별도 스레드에서 실행시키는 함수 """
    thread = Thread(target=main_start)
    thread.start()
    

def show_main_gui(user_id, user_data, current_serial_nickname):
    global main_window
    main_window = tk.Tk()
    main_window.tk.call('tk', 'scaling', 1.5)
    my_font = font.nametofont("TkDefaultFont")
    custom_font = font.Font(font=my_font, file=font_path)
    main_window.title("서이추 프로그램 [오오]")
    main_window.geometry("450x800+1100+100")
    main_window.configure(bg='black')

    main_window.iconbitmap(resource_path('files/myicon.ico'))
    # 상태 라벨
    status_text = f"빨간로고 클릭시 카페방문"
    status_label = tk.Label(main_window, text=status_text, font=(custom_font, 8), fg="white", bg='black')
    status_label.place(x=300, y=35,width=150, height=25)

    insert_text = f"{user_id}님 사용중인 PC :{current_serial_nickname} "
    insert_label = tk.Label(main_window, text=insert_text, font=(custom_font,10,"bold"), fg="white", bg='black')
    insert_label.place(x=50, y=10)

    

    # 노트북 생성
    notebook = ttk.Notebook(main_window)
    style = ttk.Style()
    style.configure("TNotebook", background='white')
    notebook.place(x=0, y=60, width=450, height=700)

    # 노트북 탭 1
    tab1 = ttk.Frame(notebook)
    style.configure('TFrame', background='white')
    
    

    original_image = Image.open(resource_path("files/logo.jpg"))

    # 이미지의 크기를 조절
    resized_image = original_image.resize((50, 50))  # width, height는 원하는 크기로 설정

        # ImageTk.PhotoImage를 사용하여 크기가 조절된 이미지 로드
    tk_image = ImageTk.PhotoImage(resized_image)
    label = tk.Label(main_window, image=tk_image,bg='black')
    label.bind('<Button-1>', open_link)
    label.place(x=0,y=0)

     # 상태 라벨
    status_text = f"만료날짜: {user_data['date']} "
    status_label = tk.Label(main_window, text=status_text, font=(custom_font, 10, "bold"), fg="white", bg='black')
    status_label.place(x=30, y=770, width=140,height=25)

    web_link_button = tk.Button(main_window, text="카톡 문의", command=open_web_link, bg="white", fg="black", font=(custom_font, 10, "bold"))
    web_link_button.place(x=350, y=770,width=80, height = 25)  # 위치는 필요에 따라 조정해 주세요.

    
    tk.Label(tab1, text="네이버 ID",font=(custom_font,10,"bold"), fg="white", bg='black').place(x=10, y=10, width=100,height=25)

    global naver_id_entry
    naver_id_entry = ttk.Entry(tab1)
    naver_id_entry.insert("0",config_naver_id)
    naver_id_entry.place(x=120, y=10, width=120,height=25)


    tk.Label(tab1, text="지연시간",font=(custom_font,10,"bold"), fg="white", bg='black').place(x=250, y=10,width=80,height=25)
    global naver_id_wait
    naver_id_wait = tk.Spinbox(tab1, from_=1, to=30, increment=1)
    naver_id_wait.delete(0, tk.END)  # 스핀박스의 모든 값을 지움
    naver_id_wait.insert(0, config_naver_wait)  # 스핀박스에 100을 입력
    naver_id_wait.place(x=330, y=10, width=30, height=25) 


    tk.Label(tab1, text="비밀번호",font=(custom_font,10,"bold"), fg="white", bg='black').place(x=10, y=40,width=100,height=25)
    global naver_pw_entry
    naver_pw_entry = ttk.Entry(tab1, show="*")
    naver_pw_entry.insert("0",config_naver_password)
    naver_pw_entry.place(x=120, y=40, width=120,height=25)

    tk.Label(tab1, text="신청 횟수",font=(custom_font,10,"bold"), fg="white", bg='black').place(x=250, y=40,width=80,height=25)
    global spinbox_send_num
    spinbox_send_num = tk.Spinbox(tab1, from_=1, to=100, increment=1)
    spinbox_send_num.delete(0, tk.END)  # 스핀박스의 모든 값을 지움
    spinbox_send_num.insert(0, config_requests_num)  # 스핀박스에 100을 입력
    spinbox_send_num.place(x=330, y=40, width=60, height=25) 

    
    tk.Label(tab1, text="서이추 멘트 입력",bg='white', fg='black',font=(custom_font,10,"bold"),underline=9).place(x=10, y=75)
    global text_widget_ment
    text_widget_ment = Text(tab1, wrap=tk.WORD)
    text_widget_ment.insert('1.0',config_send_comment)
    text_widget_ment.place(x=10, y=100, width=390, height=100)
    # Scrollbar 위젯 생성
    scrollbar = Scrollbar(tab1, command=text_widget_ment.yview)
    scrollbar.place(x=400, y=100, height=100)
    text_widget_ment.config(yscrollcommand=scrollbar.set)

    style = ttk.Style()
    style.configure("Black.TFrame", background="black")
    inner_frame = ttk.Frame(tab1,width=187,height=50, style="Black.TFrame")
    inner_frame.place(x=10,y=210)


    global selected_option
    selected_option = tk.StringVar()
    selected_option.set(config_keyword_radio)
    radio1 = tk.Radiobutton(inner_frame, text="키워드", variable=selected_option, value="1",bg='black',fg='white',selectcolor="black")
    
    global select
    radio1.place(x=10, y=25,height=25,width=60)
    radio2 = tk.Radiobutton(inner_frame, text="아이디", variable=selected_option, value="2",bg='black',fg='white',selectcolor="black")
    radio2.place(x=70, y=25,height=25,width=60)

    global sel_ac
    sel_ac = tk.StringVar()
    sel_ac.set(config_sel_radio)
    radio1_1 = tk.Radiobutton(inner_frame, text="정확도", variable=sel_ac, value="1",bg='black',fg='white',selectcolor="black" )
    radio1_1.var = sel_ac
    radio1_1.place(x=10, y=0,height=25,width=60)
    radio2_1 = tk.Radiobutton(inner_frame, text="최신순", variable=sel_ac, value="2",bg='black',fg='white',selectcolor="black")
    radio2_1.var = sel_ac
    radio2_1.place(x=70, y=0,height=25,width=60)
    
    
    # 라디오 버튼 생성
    

    global keyword_id_text
    keyword_id_text = Text(tab1, wrap=tk.WORD)
    keyword_id_text.place(x=10, y=260, width=170, height=100)

    # Scrollbar 위젯 생성
    scrollbar = Scrollbar(tab1, command=keyword_id_text.yview)
    scrollbar.place(x=180, y=260, height=100)
    keyword_id_text.config(yscrollcommand=scrollbar.set)

    inner_frame_1 = ttk.Frame(tab1,width=210,height=50, style="Black.TFrame")
    inner_frame_1.place(x=200,y=210)


    global var_like
    var_like = tk.IntVar(value=int(config_like_checkbox))
    checkbox_like = tk.Checkbutton(inner_frame_1, text="좋아요", variable=var_like,bg='black',fg='white',selectcolor="black")
    checkbox_like.place(x=3, y=0,width=60,height=25)

    
    
    global var_comment
    var_comment = tk.IntVar(value=int(config_comment_checkbox))
    checkbox_comment = tk.Checkbutton(inner_frame_1, text="댓 글", variable=var_comment,bg='black',fg='white',selectcolor="black")
    checkbox_comment.place(x=0, y=25,width=60,height=25)
    

    tk.Label(inner_frame_1, text="입력횟수",bg='black',fg='white').place(x=60, y=25,width=60,height=25)
    global spinbox_comment
    spinbox_comment = tk.Spinbox(inner_frame_1, from_=1, to=5, increment=1)
    spinbox_comment.delete(0, tk.END)  # 스핀박스의 모든 값을 지움
    spinbox_comment.insert(0, config_doit_num)  # 스핀박스에 100을 입력
    spinbox_comment.place(x=120, y=25, width=40, height=25)

    global comment_text
    comment_text = Text(tab1, wrap=tk.WORD)
    comment_text.insert('1.0',config_comments)
    comment_text.place(x=200, y=260, width=200, height=100)

    # Scrollbar 위젯 생성
    scrollbar = Scrollbar(tab1, command=comment_text.yview)
    scrollbar.place(x=400, y=260, height=100)
    comment_text.config(yscrollcommand=scrollbar.set)

    tk.Label(tab1, text="로그",bg='white',fg='black',font=(custom_font,10,"bold")).place(x=10, y=370)
    global log_text
    log_text = Text(tab1, wrap=tk.WORD)
    log_text.place(x=10, y=390, width=390, height=100)

    # Scrollbar 위젯 생성
    scrollbar = Scrollbar(tab1, command=text_widget_ment.yview)
    scrollbar.place(x=400, y=390, height=100)
    log_text.config(yscrollcommand=scrollbar.set)

    tk.Label(tab1, text="프로그램",bg='white',fg='black',font=(custom_font,10,"bold")).place(x=10, y=500)
    inner_frame_2 = ttk.Frame(tab1,width=417,height=1, style="Black.TFrame")
    inner_frame_2.place(x=10,y=520)

    notebook.add(tab1, text="기본설정")

    #버튼들 모음집
    style_options = {
    "bg": "black",  # 버튼의 배경색
    "fg": "white",  # 버튼의 글자색
    "font": (custom_font.cget("family"), 10, 'bold'),  # 글꼴, 크기, 스타일
    "relief": "flat",  # 버튼의 테두리 스타일
    "activebackground": "#6375D6",  # 버튼에 마우스를 올렸을 때의 배경색
    "activeforeground": "white"  # 버튼에 마우스를 올렸을 때의 글자색
}
    edit_start_button = tk.Button(tab1, text="시작", **style_options, command=start_threaded_task)
    edit_start_button.place(x=10, y=600,width=100)
    edit_save_button = tk.Button(tab1, text="저장", **style_options, command=save_config)
    edit_save_button.place(x=150, y=600,width=100)
    edit_end_button = tk.Button(tab1, text="종료", **style_options, command=close_app)
    edit_end_button.place(x=290, y=600,width=100)
    # 노트북 탭 2

  

    main_window.mainloop()

# 로그인 GUI

login_window = tk.Tk()
login_window.tk.call('tk', 'scaling', 1.5)
font_path = resource_path("NotoSansKR-Regular.ttf")

# 폰트 로드
my_font = font.nametofont("TkDefaultFont")
my_font.actual()
custom_font = font.Font(font=my_font, file=font_path) 
font_info = custom_font.actual()



login_window.title("서이추 프로그램 Login")
login_window.geometry("300x200+1100+300")
login_window.configure(bg='white')  # 옅은 초록색 배경
login_window.iconbitmap(resource_path('files/myicon.ico'))

# 버튼 스타일 설정


login_label = tk.Label(login_window, text="Enter your user ID:", font=('HY견고딕', 12, 'bold'), bg='#A8E6CF', fg='#555555')  # 진한 회색, 굵은 글꼴
login_label.place(x=15, y=10)  # 위치 조절

user_id_entry = ttk.Entry(login_window, width=25)
user_id_entry.insert("0",config_user_id)
user_id_entry.place(x=15, y=40, height=20)  # 위치 조절

# 바인드: 엔터키를 누르면 login 함수 실행
user_id_entry.bind("<Return>", lambda _: login())

login_button = ttk.Button(login_window, text="Login", command=login, style="TButton")
login_button.place(x=200, y=35, width=80)  # 버튼 위치 및 크기 조절

user_id_entry.focus_set()  # Entry에 초점 설정
login_window.mainloop()






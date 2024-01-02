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
import openai
import inspect



# pyinstaller -F --icon=myicon.ico --add-data="logo.jpg;." kmong_client.py
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def gpt_comments(input):
    print("hello")
    ## 클라이언트의 키값 가져와야함
    # 이건 제작자꺼
    # openai.api_key="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"
    openai.api_key = "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"
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{input} <<이 글을 보고 간단한 댓글 하나 달건데 짧게 50글자 이하로 부탁할게."}
        ]
    )
    end_time = time.time()
    restime = end_time - start_time
    print(response.choices[0].message['content'].strip())
    print(f"소요시간 : {restime:.2f}")
    return response.choices[0].message['content'].strip()

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
    driver.implicitly_wait(2)

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



time.sleep(3)
service = Service(executable_path=resource_path('files/chromedriver.exe'))
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])

## fire base 초기화 부분
# 바꿔야할 부분들 (OO사용자의 database url로)
mykey={
    "type": "service_account",
    "project_id": "comment-5b3fe",
    "private_key_id": "7ed0e904781329812e6e164d985eca4704f0b4dd",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDN8EvnaKFjbQ+t\n4WdpXZ0L5RpTwqjuc+vrlUM6brW1tB0eJXQdmhQrOO08nmL/w4m7AB5T4Z5ZTBd1\naCFdwf6XFULDaELsMEQOvLTX1iFutiUktl/K39cPcsjlpPL6/6qsdO8ETDtHeR+y\nvxo5tWOvxK6MCd58qSPFWpSsDfUVUWGpJWQ2y0TVpAFfBIHg1/nTsMLC9Ky3Tykd\nMbGvf+tW944A042RH/zxVyOZmvlduj9TxTyyPGizd4v5JsC/tQoooJbOW7Ljq+fF\n5V6piyFfBjQHVC0KgeH5Ay7x7N0wU6n5wk7mEQ/A7bw74/hPEkXtCcaOV1B2yMWy\nlH5JW0oBAgMBAAECggEACESr035qrmKAVOeeHoec6M+Zuz+vRyWd1P9Q6+1qe8Ff\nwuhXjWG0ihi2w66LRIAODVU/ongGQskQjwzvfANwLJI0tEJBH5j/foT6kMje3kJP\nYvY0ieFrUco2wSuaetPdfx+Rwh8qaR/2kxdjnuoGttWjeWljBqfG0SNmITNNQf4I\nSI7ZkDxAOdNVdztjThkYAsBisUe0kZacyM/bV7h23Aro67exMf70fqXkeeoX/kcq\n8j0i85/mL8zJcQ+N7IYtExGvycqeysj5ZCbS0xv0086ppD5rfapw7XroebyQxc3M\nIxkSC68v6vYuu5T0YRI8HqfXodG77b6SMJtecogmPQKBgQDo1H2IU/yQkxgDEZMo\nKtFTQDfS5MNwg7XkdAxpX93iAKe7/rKdHYRB1ToXFTS5GFKGStd0JMHRMNYfTbzV\nYejga0IvUlLMDUvj12m/RXDW8vc+OlIM25uCb6A1E6Oy1ro2np4NmXEmiK4/LbYd\nJVZ12HeLenS6QLdvZALZdzW0tQKBgQDibrqsU31lX3YMyupOKLHTXq1bzCeRvc8V\nSWu0+pgUn1Pix2CmWGaJjcL+L3Tg0M8lmQKuxOa54jkBqbxgQVqpglXt64pdeFcx\nefRjid+UwIJOFAaN0rjhSI6wWZmA53HPTqsD291ditbbLySXwui4CRgskL+P0Psv\na99ZxQb7nQKBgQCjPLd2aUveIQLow92kf8Ca2Z9J4NGVhQJ11VcOWgQ6e7Md/whD\nV3punYxIurloPEE/niFIcKzieZbmA56tDCQ1k32np9Qc9AWNDG47h/gA+/+URVdZ\nZG63GIP+MnLG4/1SZgryBe5q0dE4wle4P4FKxiWqSISmQNFa64eD6CxjMQKBgQCJ\nlhrbx0d0p5LFpy7EGzoiY28XTm/kwN7p4lkN+Q8byMxiCiASM7jqcDdB2Hg+euLD\nx7u3knFYFbvp5MdP/aYnRckM7oh+zza8G4yCRy6R5n/HDagF2Tr5uOrrASajCv8+\npmCH0bsqschoGrczd/2MhgooWjPsIWHfqL5of64EiQKBgGHArEaMC3suQJcyh7FM\npQzb3IYbfDIgnkFfSnpvOYM9PAIoLFuH4bFc5rHwEF/dO9763ZOC0it4L/i5HFhC\nDXYI3VhElJhsKrpVSQEBS1+uGIgsY1wiB9IxJf5sGy7QI81CSD5q2/EsC9oRHfVt\nspeQpcD5gGAnNfPCjcKNLiIZ\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-h41ge@comment-5b3fe.iam.gserviceaccount.com",
    "client_id": "112981417716442691595",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-h41ge%40comment-5b3fe.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(mykey)
firebase_app1 = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://comment-5b3fe-default-rtdb.firebaseio.com/'
}, name='comment-5b3fe')

ref = db.reference("/user_info", app=firebase_app1)
data = ref.get()


# 제작자의 클라우드키
programManageKey = {
    "type": "service_account",
    "project_id": "programmanage-bd683",
    "private_key_id": "f5f66ff7e93dba3c82930d90355cdc9dbdc1b161",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCohyOD/r8LS6SB\n+A7+1ehiu5bk/7aV74W+4ArDyTgyLdOu/M5JTvKld5ewGYNhbD3JUoDWBpaZa92h\n0m2dtJwPfJ1eek2jHjDZMbuoZtrhzH1T8H1YGWjhceFPEnOpoGhdgJNZM7gKWneJ\ny0Ret5z4vChJGr3Cxi7TNoMkHNRe8/fwEdXND6srDWXQiIqQ9SC9GFaS2o0xmPCy\nHI2xR1y91lNnHxAUPzDfxZM4x8UNeckkRjXOG4kNvrOZGgDPf6CwI/ZdS3Vn+zlO\nri89hf2QVN9o2SzQ5ldbfzQKKj4P0fSOR7GPFmZ4BXb539rYjdwgVY5W9dXBMYg7\n3xgFyTfRAgMBAAECggEACeO4RVLUgi9ZAtl8LnR+CRaKByaBtUW+MFJ0ae3WcuIL\n5d0Rppf6lumFiMDOhrqJMQBlmBRV5RXr28b98L8Rrg+kKnr8hax2tbV8ligcWHDI\nD/4bqj5U0G9UMfAwF7hWjNodNiMEqJ2Lc0DEN9ddikknB2He2IhfD2edBX2oRr7A\n9rSzAaOi5PMI1aCv2Sp8/XoX441F9R8LLpklrwi2vHxeMly2rrOwi7b0V2TsIx/K\nGsRmfwh5U3yvNCwT8yhMVHbJJEbpWG3O+xRQmcmD75IlRnZNHDOcZ/yHvOzcQVTR\ng2rBnIX/4WxKc2ME6zktuzGfbVT2dmpxumgS3tCZOQKBgQDQIQph2604GiyN7VdV\nyZo9MI9/m0kFD+lKhUfKoS+1QBE9izlpfsfqfHD8fJE0jbUVWf5eeoiog3dBOhWF\nvYP6SdOa+LFS5LeqwzfNrGqTyLZPAizGXcksOTPA9OFue46lgaowe4atkD4OnhE4\noocLMTDcD2sKn+MH5ErwDq5DvQKBgQDPSlHhmSR2sCQfR4FMFiKY6Lu87iZWotK+\nBLE915AZBEI0kyLEGabDmqsnUIabgGIosprraVe4hphYL+orCvR2NgB10LkilwYL\nj/VGvsY/+2E5GrHjFRYjfqAYSmtbgmVx76cClU/9/paidWGlPu3HiOLdukOdhMMD\nxk0wnXc7pQKBgDSuuF8O6SjTT0XZtwqrDlTAzwIA/5m9blMDq6l55Yaeof6PGEhA\n5D/RohP3QBYqbJTsA7xMjf0B0hT7q+j/kMGxIFQQ8WnHJUqfQafZJd0kqCkVptnL\ncZm1HQmRsuJxeikgykCdc/jJEzxF/Jv2X/KQUArUCEdXM3OS8PkU7j2NAoGABWyp\ndeDfDmgPme3yGT6fCydT+l61DCFYqHZQ+RBSCgWNgfizuTP+pDHA9tdpnloet3ft\nC+oGzKJhDDW8yAGSYiGJo4uhvKD9HIJY5dAKOhRm9+qV6x5bJPSkVd5krtFbvD6M\nPUoQ/NGTuY6ezoc2C7muTiUYrd+Sht/Cl1oXi60CgYBTCCsOs5qvuR4LcZX5Fig5\nbgT8EBJw39z0viF2U9IuRzxSYyv/1n8SpcBp44iWob0OF1N9oB8f9mp43Vka/VfD\nkxzwDXU5Cm+Mje/xsFToSrlsuIbi2FV+UxmJTxnh2lS+4PYpigrjFjRRamVm8nLW\nv1zUjsXIt1bEG6xLGDo21Q==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ef23l@programmanage-bd683.iam.gserviceaccount.com",
    "client_id": "101536447470937009968",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ef23l%40programmanage-bd683.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

cred2 = credentials.Certificate(programManageKey)
firebase_app2 = firebase_admin.initialize_app(cred2, {
    'databaseURL': 'https://programmanage-bd683-default-rtdb.firebaseio.com/'
}, name='programmanage-bd683')

ref1 = db.reference("/program_list",app=firebase_app2)

config = configparser.ConfigParser()
def get_motherboard_serial():
    result = subprocess.check_output('wmic baseboard get serialnumber', shell=True).decode()
    serial = result.split('\n')[1].strip()
    return serial
       




def save_config():
    config['USER_ID'] = {
        'user_id': user_id, 
        'naver_id': naver_id_entry.get(),
        'naver_password' : naver_pw_entry.get(),
        'comments_list' : text_widget_ment.get("1.0","end-1c"),
        'requests_num' : spinbox_send_num.get(),
        'secret' : var_secret.get(),
        'gpt_select' : gpt.get(),
        'keyword_radio' : selected_option.get(),
        'sel_radio' : sel_ac.get(),
        'wait_time' : naver_id_wait.get(),
        'neighbor_group' : neigbor_entry.get()
    }
    
    with open(('settings_comment.ini'), 'w', encoding="utf-8") as configfile:
        config.write(configfile)

def close_app():
    save_config()
    main_window.destroy()

def load_config():
    config = configparser.ConfigParser()
    
    if os.path.exists('settings_comment.ini'):
        config.read('settings_comment.ini', encoding='utf-8')
    else:
        # 만약 존재하지 않는다면, 기본으로 내장된 설정 파일을 불러옵니다.
        config.read(resource_path('files_comment/settings_comment.ini'), encoding='utf-8')
    
    config_user_id = config['USER_ID']['user_id']
    config_naver_id = config['USER_ID']['naver_id']
    config_naver_password = config['USER_ID']['naver_password']
    config_comments_list = config['USER_ID']['comments_list'] 
    config_requests_num = config['USER_ID']['requests_num']
    config_secret = config['USER_ID']['secret']
    config_gpt_select = config['USER_ID']['gpt_select']
    config_keyword_radio = config["USER_ID"]['keyword_radio']
    config_sel_radio = config["USER_ID"]['sel_radio']
    config_naver_wait = config["USER_ID"]['wait_time']
    config_neighbor_group = config["USER_ID"]['neighbor_group']
    return (config_user_id, config_naver_id, config_naver_password, config_comments_list,
             config_requests_num,config_secret,config_gpt_select,
             config_keyword_radio,config_sel_radio,config_naver_wait,config_neighbor_group)


(config_user_id, config_naver_id, config_naver_password, config_comments_list,
             config_requests_num,config_secret,config_gpt_select,
             config_keyword_radio,config_sel_radio,config_naver_wait,config_neighbor_group) = load_config()


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
            register_new_computer(user_id,user_unique_key)  # 컴퓨터 등록 함수
    else:
        messagebox.showerror("Error", "등록되지 않은 컴퓨터! 추가등록은 관리자에게 문의하세요.")


def register_new_computer(user_id,user_unique_key):
    top = tk.Toplevel()
    top.title("New Computer Registration")
    top.iconbitmap(resource_path('files_comment/myicon.ico'))
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

def print_with_lineno(message):
    frame = inspect.currentframe().f_back  # 이전 프레임을 가져옵니다 (print_with_lineno 함수를 호출한 프레임)
    info = inspect.getframeinfo(frame)
    print(f"[Line {info.lineno}] {message}")

def main_start():
    ######테스트#####
    ###테스트#######
    program_manage = ref1.child('OO').get()
    print(program_manage)
    if program_manage == 1:
        pass
    else:
        return
    if not text_widget_ment.get("1.0", "end-1c") and gpt.get() == 0:
        messagebox.showerror("Error", "댓글 문구를 적거나 gpt기능 체크를 해주세요!")
        return
    naver_id_list = user_data.get('naver_id_list', []) 
    if naver_id_entry.get() in naver_id_list:
        pass   
    else:
        messagebox.showerror("Error", "등록되지 않은 네이버아이디! 등록은 관리자에게 문의하세요.")
        return
    if not keyword_id_text.get("1.0","end-1c").strip() and selected_option.get()=="1":
    # 에러 메시지 띄우기
        messagebox.showerror("Error", "키워드를 입력해주세요!")
        return
    if check_expiry(user_data['date']) == False:
        messagebox.showerror("Error", "유효기간 만료! 관리자에게 문의하세요!")
        return


    driver = webdriver.Chrome(options=options)
    naver_login(driver,naver_id_entry.get(),naver_pw_entry.get())
    driver.implicitly_wait(1)
    if selected_option.get() == "1":
        print("키워드로 댓글 답니다")
        log_message("키워드로 댓글 달기 작업을 수행합니다.")
        print(keyword_id_text.get("1.0", "end-1c"))
        keyword = keyword_id_text.get("1.0", "end-1c")
        encoded_keyword = quote(keyword)
        
        page_no = 1
        targetnumber = int(spinbox_send_num.get())
        sent_comment = 1
        # URL 업데이트
        while 1:
            if sel_ac.get() == "1":
                sel_ac_time = "sim"
                url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_no}&rangeType=ALL&orderBy={sel_ac_time}&keyword={encoded_keyword}"
                driver.get(url)
                log_message("정확도로 검색합니다")
            elif sel_ac.get() == "2":
                sel_ac_time = "recentdate"
                log_message("최신순으로 검색합니다.")
                url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_no}&rangeType=ALL&orderBy={sel_ac_time}&keyword={encoded_keyword}"
                driver.get(url)

            blog_url_list = []
            for i in range(1, 8):  # 페이지에는 최대 7개의 게시물이 있습니다.
                try:
                    selector = f"#content > section > div.area_list_search > div:nth-child({i}) > div > div.info_post > div.desc > a.desc_inner"
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    blog_url = element.get_attribute("href")
                    blog_url_list.append(blog_url)  # blog_url을 리스트에 추가합니다.
                except:
                    break
            log_message("검색된 페이지의 블로그글 url을 읽어옵니다.")
            print(blog_url_list)

            for index, blog_url in enumerate(blog_url_list, start=1):
                print(f"{sent_comment}번째 페이지 탐색")
                log_message(f"{sent_comment}번째글 작업을 수행합니다.")
                send_comments = text_widget_ment.get("1.0","end-1c")
                send_comments_list = [item.strip() for item in send_comments.split("||")]
                try:
                    driver.get(blog_url)
                    current_url = driver.current_url
                    match = re.search(r'(\d+)$', current_url)
                    if match:
                        log_no = match.group(1)
                        print(log_no)  
                        driver.implicitly_wait(1)
                        driver.switch_to.frame("mainFrame")
                        try:
                            paragraphs = driver.find_elements(By.CSS_SELECTOR, "p[class*='text-paragraph']")
                            texts = []

                            for paragraph in paragraphs:
                                    # paragraph의 자식인 특정 <span> 태그를 찾습니다.
                                texts.append(paragraph.text)
                        except:
                            print("못찾았어요")

                        cleaned_texts = [text.replace('"', '').replace("'", "") for text in texts]

                        # 모든 항목을 하나의 문자열로 합칩니다.
                        resulting_text = ' '.join(cleaned_texts)

                        print(resulting_text)
                    else:
                        print("logNo not found in the URL.")

                    ##################### 블로그의 고유 게시글 번호 가져오기###############################
                    
                    try:
                        anchor = driver.find_element(By.CSS_SELECTOR,f'#Comi{log_no}').click()
                    except:
                        print("댓글창 비활성화 상태입니다.")
                        log_message("댓글을 달 수 없습니다.")
                        continue
                    time.sleep(1)
                    print('댓글창 누르기 성공')
                    try:
                        element = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no}_wai_u_cbox_content_wrap_tabpanel > ul > li > div.u_cbox_comment_box.u_cbox_mine.u_cbox_type_profile > div > div.u_cbox_info > span.u_cbox_info_sub > span > a")
                        print("이미 댓글단 사람입니다.")
                        log_message("이미 댓글을 달았습니다. 다음 글로 이동합니다.")
                        continue
                    except:
                        sent_comment +=1
                    if text_widget_ment.get("1.0","end-1c"):
                        element = driver.find_element(By.XPATH, "//*[contains(text(), '블로그가 더 훈훈해지는 댓글 부탁드립니다. @별명을 입력하면 서로이웃이 소환됩니다.')]")
                        element.click()
                        print("댓글창 활성화 성공")
                        log_message("지정된 댓글목록중에서 댓글을 작성합니다.")
                        textarea_element = driver.find_element(By.ID, f"naverComment_201_{log_no}__write_textarea")
                        ## 여기서 수정해줘야하고 랜덤으로 넣기
                        comment = random.choice(send_comments_list)
                        textarea_element.send_keys(f"{comment}")
                        try:
                            send_comments_list.remove(comment)
                        except:
                            send_comments = text_widget_ment.get("1.0","end-1c")
                            send_comments_list = [item.strip() for item in send_comments.split("||")]
                            comment = random.choice(send_comments_list)

                        if var_secret.get() == 1:
                            print("비밀댓글 신청합니다")
                            log_message("비밀댓글을 선택합니다.")
                            secret_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no}__write_textarea_secret_check")
                            secret_button.click()
                        else:
                            print("비밀댓글 신청 안함.")
                        comment_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no} > div > div.u_cbox_write_wrap.u_cbox_writing > div.u_cbox_write_box.u_cbox_type_logged_in > form > fieldset > div > div > div.u_cbox_upload > button")
                        comment_button.click()

                    if gpt.get() == 1:
                        print("gpt 댓글기능 시작")
                        log_message("gpt를 이용해서 댓글을 답니다.")
                        element = driver.find_element(By.XPATH, "//*[contains(text(), '블로그가 더 훈훈해지는 댓글 부탁드립니다. @별명을 입력하면 서로이웃이 소환됩니다.')]")
                        element.click()
                        print("댓글창 활성화 성공")
                        log_message("gpt와 통신중입니다.....")
                        textarea_element = driver.find_element(By.ID, f"naverComment_201_{log_no}__write_textarea")
                        comment = gpt_comments(resulting_text)
                        log_message("통신완료! 댓글을 입력합니다.")
                        textarea_element.send_keys(f"{comment}")
                        if var_secret.get() == 1 and not text_widget_ment.get("1.0", "end-1c"):
                            print("비밀댓글 신청합니다")
                            log_message("비밀댓글을 선택합니다.")
                            secret_button = driver.find_element(
                                By.CSS_SELECTOR, f"#naverComment_201_{log_no}__write_textarea_secret_check")
                            secret_button.click()
                        else:
                            print("비밀댓글 신청 안함.")
                        comment_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no} > div > div.u_cbox_write_wrap.u_cbox_writing > div.u_cbox_write_box.u_cbox_type_logged_in > form > fieldset > div > div > div.u_cbox_upload > button")
                        comment_button.click()
                        log_message("gpt 댓글 달기 완료")
                    else:
                        pass
                    if(targetnumber < sent_comment):
                        return
                    ##########체크박스 조건문, 좋아요 누르기 체크박스####################################################################################
                except Exception as e:
                    print(e)
                    print("댓글을 달 수 없는 글입니다.")
                    log_message("댓글을 달 수없는 글입니다.")
                    if(targetnumber < sent_comment):
                        return

            if(targetnumber < sent_comment):
                return
            else:
                page_no +=1







    else:
        print("이웃목록으로 합니다")
        log_message("이웃목록에서 이웃의 아이디를 불러옵니다.")
        blog_ids = []
        driver.get("https://blog.naver.com/MyBlog.naver")
        current_url = driver.current_url
        parts = current_url.split('/')
        parsedBlogId = parts[-1]

        
        driver.get(f"https://admin.blog.naver.com/AdminMain.naver?blogId={parsedBlogId}&Redirect=Buddyinfo")
        driver.switch_to.frame('papermain')
        
        j = 2
        neighbornum = 1
        while neighbornum  < 55:  # n은 가져오고 싶은 요소의 개수
            if neighbornum == 1:
                selector = "#buddyListManageForm > table > tbody > tr.first > td.buddy > div > a"
                group_selector = "#buddyListManageForm > table > tbody > tr.first > td.groupwrap > div"
            else:
                selector = f"#buddyListManageForm > table > tbody > tr:nth-child({neighbornum}) > td.buddy > div > a"
                group_selector = f"#buddyListManageForm > table > tbody > tr:nth-child({neighbornum}) > td.groupwrap > div"
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                group = driver.find_element(By.CSS_SELECTOR,group_selector).text
                if neigbor_entry.get() != group:
                    blog_url = element.get_attribute("href")
                    blog_id = blog_url.split('/')[-1]
                    blog_ids.append(blog_id)
                    print(blog_id)
                    neighbornum += 1
                else:
                    neighbornum += 1
               
            except:
                print("더이상 목록이 없습니다.")
                neighbornum=1
                try:
                    nextpage = driver.find_element(By.XPATH, f"//div[contains(@class, 'pp1')]//a[contains(@href, 'javascript:goPage({j})')]")
                    nextpage.click()
                    j +=1
                except:
                    break
 
        #블로그아이디 목록`으로 들어와서 
        log_message("목록 불러오기 완료!")
        print(blog_ids)
        targetnumber = int(spinbox_send_num.get())
        completenum = 0
        if targetnumber > len(blog_ids):
            log_message("에러, 지정한숫자가 이웃목록의 수보다 큽니다.")
            messagebox.showerror("Error", "에러, 지정한숫자가 이웃목록의 수보다 큽니다")
            return
        for target in blog_ids:
            if targetnumber == completenum:
                log_message("이웃목록으로 댓글달기 완료!")
                return

            send_comments = text_widget_ment.get("1.0","end-1c")
            send_comments_list = [item.strip() for item in send_comments.split("||")]
            driver.implicitly_wait(1)
            log_message(f"{completenum}번째 글에 댓글 달기를 시작합니다.")
            try:
                driver.get(f"https://blog.naver.com/PostList.naver?blogId={target}&categoryNo=0&from=postList")
                try:
                    det = driver.find_element(By.CSS_SELECTOR,"#category-name > div > table.post-body > tbody > tr > td.bcc > div > a")
                    det.click()
                except:
                    print("못찾았어요.")
                    
                try:
                    anchor = driver.find_element(By.CSS_SELECTOR,f'#postBottomTitleListBody > :nth-child(1) a')
                    anchor.click()
                except:
                    pass
                try:
                    anchor = driver.find_element(By.CSS_SELECTOR,f'#listTopForm > table > tbody > tr:nth-child(1) > td.title > div > span > a')
                    anchor.click()
                except:
                    pass
                
                current_url = driver.current_url

    

                
                match = re.search(r"logNo=(\d+)", current_url)
                if match:
                    log_no = match.group(1)
                    print(log_no)  
                    driver.implicitly_wait(1)
                    driver.get(f"https://blog.naver.com/{target}/{log_no}")
                    driver.switch_to.frame("mainFrame")
                    try:
                        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p[class*='text-paragraph']")
                        texts = []

                        for paragraph in paragraphs:
                                # paragraph의 자식인 특정 <span> 태그를 찾습니다.
                            texts.append(paragraph.text)
                    except:
                        print("못찾았어요")

                    cleaned_texts = [text.replace('"', '').replace("'", "") for text in texts]

                    # 모든 항목을 하나의 문자열로 합칩니다.
                    resulting_text = ' '.join(cleaned_texts)

                    print(resulting_text)
                else:
                    print("logNo not found in the URL.")

                ##################### 블로그의 고유 게시글 번호 가져오기###############################
                
                try:
                    anchor = driver.find_element(By.CSS_SELECTOR,f'#Comi{log_no}').click()
                except:
                    print("댓글창 비활성화 상태입니다.")
                    log_message(f"댓글창 비활성화 상태입니다.")
                    continue
                time.sleep(1)
                print('댓글창 누르기 성공')
                log_message(f"댓글창 누르기 실행")
                try:
                    element = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no}_wai_u_cbox_content_wrap_tabpanel > ul > li > div.u_cbox_comment_box.u_cbox_mine.u_cbox_type_profile > div > div.u_cbox_info > span.u_cbox_info_sub > span > a")
                    print("이미 댓글단 사람입니다.")
                    log_message(f"이미 댓글 단 글입니다.")
                    continue
                except:
                    completenum +=1
                if text_widget_ment.get("1.0","end-1c"):
                    element = driver.find_element(By.XPATH, "//*[contains(text(), '블로그가 더 훈훈해지는 댓글 부탁드립니다. @별명을 입력하면 서로이웃이 소환됩니다.')]")
                    element.click()
                    print("댓글창 활성화 성공")
                    log_message(f"댓글창 활성화 실행")
                    textarea_element = driver.find_element(By.ID, f"naverComment_201_{log_no}__write_textarea")
                    ## 여기서 수정해줘야하고 랜덤으로 넣기
                    comment = random.choice(send_comments_list)
                    log_message(f"지정해둔 댓글중 랜덤으로 골라오기를 실행합니다.")
                    textarea_element.send_keys(f"{comment}")
                    try:
                        send_comments_list.remove(comment)
                    except:
                        send_comments = text_widget_ment.get("1.0","end-1c")
                        send_comments_list = [item.strip() for item in send_comments.split("||")]
                        comment = random.choice(send_comments_list)
                    log_message(f"댓글 리스트에서 추출 완료!")

                    if var_secret.get() == 1:
                        print("비밀댓글 신청합니다")
                        log_message(f"비밀댓글로 댓글을 작성합니다.")
                        secret_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no}__write_textarea_secret_check")
                        secret_button.click()
                    else:
                        print("비밀댓글 신청 안함.")
                    comment_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no} > div > div.u_cbox_write_wrap.u_cbox_writing > div.u_cbox_write_box.u_cbox_type_logged_in > form > fieldset > div > div > div.u_cbox_upload > button")
                    comment_button.click()

                    log_message(f"일반 댓글 달기 완료")

                if gpt.get() == 1:
                    print("gpt 댓글기능 시작")
                    log_message(f"gpt로 댓글달기를 시작합니다.")
                    element = driver.find_element(By.XPATH, "//*[contains(text(), '블로그가 더 훈훈해지는 댓글 부탁드립니다. @별명을 입력하면 서로이웃이 소환됩니다.')]")
                    element.click()
                    print("댓글창 활성화 성공")
                    textarea_element = driver.find_element(By.ID, f"naverComment_201_{log_no}__write_textarea")
                    log_message(f"gpt와 통신중입니다....")
                    comment = gpt_comments(resulting_text)
                    log_message(f"gpt와 통신완료! 댓글을 불러옵니다.")
                    textarea_element.send_keys(f"{comment}")
                    if var_secret.get() == 1 and not text_widget_ment.get("1.0", "end-1c"):
                        print("비밀댓글 신청합니다")
                        log_message(f"비밀댓글로 댓글을 작성합니다.")
                        secret_button = driver.find_element(
                            By.CSS_SELECTOR, f"#naverComment_201_{log_no}__write_textarea_secret_check")
                        secret_button.click()
                    else:
                        print("비밀댓글 신청 안함.")
                    comment_button = driver.find_element(By.CSS_SELECTOR, f"#naverComment_201_{log_no} > div > div.u_cbox_write_wrap.u_cbox_writing > div.u_cbox_write_box.u_cbox_type_logged_in > form > fieldset > div > div > div.u_cbox_upload > button")
                    comment_button.click()
                    log_message(f"gpt댓글 달기 완료!")
                else:
                    pass



                ##########체크박스 조건문, 좋아요 누르기 체크박스####################################################################################
            except:
                print("댓글을 달 수 없는 글입니다.")
#걔네들의 글 목록으로 들어가자.

        


    time.sleep(1)
    
   

def start_threaded_task():
    ###
    # print(type(int(spinbox_send_num.get())))
    # return
    ###
    """ main_start 함수를 별도 스레드에서 실행시키는 함수 """
    thread = Thread(target=main_start)
    thread.start()
    

def show_main_gui(user_id, user_data, current_serial_nickname):
    global main_window
    main_window = tk.Tk()
    main_window.tk.call('tk', 'scaling', 1.5)
    my_font = font.nametofont("TkDefaultFont")
    custom_font = font.Font(font=my_font, file=font_path)
    main_window.title("댓글 작성 프로그램 [오오]")
    main_window.geometry("450x800+1100+100")
    main_window.configure(bg='black')

    main_window.iconbitmap(resource_path('files_comment/myicon.ico'))
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
    
    

    original_image = Image.open(resource_path("files_comment/logo.jpg"))

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

    tk.Label(tab1, text="입력 횟수",font=(custom_font,10,"bold"), fg="white", bg='black').place(x=250, y=40,width=80,height=25)
    global spinbox_send_num
    spinbox_send_num = tk.Spinbox(tab1, from_=1, to=10000, increment=1)
    spinbox_send_num.delete(0, tk.END)  # 스핀박스의 모든 값을 지움
    spinbox_send_num.insert(0, config_requests_num)  # 스핀박스에 100을 입력
    spinbox_send_num.place(x=330, y=40, width=60, height=25) 

    
    tk.Label(tab1, text="사용자 지정 댓글",bg='white', fg='black',font=(custom_font,10,"bold"),underline=9).place(x=10, y=75)
    global text_widget_ment
    text_widget_ment = Text(tab1, wrap=tk.WORD)
    text_widget_ment.insert('1.0',config_comments_list)
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
    if selected_option.get() == "1":
        print(type(selected_option.get()))
    radio1.place(x=10, y=25,height=25,width=60)
    radio2 = tk.Radiobutton(inner_frame, text="이 웃", variable=selected_option, value="2",bg='black',fg='white',selectcolor="black")
    if selected_option.get() == "2":
        print(type(selected_option.get()))
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


    global gpt
    gpt = tk.IntVar(value=int(config_gpt_select))
    gpt_select = tk.Checkbutton(inner_frame_1, text="GPT", variable=gpt,bg='black',fg='white',selectcolor="black")
    gpt_select.place(x=3, y=0,width=60,height=25)

    
    
    global var_secret
    var_secret = tk.IntVar(value=int(config_secret))
    secret = tk.Checkbutton(inner_frame_1, text="비 밀", variable=var_secret,bg='black',fg='white',selectcolor="black")
    secret.place(x=0, y=25,width=60,height=25)
    

    

    tk.Label(tab1, text="로그",bg='white',fg='black',font=(custom_font,10,"bold")).place(x=10, y=370)
    global log_text
    log_text = Text(tab1, wrap=tk.WORD)
    log_text.place(x=10, y=390, width=390, height=100)

    # Scrollbar 위젯 생성
    scrollbar = Scrollbar(tab1, command=text_widget_ment.yview)
    scrollbar.place(x=400, y=390, height=100)
    log_text.config(yscrollcommand=scrollbar.set)

    tk.Label(tab1, text="제외할그룹",font=(custom_font,10,"bold"), fg="white", bg='black').place(x=10, y=500,width=100,height=25)
    global neigbor_entry
    neigbor_entry = ttk.Entry(tab1)
    neigbor_entry.insert("0",config_neighbor_group)
    neigbor_entry.place(x=120, y=500, width=120,height=25)

    tk.Label(tab1, text="프로그램",bg='white',fg='black',font=(custom_font,10,"bold")).place(x=10, y=550)
    inner_frame_2 = ttk.Frame(tab1,width=417,height=1, style="Black.TFrame")
    inner_frame_2.place(x=10,y=545)

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



login_window.title("댓글작성 프로그램 Login")
login_window.geometry("300x200+1100+300")
login_window.configure(bg='white')  # 옅은 초록색 배경
login_window.iconbitmap(resource_path('files_comment/myicon.ico'))

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






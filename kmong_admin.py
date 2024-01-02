import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from tkcalendar import DateEntry
from tkcalendar import Calendar
from datetime import datetime, timedelta
import os
import psutil
# fire base 초기화 하는 부분
mykey1 = {

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

cred = credentials.Certificate(mykey1)
firebase_app1 = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://blog-95f26-default-rtdb.firebaseio.com/'
})

# 바꿔야할 부분들
mykey2 = {
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
cred2 = credentials.Certificate(mykey2)
firebase_app2 = firebase_admin.initialize_app(cred2, {
    'databaseURL': 'https://comment-5b3fe-default-rtdb.firebaseio.com/'
}, name='comment-5b3fe')


# 사용자 인증 부분
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


cred3 = credentials.Certificate(programManageKey)
firebase_app3 = firebase_admin.initialize_app(cred3, {
    'databaseURL': 'https://programmanage-bd683-default-rtdb.firebaseio.com/'
}, name='programmanage-bd683')
# 사용자 인증 부분

ref0 = db.reference("/user_info", app=firebase_app1)  # db 위치 지정, 기본 가장 상단을 가르킴
data0 = ref0.get()
# print("------------------------------------------------------------------------------------------------------")

ref1 = db.reference("/user_info", app=firebase_app2)
data1 = ref1.get()

ref3 = db.reference("/program_list", app=firebase_app3)
# print(data1)

style_options = {
    "bg": "#4E71F4",  # 버튼의 배경색
    "fg": "white",  # 버튼의 글자색
    "font": ("Arial", 10, "bold"),  # 글꼴, 크기, 스타일
    "relief": "flat",  # 버튼의 테두리 스타일
    "activebackground": "#6375D6",  # 버튼에 마우스를 올렸을 때의 배경색
    "activeforeground": "white"  # 버튼에 마우스를 올렸을 때의 글자색
}


def validate_spinbox_input(value):
    # 만약 값이 숫자가 아니거나 1 미만일 경우 거부
    if not value.isdigit() or int(value) < 1:
        return False
    return True


def check_expiry(expiry_date_str):
    # 현재 날짜 구하기
    current_date = datetime.now().date()
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
    # 만료일과 현재 날짜의 차이 계산
    days_until_expiry = (expiry_date - current_date).days

    if days_until_expiry > 0:
        print(f"유효 기간이 {days_until_expiry}일 남았습니다.")

    elif days_until_expiry == 0:
        print("오늘까지가 유효 기간입니다.")
    else:
        print("유효 기간이 이미 만료되었습니다.")
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()

# check_expiry('2023-08-28')
# 데이터 등록 함수


def register_data():
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
        ref_to_use = ref0
        data_to_use = data0
    elif current_tab_index == 1:
        tree_to_use = tree2
        ref_to_use = ref1
        data_to_use = data1

    current_tab_index = get_current_tab_index()
    user_id = user_id_entry.get()
    date = date_entry.get()
    pc_count = int(pc_spinbox.get())
    id_count = int(id_spinbox.get())

    if not user_id or not date:
        messagebox.showerror("Error", "모든 필드를 입력해주세요.")
        return

    # 입력한 pc_count에 맞게 None 값을 가진 리스트 생성
    computer_serial_list = ["None" for _ in range(pc_count)]

    # 입력한 id_count에 맞게 None 값을 가진 리스트 생성
    naver_id_list = ["None" for _ in range(id_count)]

    # 아이디 중복 체크
    data_to_use = ref_to_use.get()
    if any(user_id in user_info for user_info in data_to_use.values()):
        messagebox.showerror("Error", "중복된 아이디입니다.")
        return

    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1

    ref_to_use.push({
        user_id: {
            "computer_serial": computer_serial_list,
            'date': date,
            'permissioned_computer': pc_count,
            'naver_id_permission': id_count,
            'naver_id_list': naver_id_list
        }
    })

    messagebox.showinfo("Info", "데이터가 성공적으로 등록되었습니다.")
    selected_tab_index = notebook.index(notebook.select())
    print(f'Tab changed to: {selected_tab_index}')
    if selected_tab_index == 0:
        data_to_use = ref0.get()
    elif selected_tab_index == 1:
        data_to_use = ref1.get()
    selected_tab_id = notebook.select()
    selected_tab_title = notebook.tab(selected_tab_id, 'text')
    print(selected_tab_title, '의 등록회원 수 = ', len(data_to_use))
    user_number_label = tk.Label(
        root, text=f"등록회원 수 = {len(data_to_use)}", **style_options)
    user_number_label.place(x=467, y=155, width=155, height=50)

    # Treeview의 현재 항목 모두 삭제
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2

    for item in tree_to_use.get_children():
        tree_to_use.delete(item)

    # 데이터베이스에서 데이터 다시 가져오기
    data = ref_to_use.get()
    try:
        for user_id, details in data.items():
            for kk, user_info in details.items():
                tree_to_use.insert("", "end", values=(
                    kk, user_info["date"], user_info["permissioned_computer"], user_info["naver_id_permission"]))
    except:
        pass

    # Entry 위젯 초기화
    entry_initialize()


# 검색 함수
def search_id():
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2
    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1
    search_value = search_id_entry.get()
    for item in tree_to_use.get_children():
        if tree_to_use.item(item, 'values')[0] == search_value:
            tree_to_use.selection_set(item)  # 해당 항목을 선택합니다.
            tree_to_use.see(item)            # 해당 항목이 화면에 보이도록 합니다.
            return
    messagebox.showinfo("Info", "해당 아이디를 찾을 수 없습니다.")  # 검색 결과가 없을 경우 메시지 출력

    # 입력창 초기화
    user_id_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    pc_spinbox.delete(0, tk.END)
    pc_spinbox.insert(0, "0")


def on_item_double_click(event):
    print("더블 클릭 이벤트를 실행합니다.")
    edit_item()


def delete_item():
    print("삭제를 실행합니다.")
    delete_selected_data()

    # 삭제 작업을 수행할 코드를 여기에 작성하세요.


def get_current_tab_index():
    # 현재 선택된 탭의 인덱스를 반환합니다.
    return notebook.index(notebook.select())


# 데이터 삭제 함수
def delete_selected_data():
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2
    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1
    # 현재 선택된 항목의 user_id를 가져옵니다.
    selected_item = tree_to_use.selection()[0]  # 선택된 항목들 중 첫 번째 항목
    target_user_id = tree_to_use.item(selected_item, "values")[
        0]  # 첫 번째 column의 값

    # Firebase에서 데이터 가져오기
    data = ref_to_use.get()

    # 해당 user_id를 가진 데이터의 키 찾기
    for key, user_info in data.items():
        if target_user_id in user_info:
            # 키를 사용하여 데이터 삭제
            ref_to_use.child(key).delete()
            print(f"Deleted data for {target_user_id} with key {key}")

    # Treeview에서 항목 삭제
    tree_to_use.delete(selected_item)

    # 사용자에게 메시지 표시
    messagebox.showinfo("Info", "데이터가 성공적으로 삭제되었습니다.")
    selected_tab_index = notebook.index(notebook.select())
    print(f'Tab changed to: {selected_tab_index}')
    if selected_tab_index == 0:
        data_to_use = ref0.get()
    elif selected_tab_index == 1:
        data_to_use = ref1.get()
    selected_tab_id = notebook.select()
    selected_tab_title = notebook.tab(selected_tab_id, 'text')
    print(selected_tab_title, '의 등록회원 수 = ', len(data_to_use))
    user_number_label = tk.Label(
        root, text=f"등록회원 수 = {len(data_to_use)}", **style_options)
    user_number_label.place(x=467, y=155, width=155, height=50)


def edit_item():
    global spinrestrict
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2
    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1
    spinrestrict = 0
    # 현재 선택된 항목의 user_id를 가져옵니다.
    selected_item = tree_to_use.selection()[0]  # 선택된 항목들 중 첫 번째 항목
    target_user_id = tree_to_use.item(selected_item, "values")[
        0]  # 첫 번째 column의 값

    # Firebase에서 해당 user_id의 데이터 가져오기
    data = ref_to_use.get()
    user_info = None
    for key, user_data in data.items():
        if target_user_id in user_data:
            user_info = user_data[target_user_id]
            target_key = key
            break

    if not user_info:
        messagebox.showinfo("Error", "데이터를 찾을 수 없습니다.")
        return

    # 새로운 창 생성
    edit_window = tk.Toplevel(root)
    edit_window.geometry("400x600+1100+300")
    edit_window.title(f"Edit Information for {target_user_id}")

    # 날짜 위젯
    edit_date_label = tk.Label(edit_window, text="날짜:")
    edit_date_label.place(x=10, y=10)
    edit_date_entry = DateEntry(edit_window, date_pattern='y-mm-dd',
                                background='darkblue', foreground='white', borderwidth=2)
    edit_date_entry.set_date(user_info['date'])  # 원래 데이터로 설정
    edit_date_entry.place(x=80, y=10)

    # Date extension widgets
    extension_spinbox = tk.Spinbox(
        edit_window, from_=-24, to=24, increment=1, width=3)
    extension_spinbox.delete(0, tk.END)
    extension_spinbox.insert(0, "1")
    extension_spinbox.place(x=190, y=10)

    month_label = tk.Label(edit_window, text="달")
    month_label.place(x=240, y=7)

    def extend_date():
        try:
            current_date = datetime.strptime(edit_date_entry.get(), "%Y-%m-%d")
            # assuming 30 days in a month
            extended_date = current_date + \
                timedelta(days=int(extension_spinbox.get()) * 30)
            edit_date_entry.set_date(extended_date.date())
        except ValueError:
            messagebox.showerror("Error", "날짜 형식이 잘못되었습니다.")
    extend_button = tk.Button(edit_window, text="연장",
                              command=extend_date, **style_options)
    extend_button.place(x=260, y=5)

    def update_computer_serials():
        current_pc_value = int(edit_pc_spinbox.get())
        current_listbox_size = edit_cs_listbox.size()

        if current_listbox_size == 1 and current_pc_value == 1:
            return

        none_indices = [i for i, value in enumerate(
            edit_cs_listbox.get(0, tk.END)) if value == "None"]

        if current_pc_value > current_listbox_size:
            for _ in range(current_pc_value - current_listbox_size):
                edit_cs_listbox.insert(tk.END, "None")
        else:
            # None 값들을 먼저 삭제합니다.
            for index in reversed(none_indices):
                edit_cs_listbox.delete(index)
                current_listbox_size -= 1  # listbox 크기 감소

                if current_listbox_size == current_pc_value:
                    break

            # 여전히 줄여야 할 항목이 있다면, 마지막 항목부터 삭제
            non_none_items = [edit_cs_listbox.get(i) for i in range(
                current_listbox_size) if edit_cs_listbox.get(i) != "None"]

            if len(non_none_items) > current_pc_value:
                # parent를 edit_window로 설정
                messagebox.showinfo(
                    "Error", "먼저 등록된 컴퓨터를 먼저 초기화 해주세요.", parent=edit_window)
                # spinbox 값을 +1 증가
                edit_pc_spinbox.delete(0, tk.END)
                edit_pc_spinbox.insert(0, current_pc_value + 1)
                return

            for _ in range(current_listbox_size - current_pc_value):
                edit_cs_listbox.delete(tk.END)

    def delete_selected_serial():
        selected_serial = edit_cs_listbox.curselection()
        if selected_serial:
            edit_cs_listbox.delete(selected_serial)
            edit_cs_listbox.insert(selected_serial, "None")

    def update_id_list():
        current_id_value = int(edit_naver_id_spinbox.get())
        current_listbox_size = naver_id_listbox.size()

        if current_listbox_size == 1 and current_id_value == 1:
            return

        none_indices = [i for i, value in enumerate(
            naver_id_listbox.get(0, tk.END)) if value == "None"]

        if current_id_value > current_listbox_size:
            for _ in range(current_id_value - current_listbox_size):
                naver_id_listbox.insert(tk.END, "None")
        else:
            # None 값들을 먼저 삭제
            for index in reversed(none_indices):
                naver_id_listbox.delete(index)
                current_listbox_size -= 1  # listbox 크기 감소

                if current_listbox_size == current_id_value:
                    break

            # 여전히 줄여야 할 항목이 있다면, 마지막 항목부터 삭제
            non_none_items = [naver_id_listbox.get(i) for i in range(
                current_listbox_size) if naver_id_listbox.get(i) != "None"]

            if len(non_none_items) > current_id_value:
                # parent를 edit_window로 설정
                messagebox.showinfo(
                    "Error", "먼저 등록된 아이디를 먼저 초기화 해주세요.", parent=edit_window)
                edit_naver_id_spinbox.delete(0, tk.END)
                edit_naver_id_spinbox.insert(0, current_id_value + 1)
                # spinbox 값을 +1 증가

                return

            for _ in range(current_listbox_size - current_id_value):
                naver_id_listbox.delete(tk.END)

    def delete_selected_naver_id():
        selected_id = naver_id_listbox.curselection()
        if selected_id:
            naver_id_listbox.delete(selected_id)
            naver_id_listbox.insert(selected_id, "None")

    def on_naver_id_double_click(event):
        idx = naver_id_listbox.curselection()  # 선택된 항목의 인덱스 가져오기
        if not idx:  # 아무 것도 선택되지 않은 경우
            return
        idx = idx[0]
        value = naver_id_listbox.get(idx)  # 선택된 항목의 값 가져오기

        # Entry 위젯 생성 및 설정
        edit_entry = tk.Entry(edit_window,
                              bg="lightyellow",  # 배경색 설정
                              bd=2,  # 테두리 두께 설정
                              relief="solid",  # 테두리 스타일 설정
                              highlightbackground="red",  # 포커스가 없을 때의 테두리 색상
                              highlightcolor="blue",  # 포커스가 있을 때의 테두리 색상
                              highlightthickness=2)
        edit_entry.insert(0, value)

        item_height = naver_id_listbox.bbox(idx)[3]

        y_position = 290 + \
            (idx - int(naver_id_listbox.nearest(0))) * item_height
        # 항목 하나의 높이 계산

        # Entry의 위치 설정
        edit_entry.place(x=10, y=y_position, width=280)
        edit_entry.focus()

        # Entry 내에서 Enter 키 이벤트 핸들러
        def on_entry_enter(event):
            naver_id_listbox.delete(idx)
            naver_id_listbox.insert(idx, edit_entry.get())
            edit_entry.destroy()  # Entry 위젯 제거

        # Entry 위젯에 Enter 키 이벤트 바인딩
        edit_entry.bind('<Return>', on_entry_enter)
        # Entry 위젯에 포커스 손실 이벤트 바인딩
        edit_entry.bind('<FocusOut>', on_entry_enter)

    # Permissioned Computer Spinbox
    edit_pc_label = tk.Label(edit_window, text="등록 가능한 pc수")
    edit_pc_label.place(x=10, y=50)
    edit_pc_spinbox = tk.Spinbox(edit_window, from_=1, to=100, increment=1)
    edit_pc_spinbox.delete(0, tk.END)
    edit_pc_spinbox.insert(0, user_info['permissioned_computer'])  # 원래 데이터로 설정
    edit_pc_spinbox.place(x=150, y=50)
    edit_pc_spinbox.config(command=update_computer_serials)

    # "등록 가능한 네이버 아이디" 레이블 및 스핀박스 추가
    edit_naver_id_label = tk.Label(edit_window, text="등록 가능한 네이버 아이디:")
    edit_naver_id_label.place(x=10, y=80)
    # 기본값 설정
    naver_id_permission_default_value = user_info['naver_id_permission']
    edit_naver_id_spinbox = tk.Spinbox(
        edit_window, from_=1, to=100, increment=1)
    edit_naver_id_spinbox.delete(0, tk.END)
    edit_naver_id_spinbox.insert(0, naver_id_permission_default_value)
    edit_naver_id_spinbox.place(x=150, y=80)
    edit_naver_id_spinbox.config(command=update_id_list)

    # Computer Serial Listbox and Scrollbar
    edit_cs_label = tk.Label(edit_window, text="컴퓨터 Serials:")
    edit_cs_label.place(x=10, y=120)

    scrollbar = tk.Scrollbar(edit_window, orient=tk.VERTICAL)
    edit_cs_listbox = tk.Listbox(edit_window, yscrollcommand=scrollbar.set)

    for serial in user_info['computer_serial']:
        edit_cs_listbox.insert(tk.END, serial)
    edit_cs_listbox.place(x=10, y=150, width=280, height=100)

    scrollbar.config(command=edit_cs_listbox.yview)
    scrollbar.place(x=290, y=150, height=100)

    edit_delete_button = tk.Button(
        edit_window, text="삭제", command=delete_selected_serial, **style_options)
    edit_delete_button.place(x=320, y=150)

    # 네이버 ID 리스트 리스트박스 및 삭제 버튼 추가
    edit_naver_id_label = tk.Label(edit_window, text="네이버 ID 리스트:")
    edit_naver_id_label.place(x=10, y=260)

    naver_id_listbox = tk.Listbox(edit_window)
    naver_id_listbox.bind("<Double-Button-1>", on_naver_id_double_click)
    naver_id_listbox.place(x=10, y=290, width=280, height=100)

    naver_id_scrollbar = tk.Scrollbar(edit_window, orient=tk.VERTICAL)
    naver_id_scrollbar.config(command=naver_id_listbox.yview)
    naver_id_scrollbar.place(x=290, y=290, height=100)

    naver_id_listbox.config(yscrollcommand=naver_id_scrollbar.set)
    # 'naver_id_list'라는 키가 데이터에 있을 경우 리스트를 불러옵니다.
    for naver_id in user_info.get('naver_id_list', []):
        naver_id_listbox.insert(tk.END, naver_id)

    edit_delete_naver_id_button = tk.Button(
        edit_window, text="삭제", command=delete_selected_naver_id, **style_options)
    edit_delete_naver_id_button.place(x=320, y=290)

    # 저장 버튼
    def save_changes():
        current_tab_index = get_current_tab_index()
        if current_tab_index == 0:
            tree_to_use = tree1
            ref_to_use = ref0
            data_to_use = data0
        elif current_tab_index == 1:
            tree_to_use = tree2
            ref_to_use = ref1
            data_to_use = data1

        updated_date = edit_date_entry.get()
        updated_pc = int(edit_pc_spinbox.get())
        updated_serials = [edit_cs_listbox.get(
            i) for i in range(edit_cs_listbox.size())]
        updated_id_count = int(edit_naver_id_spinbox.get())
        updated_id_list = [naver_id_listbox.get(
            i) for i in range(naver_id_listbox.size())]

        # Firebase에 저장
        ref_to_use.child(target_key).set({
            target_user_id: {
                "computer_serial": updated_serials,
                'date': updated_date,
                'permissioned_computer': updated_pc,
                'naver_id_list': updated_id_list,
                'naver_id_permission': updated_id_count

            }
        })

        # Treeview 갱신
        for item in tree_to_use.get_children():
            tree_to_use.delete(item)
        data = ref_to_use.get()
        try:
            for user_id, details in data.items():
                for kk, user_info in details.items():
                    tree_to_use.insert("", "end", values=(
                        kk, user_info["date"], user_info["permissioned_computer"], user_info["naver_id_permission"]))
        except:
            pass

        messagebox.showinfo("Info", "데이터가 성공적으로 수정되었습니다.")

      # Save button design and positioning
    edit_save_button = tk.Button(edit_window, text="저장", command=save_changes,
                                 bg="#3D9BF0", fg="white", font=('Arial', 10, 'bold'), relief=tk.GROOVE, bd=3)
    edit_save_button.place(x=10, y=550, width=380, height=40)


def on_item_right_click(event):
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2
    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1
    # 마우스로 클릭한 위치의 항목을 가져온다
    clicked_item = tree_to_use.identify_row(event.y)

    # 클릭한 항목을 선택한다
    tree_to_use.selection_set(clicked_item)

    # 마우스 포인터 위치에 메뉴를 표시한다
    popup_menu.post(event.x_root, event.y_root)


def root_click(event):
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2
    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1
    widget = root.winfo_containing(event.x_root, event.y_root)

    if widget == search_button:
        return

    if widget not in [tree_to_use, register_button]:
        tree_to_use.selection_remove(tree_to_use.selection())


def view_info():
    current_tab_index = get_current_tab_index()
    if current_tab_index == 0:
        tree_to_use = tree1
    elif current_tab_index == 1:
        tree_to_use = tree2
    if current_tab_index == 0:
        ref_to_use = ref0
    elif current_tab_index == 1:
        ref_to_use = ref1
    print("정보보기를 실행합니다.")

    # 현재 선택된 항목의 user_id를 가져오기
    selected_item = tree_to_use.selection()[0]
    target_user_id = tree_to_use.item(selected_item, "values")[0]

    # Firebase에서 해당 user_id의 데이터 가져오기
    data = ref_to_use.get()
    user_info = None
    for key, user_data in data.items():
        if target_user_id in user_data:
            user_info = user_data[target_user_id]
            break

    if user_info:
        # 새로운 tkinter 창을 생성하고 정보를 표시합니다.
        info_window = tk.Toplevel(root)
        info_window.geometry("400x300+1100+300")
        info_window.title(f"Information for {target_user_id}")
        info_window.configure(bg='#87CEFA')  # 배경색 변경

        font_style = ("Arial", 12)  # 글꼴 및 크기 설정

        user_id_label = tk.Label(
            info_window, text=f"아이디: {target_user_id}", font=font_style, bg='#87CEFA')
        user_id_label.place(x=50, y=20)

        date_label = tk.Label(
            info_window, text=f"만료날짜: {user_info['date']}", font=font_style, bg='#87CEFA')
        date_label.place(x=50, y=60)

        pc_count_label = tk.Label(
            info_window, text=f"등록가능대수: {user_info['permissioned_computer']}", font=font_style, bg='#87CEFA')
        pc_count_label.place(x=50, y=100)

        naver_id_permission_label = tk.Label(
            info_window, text=f"등록된 아이디개수: {user_info['naver_id_permission']}", font=font_style, bg='#87CEFA')
        naver_id_permission_label.place(x=50, y=140)

        computer_combobox = ttk.Combobox(
            info_window, values=user_info['computer_serial'], state="readonly", font=font_style)
        computer_combobox.set("등록된 컴퓨터 리스트")
        computer_combobox.place(x=50, y=180, width=300)

        naver_id_combobox = ttk.Combobox(
            info_window, values=user_info['naver_id_list'], state="readonly", font=font_style)
        naver_id_combobox.set("등록된 아이디 리스트")
        naver_id_combobox.place(x=50, y=220, width=300)

    else:
        messagebox.showinfo("Error", "데이터를 찾을 수 없습니다.")


def update_date():
    # Spinbox의 현재 값 가져오기
    offset = int(date_spinbox.get())

    # DateEntry의 현재 날짜 가져오기
    current_date = date_entry.get_date()

    # DateEntry에 새로운 날짜 설정하기
    new_date = current_date + timedelta(days=offset*30)  # 한달씩 추가/감소
    date_entry.set_date(new_date)


def entry_initialize():
    user_id_entry.delete(0, tk.END)  # 모든 내용 삭제
    date_entry.delete(0, tk.END)  # 모든 내용 삭제
    date_spinbox .delete(0, tk.END)
    date_spinbox .insert(0, "0")
    pc_spinbox .delete(0, tk.END)
    pc_spinbox .insert(0, "1")
    id_spinbox .delete(0, tk.END)
    id_spinbox .insert(0, "1")

    # 오늘 날짜를 "YYYY-MM-DD" 형식으로 가져오기
    today_date = datetime.today().strftime('%Y-%m-%d')
    date_entry.insert(0, today_date)  # 오늘 날짜로 초기화


def on_tab_changed(event):
    selected_tab_index = notebook.index(notebook.select())
    print(f'Tab changed to: {selected_tab_index}')
    if selected_tab_index == 0:
        data_to_use = data0
    elif selected_tab_index == 1:
        data_to_use = data1
    selected_tab_id = notebook.select()
    selected_tab_title = notebook.tab(selected_tab_id, 'text')
    print(selected_tab_title, '의 등록회원 수 = ', len(data_to_use))
    user_number_label = tk.Label(
        root, text=f"등록회원 수 = {len(data_to_use)}", **style_options)
    user_number_label.place(x=467, y=155, width=155, height=50)

def checkProgram():
    program_manage = ref3.child('OO').get()
    print(program_manage)
    if program_manage == 1:
        print("현재실행 가능함")
    else:
        print("현재 실행 불가능함")
        root.destroy()
        return
root = tk.Tk()
root.geometry("621x600+1100+300")
root.title("Firebase Data Viewer")
root.configure(bg='#ebc034')
# 위의 함수를 Tcl wrapper로 변환
validate_cmd = root.register(validate_spinbox_input)

treeview_frame = tk.Frame(root, bg="lightgray", bd=2, relief="groove")
treeview_frame.place(x=0, y=0, width=450, height=320)  # 위치와 크기를 조절하세요.

notebook = ttk.Notebook(treeview_frame)
notebook.pack(expand=True, fill='both')

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text='서이추 관리창')
notebook.add(tab2, text='댓글달기 관리창')

# 첫번째 트리뷰 생성하는곳
tree1 = ttk.Treeview(tab1, columns=(
    "user_id", "date", "permissioned_computer", "permissioned_id"), show="headings", height=500)

tree1.heading("user_id", text="user_id")
tree1.heading("date", text="date")
tree1.heading("permissioned_computer", text="permissioned_computer")
tree1.heading("permissioned_id", text="permissioned_id")

tree1.column("user_id", width=40)
tree1.column("date", width=40)
tree1.column("permissioned_computer", width=90)
tree1.column("permissioned_id", width=80)


try:
    for user_id, details in data0.items():
        for kk, user_info in details.items():
            tree1.insert("", "end", values=(
                kk, user_info["date"], user_info["permissioned_computer"], user_info["naver_id_permission"]))
except:
    pass

tree1.place(x=0, y=0, width=600, height=300)

scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=tree1.yview)
scrollbar.place(x=430, y=0, height=300)

tree1.configure(yscrollcommand=scrollbar.set)
tree1.place(x=0, y=0, width=430, height=300)

# 두번째 트리뷰 생성하는곳
tree2 = ttk.Treeview(tab2, columns=(
    "user_id", "date", "permissioned_computer", "permissioned_id"), show="headings", height=500)

tree2.heading("user_id", text="user_id")
tree2.heading("date", text="date")
tree2.heading("permissioned_computer", text="permissioned_computer")
tree2.heading("permissioned_id", text="permissioned_id")

tree2.column("user_id", width=40)
tree2.column("date", width=40)
tree2.column("permissioned_computer", width=90)
tree2.column("permissioned_id", width=80)


try:
    for user_id, details in data1.items():
        for kk, user_info in details.items():
            tree2.insert("", "end", values=(
                kk, user_info["date"], user_info["permissioned_computer"], user_info["naver_id_permission"]))
except:
    pass

tree2.place(x=0, y=0, width=600, height=300)

scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=tree2.yview)
scrollbar.place(x=430, y=0, height=300)

tree2.configure(yscrollcommand=scrollbar.set)
tree2.place(x=0, y=0, width=430, height=300)


entry_frame = tk.Frame(root, bg="lightgray", bd=2, relief="groove")
entry_frame.place(x=0, y=350, width=617, height=150)

# User ID 레이블 및 Entry
user_id_label = tk.Label(entry_frame, text="아이디:")
user_id_label.place(x=10, y=20)
user_id_entry = tk.Entry(entry_frame)
user_id_entry.place(x=70, y=20, width=100)

# Date 레이블 및 DateEntry
date_label = tk.Label(entry_frame, text="날짜")
date_label.place(x=200, y=20)  # 위치 조정
date_entry = DateEntry(entry_frame, date_pattern='y-mm-dd',
                       background='darkblue', foreground='white', borderwidth=2)
date_entry.place(x=250, y=20, width=100)  # 위치 조정

# Date 레이블 옆에 spinbox 추가
date_spinbox = tk.Spinbox(entry_frame, from_=0, to=12, increment=1,
                          command=update_date) 
date_spinbox .delete(0, tk.END)
date_spinbox .insert(0, "0")
date_spinbox.place(x=250, y=50, width=50)


# Permissioned Computer 레이블 및 Entry
pc_label = tk.Label(entry_frame, text="등록가능한 pc수")
pc_label.place(x=360, y=20)
pc_spinbox = tk.Spinbox(entry_frame, from_=1, to=100,
                        increment=1)  
pc_spinbox.place(x=460, y=20, width=50)

naver_id_label = tk.Label(entry_frame, text="네이버 id수")
naver_id_label.place(x=360, y=50)
id_spinbox = tk.Spinbox(entry_frame, from_=1, to=100, increment=1)
id_spinbox.place(x=460, y=50, width=50)

# 등록 버튼
register_button = tk.Button(
    entry_frame, text="신규등록", command=register_data, **style_options)
register_button.place(x=10, y=50, width=60, height=30)

register_button = tk.Button(entry_frame, text="초기화",
                            command=entry_initialize, **style_options)
register_button.place(x=75, y=50, width=60, height=30)

# 검색, 등록 프레임
entry_frame_1 = tk.Frame(root, bg="lightgray", bd=2, relief="groove")
entry_frame_1.place(x=467, y=0, width=155, height=150)

# 검색용 아이디 입력 Entry
search_id_label = tk.Label(entry_frame_1, text="검색 아이디:")
search_id_label.place(x=10, y=10)
search_id_entry = tk.Entry(entry_frame_1)
search_id_entry.place(x=10, y=30, width=130)


# Treeview에 오른쪽 클릭 이벤트를 바인딩합니다.
tree1.bind("<Button-3>", on_item_right_click)

# 더블클릭 이벤트 바인딩
tree1.bind("<Double-1>", on_item_double_click)

tree2.bind("<Button-3>", on_item_right_click)

# 더블클릭 이벤트 바인딩
tree2.bind("<Double-1>", on_item_double_click)

# root 클릭 이벤트 바인딩
root.bind("<Button-1>", root_click)

# 노트북 선택 클릭 이벤트 바인딩
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)


# 팝업 메뉴 생성
popup_menu = tk.Menu(root, tearoff=0)
popup_menu.add_command(label="삭제", command=delete_item)
popup_menu.add_command(label="수정", command=edit_item)
popup_menu.add_command(label="정보보기", command=view_info)


# 검색 버튼
search_button = tk.Button(entry_frame_1, text="검색",
                          command=search_id, **style_options)
search_button.place(x=10, y=60, width=60, height=30)

root.after(5000, checkProgram)
root.mainloop()

###########################################################################################

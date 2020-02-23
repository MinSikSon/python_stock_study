import win32com.client
import ctypes

import os
# from pywinauto import application # python 3.x 에서 사용 불가
import subprocess

from time import sleep

from stock import login

class Connection:
    def __init__(self, logging=False):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.logging = logging

    def do_connect(self):
        bConnect = self.check_connect()
        if bConnect == False:
            self.kill_creon()
            bConnect = self.run_creon(login.id, login.pwd, login.pwdcert)
        return bConnect

    def check_connect(self):
        bIsConnected = False

        if ctypes.windll.shell32.IsUserAnAdmin() == False:
            print("[check_connect] 오류: 관리자 권한으로 실행하세요")
            return False

        if self.logging == True:
            print("[check_connect] 정상: 관리자 권한으로 실행된 프로세스")

        # 연결 상태 확인
        if self.instCpCybos.IsConnect == 1:
            bIsConnected = True
            if self.logging == True:
                print("[check_connect] connect! (ret : %s)" % bIsConnected)
        else :
            bIsConnected = False
            print("[check_connect] fail.. (ret : %s)" % bIsConnected)
            
        return bIsConnected

    def kill_creon(self):
        print('[kill_creon]')
        os.system('taskkill /IM coStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    def run_creon(self, id, pwd, pwdcert):
        print('[run_creon]')
        cmd = [
            'powershell.exe', 
            'C:\CREON\STARTER\coStarter.exe /prj:cp /id:%s /pwd:%s /pwdcert:%s /autostart' % (id, pwd, pwdcert),
            'Start-Process', 
            ]
        subprocess.run(cmd, shell=True)
        while not self.check_connect():
            sleep(1)
        return True
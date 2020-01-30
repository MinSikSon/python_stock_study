import win32com.client
import ctypes

class Connection:
    def __init__(self, logging=False):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.logging = logging

    def check_connect(self):
        if ctypes.windll.shell32.IsUserAnAdmin():
            if self.logging == True:
                print("[check_connect] 정상: 관리자 권한으로 실행된 프로세스")
        else:
            print("[check_connect] 오류: 관리자 권한으로 실행하세요")
        bConnect = self.instCpCybos.IsConnect
        if bConnect == 1:
            if self.logging == True:
                print("[check_connect] connect! (ret : %s)" % bConnect)
        else :
            print("[check_connect] fail.. (ret : %s)" % bConnect)
            
        return bConnect
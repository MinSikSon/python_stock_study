import win32com.client
import ctypes

class Connection:
    def __init__(self, logging=False):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.logging = logging

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
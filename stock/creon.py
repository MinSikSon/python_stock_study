import win32com.client

TRUE = 1
FALSE = 0

class Creon:
    def __init__(self):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        print(self.instCpCybos)
        
        self.instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
        print(self.instCpStockCode)

    def check_connect(self):
        bConnect = self.instCpCybos.IsConnect
        if bConnect == 1:
            print("[check_connect] connect! %s" % bConnect)
        else :
            print("[check_connect] fail.. %s" % bConnect)
        return bConnect

    def get_code_from_name(self, name):
        return self.instCpStockCode.NameToCode(name)

    def get_name_from_code(self, code):
        return self.instCpStockCode.CodeToName(code)

if __name__ == '__main__':
    stCreon = Creon()
    bConnect = stCreon.check_connect()

    if bConnect == TRUE :
        code = stCreon.get_code_from_name('삼성전자')
        print("삼성전자 code : %s" % code)

        name = stCreon.get_name_from_code(code)
        print("삼성전자 name : %s" % name)

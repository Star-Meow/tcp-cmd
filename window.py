from tkinter import *
import tkinter.ttk as ttk
import socket
import time

root = Tk()
root.title("燈光控制視窗")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("10.32.21.1", 502))
clientSocket.settimeout(500)

class Color:
    SKY_WHITE = [0, 0x64]      # 藍天白，1 Mired = 1000000/10000K=100=0064(16進制)
    FLOWER_WHITE = [0, 0xa6]   # 花白色，1 Mired = 1000000/6000K=166=00a6(16進制)
    DAY = [0, 0xc8]            # 晝光色，1 Mired = 1000000/5000K=200=00c8(16進制)
    WARM_WHITE = [1, 0x4d]     # 暖白色，1 Mired = 1000000/3000K=333=014d(16進制)
    YELLOW_WHITE = [1, 0x90]   # 黃白色，1 Mired = 1000000/2500K=400=0190(16進制)
    CANDLE = [1, 0xf4]         # 燭光色，1 Mired = 1000000/2000K=500=01f4(16進制)

def checksum(*args) -> int:  # 定義checksum為字串或數字
    return sum(args) % 256  # 加總get_payload的參數 % 256

def getP():
    p = entryPostion.get()
    return p

def getB():
    b = scaleBrightness.get() 
    return b

def getV():
    v = openCB.get()
    return v    
    

def LightON():
    print(tcp_dali_cmd(command_code=1, address=int(getP()), command=[5]))
    return 

def LightOFF():
    print(tcp_dali_cmd(command_code=1, address=int(getP()), command=[0]))
    return 

def Brightness():
    print(tcp_dali_cmd(command_code=1, address=int(getP()), command=[int(getB())]))
    return

def Temp():
    return

def GpIn():
    return
def GpOut():
    return

def check():
    print(getP(),getB())

def tcp_dali_cmd(index_hi=0x00, index_lo=0x00, type_cmd=0x00,
                 gateway_id=0xff, command_code=0x01, address=0xff, command=[0x00]):  # 定義TCP指令參數及預設值，並以 16 進制讀取

    cmd_msg = bytearray()           # 加入參數將以bytearry方式發送指令
    cmd_msg.append(index_hi)        # 流水號HighByte
    cmd_msg.append(index_lo)        # 流水號LowByte
    cmd_msg.append(type_cmd)        # command=0,query=1
    cmd_msg.append(1)               # fixed
    cmd_msg.append(0)               # fixed
    cmd_msg.append(4+len(command))  # DALI-485 command Length=5 bytes
    cmd_msg.append(gateway_id)      # gateway_id
    cmd_msg.append(command_code)    # dimming：0x00,Normal control:0c01,temperature:0x06
    cmd_msg.append(address)         # broadcast：0xff,group:0xc0-0xcf,single:0x00-0x3f
    for index in command:           # 透過for把list分割加入bytearray()
        cmd_msg.append(index)
    cmd_msg.append(checksum(gateway_id, command_code, address, *command))  # 計算checksum並代入指令

    return cmd_msg


w,h = 600,400
#取螢幕大小
screenWidth = root.winfo_screenwidth()
screenHeigh = root.winfo_screenheight()
x = (screenWidth - w)/2 #視窗左上角X軸
y = (screenHeigh - h)/2 #視窗右上角Y軸
root.geometry("%dx%d+%d+%d"%(w,h,x,y))#產生依照whxy的視窗



btnON = Button(root, text = '開燈',bg= 'yellow',command = LightON)
btnOFF = Button(root, text = '關燈',bg= 'gray',command = LightOFF)
btnBrightness = Button(root, text = '亮度',bg= 'yellow',command = Brightness)
btnTemp = Button(root, text = '色溫控制',bg= 'orange',command = Temp)
btnGpIn = Button(root, text = '進群',bg= 'yellow',command = GpIn)
btnGpOut = Button(root, text = '退群',bg= 'yellow',command = GpOut)
btnDestory = Button(root, text ="關閉視窗",bg= 'gray', command = root.destroy) 
btnCheck = Button(root, text ="檢查",bg= 'gray', command = check) 

btnON.grid(row = 0, column = 1,ipadx = 50, ipady=5,padx=50, pady=10, sticky = NSEW)    
btnOFF.grid(row = 2, column = 1,ipadx = 50, ipady=5,padx=50, pady=10, sticky = NSEW)
btnBrightness.grid(row = 4, column = 1,ipadx = 50, ipady=5,padx=50, pady=10, sticky = NSEW)
btnTemp.grid(row = 6, column = 1,ipadx = 50, ipady=5,padx=50, pady=10, sticky = NSEW)
btnGpIn.grid(row = 8, column = 1,ipadx = 50, ipady=5,padx=50, pady=10, sticky = NSEW)
btnGpOut.grid(row = 10, column = 1,ipadx = 50, ipady=5,padx=50, pady=10, sticky = NSEW)
btnDestory.grid(row = 12, column = 2,ipadx = 50, ipady=5, pady=10, sticky = NSEW)
btnCheck.grid(row = 12, column = 3,ipadx = 50, ipady=5, pady=10, sticky = NSEW)
#sticky網格內NSEW方向擴張
#row 上下 column左右 ipadx物件內部 padx物件外部
labelPostion = Label(root,text = '燈具位置')
labelBrightness = Label(root,text = '調光數值')
labelColorChneger = Label(root, text = '顏色選擇')

labelPostion.grid(row = 0, column = 2, padx=5, pady=10, sticky = EW)
labelBrightness.grid(row = 4, column = 2, padx=5, pady=10, sticky = NSEW)
labelColorChneger.grid(row = 6, column = 2, padx=5, pady=10, sticky = NSEW)

entryPostion = Entry(root)
entryPostion.grid(row = 0, column = 3, padx=5, pady=10, sticky = EW)

scaleBrightness = Scale(root, orient='horizontal', from_ = 0, to = 254)
scaleBrightness.grid(row = 4, column = 3, padx=5, pady=10, sticky = NSEW)

openCB = ttk.Combobox(root)
openCB['values'] = ['','SKY_WHITE','FLOWER_WHITE','DAY','WARM_WHITE','YELLOW_WHITE','CANDLE']
openCB.current(0)
openCB.grid(row = 6, column = 3, padx=5, pady=10, sticky = EW)

root.mainloop()

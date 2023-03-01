import serial, time

help_msg = """    00: turn off
    01: up
    02: down
    03: step up
    04: step down
enter the control code:"""

# 19200,N,8,1
ser = serial.Serial("com3", 19200)
ser.bytesize = serial.EIGHTBITS  # number of bits per bytes

ser.timeout = 3  # non-block read 10s
ser.writeTimeout = 10  # timeout for write 10s


def checksum(*args) -> int:   # 定義checksum為字串或數字
    return sum(args) % 256    # 加總get_payload的參數 % 256


# 定義get_payload參數，(gateway_id,命令代碼,燈具位址,燈具亮度)
def get_payload(gateway_id=0xff, command_code=0x00, address=0xff, command=0x00):
    result = bytearray()         # 將result設定讀取bytearray
    result.append(gateway_id)    # 代入payload參數
    result.append(command_code)
    result.append(address)
    result.append(command)
    result.append(checksum(gateway_id, command_code, address, command))   # 計算checksum並代入指令

    return result


while True:
    if ser.isOpen():   # 連接COM
        i, j = str(input(help_msg)).split(',')
        ser.write(get_payload(
            # gateway_id=1,
            command_code=1,
            address=int(i, 16),
            command=int(j, 16)  # 輸入數字轉化成16進制
        ))
        time.sleep(0.5)
        recv_data = ser.readlines()
        print(get_payload)
    else:
        print("port open failed")
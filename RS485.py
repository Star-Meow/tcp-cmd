import serial, time

# 19200,N,8,1
ser = serial.Serial("com3", 19200)
ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
ser.stopbits = serial.STOPBITS_ONE  # number of stop bits

ser.timeout = 10  # non-block read 10s
ser.writeTimeout = 10  # timeout for write 10s

while True:
    if ser.isOpen():   #  連接COM
        print("port open success")   #    顯示連接成功
        i = str(input("Please enter 0 or 1: "))
        if i == '0':
            send_data = bytes.fromhex('ff 00 ff 00 fe')  #  power_off
            ser.write(send_data)   #發送命令
            time.sleep(0.5)
            # len_return_data = ser.inWaiting()  #  獲取緩衝數據長度
        elif i == '1':
            send_data = bytes.fromhex('ff 00 ff fe fc')  #  power_on
            ser.write(send_data)  # 發送命令
            time.sleep(0.5)
            # len_return_data = ser.inWaiting()  # 獲取緩衝數據長度
        # return_data = str(ser.read(len_return_data))
        # print(return_data)
        else:
            print("port open failed")


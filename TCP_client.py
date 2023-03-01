import socket, time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

help_msg = """    00: turn off
    01: up
    02: down
    03: step up
    04: step down
enter the control code:"""


def checksum(*args) -> int:  # 定義checksum為字串或數字
    return sum(args) % 256  # 加總get_payload的參數 % 256


# DALI-TCP header 6 bytes + DALI-485 normal command
def tcp_nor_cmd(index_hi=0x00, index_lo=0x00, type_cmd=0x00, protocol=0x01, payload_hi=0x00, payload_lo=0x05,
                gateway_id=0xff, command_code=0x00, address=0xff, command=0xfe):

    cmd = bytearray()
    cmd.append(index_hi)        # 流水號HighByte
    cmd.append(index_lo)        # 流水號LowByte
    cmd.append(type_cmd)        # command=0,query=1
    cmd.append(protocol)        # fixed
    cmd.append(payload_hi)      # fixed
    cmd.append(payload_lo)      # DALI-485 command Length=5 bytes
    cmd.append(gateway_id)      # 代入RS485參數
    cmd.append(command_code)
    cmd.append(address)
    cmd.append(command)
    cmd.append(checksum(gateway_id, command_code, address, command))  # 計算checksum並代入指令

    return cmd


# DALI-TCP header 6 bytes + DALI-485 temperature command
def tcp_temp_cmd(index_hi=0x00, index_lo=0x01, type_cmd=0x00, protocol=0x01, payload_hi=0x00, payload_lo=0x06,
                 gateway_id=0xff, command_code=0x06, address=0xff, temp_hi=0x01, temp_lo=0x4d):

    cmd = bytearray()
    cmd.append(index_hi)        # 流水號HighByte
    cmd.append(index_lo)        # 流水號LowByte
    cmd.append(type_cmd)        # command=0,query=1
    cmd.append(protocol)        # fixed
    cmd.append(payload_hi)      # fixed
    cmd.append(payload_lo)      # DALI-485 command Length=6 bytes
    cmd.append(gateway_id)      # 代入RS485參數
    cmd.append(command_code)
    cmd.append(address)
    cmd.append(temp_hi)
    cmd.append(temp_lo)
    cmd.append(checksum(gateway_id, command_code, address, temp_hi, temp_lo))  # 計算checksum並代入指令

    return cmd


while True:
    clientSocket.connect(("10.32.21.1", 502))
    # if clientSocket.connect(("10.32.21.1", 502)):  # 連線位址，Port號
    # a, b, c, d, e = str(input(help_msg)).split(',')
    # b, c = str(input(help_msg)).split(',')
    clientSocket.send(tcp_nor_cmd(
        # index_lo=int(a, 16),  # 輸入數字以16進制讀取
        # payload_lo=int(b, 16),
        # command_code=int(c, 16),
        # address=int(a, 16),
        # command=int(e, 16),
        # temp_hi=int(b, 16),
        # temp_lo=int(c, 16),
        ))
    time.sleep(0.5)
    recv_data = clientSocket.recv(1024)
    print(recv_data)
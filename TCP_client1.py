import socket
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("10.32.21.1", 502))
clientSocket.settimeout(500)

help_msg = '''
1. ON
2. OFF
3. Dimming
4. Add to Group
5. Remove from Group
6. Color
enter the control code:'''


class Color:
    SKY_WHITE = [0, 0x64]
    FLOWER_WHITE = [0, 0xa6]
    DAY = [0, 0xc8]
    WARM_WHITE = [1, 0x4d]
    YELLOW_WHITE = [1, 0x90]
    CANDLE = [1, 0xf4]


def checksum(*args) -> int:  # 定義checksum為字串或數字
    return sum(args) % 256  # 加總get_payload的參數 % 256


# DALI-TCP header 6 bytes + DALI-485 normal command
def tcp_dali_cmd(index_hi=0x00, index_lo=0x00, type_cmd=0x00,
                 gateway_id=0xff, command_code=0x01, address=0xff, command=[0x00]):

    cmd_msg = bytearray()
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


def on(address):
    return tcp_dali_cmd(command_code=1, address=address, command=[5])


def off(address):
    return tcp_dali_cmd(command_code=1, address=address, command=[0])


def dimming(address, command):
    return tcp_dali_cmd(command_code=0, address=address, command=[command])


def add_group(address, group_id):
    return tcp_dali_cmd(command_code=1, address=address, command=[group_id])


def remove_group(address, group_id):
    return tcp_dali_cmd(command_code=1, address=address, command=[group_id])


def temperature(address, color: Color):
    return tcp_dali_cmd(command_code=6, address=address, command=color)


while True:
    cmd = input(help_msg)
    if cmd == '1':
        addr = input('enter address: ')
        if not addr:
            continue

        for addrs in addr.split(','):
            cmd_on = on(int(addrs, 16))
            clientSocket.send(cmd_on)
            time.sleep(0.05)
        pass

    elif cmd == '2':
        addr = input('enter address: ')
        if not addr:
            continue

        for addrs in addr.split(','):
            cmd_off = off(int(addrs, 16))
            clientSocket.send(cmd_off)
            time.sleep(0.05)
        pass

    elif cmd == '3':
        addr = input('enter address: ')
        if not addr:
            continue

        command = input('enter brightness：')
        if not command:
            continue

        for addrs in addr.split(','):
            cmd_brightness = off(int(addrs, 16))
            print(cmd_brightness)
            time.sleep(0.05)
        pass

    elif cmd == '4':
        addr = input('enter address: ')
        if not addr:
            continue

        group_id = input('enter group: ')
        if not group_id:
            continue

        for addrs in addr.split(','):
            cmd_add_group = add_group(int(addrs, 16))
            clientSocket.send(cmd_add_group)
            time.sleep(0.05)
        pass

    elif cmd == '5':
        addr = input('enter address: ')
        if not addr:
            continue

        group_id = input('enter group: ')
        if not group_id:
            continue

        for addrs in addr.split(','):
            cmd_remove_group = remove_group(int(addrs, 16))
            clientSocket.send(cmd_remove_group)
            time.sleep(0.05)
        pass

    elif cmd == '6':
        addr = input('enter address: ')
        if not addr:
            continue

        color = input('''select color
    1. SKY_WHITE 
    2. FLOWER_WHITE
    3. DAY
    4. WARM_WHITE
    5. YELLOW_WHITE
    6. CANDLE
    ''')
        if color == '1':
            Color.SKY_WHITE
        elif color == '2':
            Color.FLOWER_WHITE
        elif color == '3':
            Color.DAY
        elif color == '4':
            Color.WARM_WHITE
        elif color == '5':
            Color.YELLOW_WHITE
        elif color == '6':
            Color.CANDLE

        for addr in addrs.split(','):
            cmd_temperature = temperature(int(addr, 16), color)
            clientSocket.send(cmd_temperature)
            time.sleep(0.05)
        pass

    else:
        continue

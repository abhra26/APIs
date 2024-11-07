import threading
import struct
import serial as s
import time
import CALLS as c

PORT = '/dev/ttyUSB1'
BAUD = 115200
SER = s.Serial(port=PORT,baudrate=BAUD)
response_queue = []
task_queue = []
token_map = {}

def add_task(MsgList):
    global task_queue
    for msg in MsgList[2 : ]:
        task_queue.append(msg)
    token_map[MsgList[0]] = MsgList[1]

def remove_task(token):
    try:
        del token_map[token]
        return True
    except:
        print("E404: Token-Task map doesnt exist")
        return False

def write(SerPORT):
    global task_queue
    while SerPORT:
        try:
            SerPORT.write(task_queue[-1])
            del task_queue[0]
        except:
            time.sleep(0.1)

def read(SerPORT):
    global response_queue
    while True:
        try:
            value = SerPORT.readline()
            entry = str(value,"UTF-8")
            tag = entry[0:3]
            data = entry[3:len(entry)]
            if tag == "REQ":
                response_queue.append(data)
            else:
                print(entry)
        except:
            time.sleep(0.1)

def print_():
    global response_queue
    while True:
        try:
            print(response_queue[-1])
            del response_queue[0]
            time.sleep(0.1)
        except:
            time.sleep(0.1)

def listen():
    global task_queue
    while True:
        data = str(input()) + '\n'
        cmd = '>' +str(len(data)) + 's'
        task = struct.pack(cmd,data.encode())
        task_queue.append(task)


threading.Thread(target=listen).start()
threading.Thread(target=write,args=(SER,)).start()
threading.Thread(target=read,args=(SER,)).start()
threading.Thread(target=print_).start()


        


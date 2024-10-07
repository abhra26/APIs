import serial as s
import socket as soc
import struct
import random
import string

ADDR_MAP = {

    'AES256'      : 'a1Y0Kyjk',
    'KyberMul'    : 'vnBnERLO',
    'SHA/SHAKE'   : 'fJJiIkAP',
    'TRNG'        : 'vZgFjb4w',
    'PRNG'        : 'iu5fIjSd',
    'GausSampler' : 'dpiAWxhs'

}

PARAMS = {

    'n' : 256,
    'k' : 16,
    'q' : 7321

}

PORT = '/dev/ttyUSB1'
BAUD = 115200
IP_ADDR = '192.168.1.100'

def generate_unique_token(length=16):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

def READ_THREAD(response_queue):
    COUNT = 0
    STATE = "IDLE"
    ADDRS = list(ADDR_MAP.keys())
    addr_ = "_"

    try: 
        with s.Serial(port = PORT, baudrate = BAUD) as SER:
            while True:
                value = SER.readline()
                response = str(value,'UTF-8')
                if response == "READ" or response == "read" :
                    STATE = "READ"
                elif response == "END" or response == "end":
                    STATE == "COMPLETE"
                else:
                    if STATE == "READ":
                        if response in ADDRS:
                            addr_ = response
                            continue
                        else:
                            #Manage addr_ error here 
                            pass

                    elif STATE == "COMPLETE":
                        STATE = "IDLE"
                    else:
                        pass
                
                if addr_ is not "_":
                    if addr_ == ADDR_MAP['KyberMul']:
                            if COUNT < PARAMS['k']:
                                cmd = '>' + ('I'*PARAMS['n']*PARAMS['k'])
                                ele = struct.unpack(cmd,value)
                                Coeffs = list(ele)
                                response_queue.append(Coeffs)
                                COUNT += 1
                            else:
                                COUNT = 0 
                                addr_ = "_"

                    if addr_ == ADDR_MAP['GausSampler']:
                        if COUNT < PARAMS['k']:
                            cmd = '>' + ('I'*PARAMS['n'])
                            sample = list(struct.unpack(cmd,value))
                            response_queue.append(sample)
                            COUNT += 1
                        else:
                            COUNT = 0
                            addr_ = "_"
                            

        return None
    except:
        print("ERROR: PORT {} could not be opened".format(PORT))
        response_queue.append("ERROR")
        return None
        
    

def CLOSE_PORT(SPort):
    if SPort.isopen():
        SPort.close()
        print("PORT WAS OPEN, NOW CLOSED")
        return None
    else:
        print("PORT ALREADY CLOSED")
        return None

def callGAUSSAMPLER():

    try:
        with s.Serial(port= PORT,baudrate= BAUD,timeout=1) as SER:

            STRING = ADDR_MAP['GausSampler'] + '|start' + '\n'
            SER.write(STRING.encode())
            #add delay if required
            RESPONSE_BYTES = SER.read()
            response_length = RESPONSE_BYTES[0] + 1
            string = 'i'*response_length
            RESPONSE = struct.unpack(string,RESPONSE_BYTES)
            print("DONE")
            return RESPONSE
    except:

        print("ERROR: PORT {} could not be opened".format(PORT))
        return None
    
def callKyberPolyMul(a,s,k):
    Coeff_len = len(a[0][0])
    try:
        with s.Serial(port=PORT,baudrate = BAUD, timeout = 1) as SER:
            msg1 = ADDR_MAP['KyberMul'] + '|init_A' + '\n'
            SER.write(msg1.encode())

            msg2 = struct.pack('>III',k,k,Coeff_len)
            SER.write(msg2)
            SER.write(b'\n')

            for i in range(PARAMS['k']):
                coeffs = []
                cmd = '>' + ('I'*PARAMS['n']*PARAMS['k'])
                for j in range(PARAMS['k']):
                    coeffs += list(a[i][j].poly())

                msg3 = struct.pack(cmd,*coeffs)
                SER.write(msg3)
                SER.write(b'\n')

            msg4 = ADDR_MAP['KyberMul'] + '|init_S' + '\n'
            SER.write(msg4.encode())

            msg5 = struct.pack('>III',k,1,Coeff_len)
            SER.write(msg5)
            SER.write(b'\n')
            coeffs = []
            cmd = '>' + ('I'*PARAMS['n']*PARAMS['k'])
            for i in range(k):
                coeffs += list(s[i].poly())

            msg6 = struct.pack(cmd, *coeffs)
            SER.write(msg6)
            SER.write(b'\n')

        print("DONE")
        return None

    except:

        print("ERROR: PORT {} could not be opened".format(PORT))
        return None
    

# while True:
#     value = SER.readline()
#     valueInString = str(value,'UTF-8')
#     print(valueInString)


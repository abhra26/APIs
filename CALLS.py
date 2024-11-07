import struct
import random
import string

ADDR_MAP = {

    'AES256'      : 'N1TpktxO',
    'KyberMul'    : 'cCTsFlby',
    'SHA/SHAKE'   : 'obwInnd2', 
    'PRNG'        : '38Yejpjk',
    'GausSampler' : '5eCKGG3W'

}

PARAMS = {

    'n' : 256,
    'k' : 16,
    'q' : 7321

}

INSTS = {

    'init' : 'nwlapYHl',
    'Sample' : '2UOzhC8y',
    'Encrypt' : 'UCVMPrtC',
    'Decrypt' : 'bwGFXxFS'
}

def generate_unique_token(length=64):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

def callAES256(DATA,KEY,TASK = "Encrypt"):
    token  = generate_unique_token()
    value = token + str(ADDR_MAP['AES256']) + str(KEY) + str(INSTS[TASK]) + str(DATA) + "\n"
    cmd = '>' + str(len(value)) + 's'
    msg = struct.pack(cmd,value.encode())
    task = "AES256|" + TASK
    return [token,task,msg]
         
def callGAUSSAMPLER():
    token = generate_unique_token()
    value = token + str(ADDR_MAP['GausSampler']) + str(INSTS['Sample']) + "\n"
    cmd = '>' + str(len(value)) + 's'
    msg = struct.pack(cmd,value.encode())
    task = 'GausSampler|Sample'
    return [token,task,msg]
    
def callKyberPolyMul(a,s,k,e):
    Coeff_len = len(a[0][0])
    token = generate_unique_token()
    value = token + str(ADDR_MAP['KyberMul']) + str(INSTS['init']) + "\n"
    cmd = '>' + str(len(value)) + 's'
    msg1 = struct.pack(cmd,value)
    a_compressed = []
    for i in range(PARAMS['k']):
        for j in range(PARAMS['k']):
            a_compressed += list(a[i][j].poly())

    cmd = '>' + ('I'*len(a_compressed))
    msg2 = struct.pack(cmd,*a_compressed)
        
    s_compressed = []
    for i in range(PARAMS['k']):
        s_compressed += list(s[i].poly())
    
    cmd  = '>' + ('I'*len(s_compressed))
    msg3 = struct.pack(cmd,*s_compressed)

    e_compressed = []
    for i in range(PARAMS['k']):
        e_compressed += list(e[i].poly())
    
    cmd  = '>' + ('I'*len(e_compressed))
    msg4 = struct.pack(cmd,*e_compressed)

    task = "KyberPolyMul|init"

    return [token,task,msg1,msg2,msg3,msg4]



import socket
import pickle
from urllib import request as urlreq
from urllib.error import URLError
import typing as T

Socket = socket.socket

def arg_on_error(func):
    def _(*args):
        try:
            return func(*args)
        except Exception as e:
            return args
    return _

def get_ip() -> str:
    try:
        ip = urlreq.urlopen(
            "https://ident.me", timeout=1.5
        ).read().decode("utf8")
    except URLError:
        ip = socket.gethostbyname(socket.gethostname())
    return ip

@arg_on_error
def recvobj(sock_where: Socket):
    '''Receive an object from `sock_where`'''
    objlen = sock_where.recv(8).decode()
    if not objlen:
        return None
    objlen = int(objlen)
    res = b''
    while len(res) < objlen:
        res += sock_where.recv(min(2048, objlen - len(res)))
    return pickle.loads(res)

@arg_on_error
def sendobj(sock_where: Socket, obj) -> T.Union[None, Socket]:
    '''Send object `obj` to `sock_where`\n\nreturn None on success'''
    # print('sent', obj)
    obj = pickle.dumps(obj)
    obj = str(len(obj)).zfill(8).encode() + obj
    return sock_where.sendall(obj)

def validate_ip(ip: str):
    ip = ip.split('.')

    if len(ip) != 4:
        return False

    for arg in ip:
        # if not numeric or is starting with '0' while not being equal to 0
        if not arg.isdigit() or (arg.startswith('0') and len(arg) > 1):
            return False
        elif 0 > int(arg) >= 256:
            return False
    return True
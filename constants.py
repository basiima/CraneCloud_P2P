import socket
import threading
import sys
import time
from random import randint

HOST = '127.0.0.1'
PORT = 5000
PEER_BYTE = b'\x11'
SIZE = 1024
TIME_START = 1
TIME_END = 2
REQ_STRING = "req"

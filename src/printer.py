import serial
import re


class AbstractPort:
    def write(self):
        pass
    
    
class TTYPort(AbstractPort):
    def __init__(self, path):
        self.path = path
        self.tty = None
        
    def initSerial(self):
        if self.tty == None:
            self.tty = serial.Serial(self.path, timeout=2)
        
    def write(self, data):
        self.initSerial()
        self.tty.write(data)
    
    def readLine(self):
        self.initSerial()
        buffer = b""
        char = b""
        while char != b"\r" and char != b"\n":
            buffer += char
            char = self.tty.read(1)
            if len(char) == 0:
                raise IOError("Timeout")
        return buffer
    
    def getID(self):
        self.write(b"UQ\r\n")
        while True:
            line = self.readLine().decode("utf-8")
            matches = re.search(".+System Location,lk([0-9]+)", line)
            if matches != None:
                return int(matches.group(1))
        

class TestPort(AbstractPort):
    def write(self, data):
        print(data)


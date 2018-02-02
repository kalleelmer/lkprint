import serial
import re


class AbstractPort:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
    
    def write(self):
        pass
    
    def close(self):
        pass
    
    def getID(self):
        return 0

    def getSerialNumber(self):
        return None

    
class SerialPort(AbstractPort):
    def __init__(self, path):
        AbstractPort.__init__(self)
        self.path = path
        self.tty = None
        self.offset_x = 0
        
    def initPort(self):
        if self.tty == None:
            self.tty = serial.Serial(self.path, timeout=2)
        
    def write(self, data):
        self.initPort()
        self.tty.write(data)
        self.tty.flush()
        
    def readChar(self):
        return self.tty.read(1)
    
    def readLine(self):
        self.initPort()
        buffer = b""
        char = b""
        while char != b"\r" and char != b"\n":
            buffer += char
            char = self.readChar()
            if len(char) == 0:
                self.tty.close()
                self.tty = None
                raise IOError("Timeout")
        return buffer
    
    def getID(self):
        self.write(b"UQ\r\n")
        while True:
            line = self.readLine().decode("utf-8")
            matches = re.search(".+System Location,lk([0-9]+)", line)
            if matches != None:
                return int(matches.group(1))
    
    def __str__(self):
        return self.path
    
    def close(self):
        if self.tty != None:
            self.tty.close()
            self.tty = None
        

class ParallelPort(SerialPort):
    def __init__(self, path):
        AbstractPort.__init__(self)
        self.path = path
        self.file = None
        self.offset_x = 70
    
    def initPort(self):
        if self.file == None:
            self.file = open(self.path, "r+b")
    
    def write(self, data):
        self.initPort()
        self.file.write(data)
        self.file.flush()
    
    def readChar(self):
        return self.file.read(1)
    
    def getID(self):
        return 0

    def getSerialNumber(self):
        self.write(b"USR\r\n")
        while True:
            line = self.readLine().decode("utf-8", "ignore")
            return line
        
    def close(self):
        if self.file != None:
            try:
                self.file.close()
            except OSError as e:
                pass
            self.file = None


class TestPort(AbstractPort):
    def write(self, data):
        print(data)
    
    def getID(self):
        return 1
    
    def __str__(self):
        return "stdout"


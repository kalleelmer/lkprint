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

class SerialPort(AbstractPort):
    def __init__(self, path):
        AbstractPort.__init__(self)
        self.path = path
        self.tty = None
        self.offset_x = 0
        
    def initPort(self):
        if self.tty == None:
            self.tty = serial.Serial(self.path, timeout=5)
        
    def write(self, data):
        self.initPort()
        self.tty.write(data)
        self.tty.flush()
#         print("Send:", data)
        
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
#         if len(buffer) > 0:
#             print("Receive:", buffer)
        return buffer
    
    def waitForOk(self):
        line = b""
        while line != b"Ok":
            line = self.readLine()
            if line == b"Out of media":
                raise IOError("Out of media")
            elif line == b"Next label not found":
                raise IOError("Next label not found")
    
    def getID(self):
        self.write(b"SYSVAR(18)=10\r\n")
        self.waitForOk()
        self.write(b"SYSVAR(43)=1\r\n")
        self.waitForOk();
        self.write(b"COPY \"/home/user/lkprint.conf\", \"usb1:\"\r\n")
        while True:
            line = self.readLine().decode("utf-8")
            matches = re.search("id=([0-9]+)", line)
            if matches != None:
                self.waitForOk()
                return int(matches.group(1))
    
    def __str__(self):
        return self.path
    
    def close(self):
        if self.tty != None:
            self.tty.close()
            self.tty = None


class TestPort(AbstractPort):
    def write(self, data):
        print(data)
    
    def getID(self):
        return 1
    
    def __str__(self):
        return "stdout"


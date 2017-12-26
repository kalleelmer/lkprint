import serial


class AbstractPort:
    def write(self):
        pass
    
    
class TTYPort(AbstractPort):
    def __init__(self, path):
        self.path = path
        self.tty = None
        
    def write(self, data):
        if self.tty == None:
            self.tty = serial.Serial(self.path)
        self.tty.write(data)


class TestPort(AbstractPort):
    def write(self, data):
        print(data)


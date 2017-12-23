import serial

class TextBox:
    def __init__(self, x, y, size, text):
        self.x = x
        self.y = y
        self.size = size
        self.text = text

    def render(self):
        line = "A" + str(self.y) + "," + str(self.x) + ",1,1," + str(self.size) + "," + str(self.size) + ",N,\"" + self.text + "\"\r\n"
        return bytes(line, "utf-8")


port = serial.Serial("/dev/ttyACM0")

title = TextBox(250, 300, 3, "Spexet")
time = TextBox(250, 250, 2, "19 maj 17:00")
category = TextBox(250, 200, 2, "Parkett")
rate = TextBox(250, 150, 2, "Student")
port.write(title.render())
port.write(time.render())
port.write(category.render())
port.write(rate.render())
port.write(b"P1\r\n")

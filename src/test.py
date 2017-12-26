from draw import TextBox
from printer import TTYPrinter

port = TTYPrinter("/dev/ttyACM0")

title = TextBox(250, 300, 3, "Spexet")
time = TextBox(250, 250, 2, "19 maj 17:00")
category = TextBox(250, 200, 2, "Parkett")
rate = TextBox(250, 150, 2, "Student")
port.write(title.render())
port.write(time.render())
port.write(category.render())
port.write(rate.render())
port.write(b"P1\r\n")

class TextBox:
    def __init__(self, x, y, size, text):
        self.x = x
        self.y = y
        self.size = size
        self.text = text

    def render(self):
        line = "A" + str(self.y) + "," + str(self.x) + ",1,1," + str(self.size) + "," + str(self.size) + ",N,\"" + self.text + "\"\r\n"
        return bytes(line, "utf-8")
    

class TicketPrinter:
    def __init__(self, port):
        self.port = port

    def printTicket(self, ticket):
        title = TextBox(250, 300, 3, ticket["show_name"])
        self.port.write(title.render())
        time = TextBox(250, 250, 2, ticket["performance_start"])
        self.port.write(time.render())
        category = TextBox(250, 200, 2, ticket["category_name"])
        self.port.write(category.render())
        rate = TextBox(250, 150, 2, ticket["rate_name"])
        self.port.write(rate.render())
        self.port.write(b"P1\r\n")
        
        
        
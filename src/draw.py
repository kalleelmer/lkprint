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
        self.port.write(b"N\r\n")
        title = TextBox(self.port.offset_x, 300, 3, ticket["show_name"])
        self.port.write(title.render())
        time = TextBox(self.port.offset_x, 250, 2, ticket["performance_start"])
        self.port.write(time.render())
        category = TextBox(self.port.offset_x, 200, 2, ticket["category_name"])
        self.port.write(category.render())
        rate = TextBox(self.port.offset_x, 150, 2, ticket["rate_name"])
        self.port.write(rate.render())
        self.port.write(b"P1\r\n")
    
    def getID(self):
        return self.port.getID()

    def getSerialNumber(self):
        return self.port.getSerialNumber()
    
    def __str__(self):
        return self.port.__str__()
    
    def close(self):
        self.port.close()
        
        
        
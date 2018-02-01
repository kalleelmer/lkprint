class TextBox:
    def __init__(self, x, y, font, size, text):
        self.x = x
        self.y = y
        self.font = font
        self.size = size
        self.text = text

    def render(self):
        line = "A" + str(self.y) + "," + str(self.x) + ",1," + str(self.font) + "," + str(self.size) + "," + str(self.size) + ",N,\"" + self.text + "\"\r\n"
        return bytes(line, "cp850")
    
    
class DataMatrix:
    def __init__(self, x, y, size, data):
        self.x = x
        self.y = y
        self.size = size
        self.data = data
        
    def render(self):
        line = "b" + str(self.y) + "," + str(self.x) + ",D," + str(self.size) + ",\"" + str(self.data) + "\"\r\n"
        return bytes(line, "cp850")
    

class TicketPrinter:
    def __init__(self, port):
        self.port = port

    def printTicket(self, ticket):
        self.port.write(b"N\r\n")
        title = TextBox(self.port.offset_x, 410, "b", 1, ticket["show_name"])
        self.port.write(title.render())
        time = TextBox(self.port.offset_x, 330, "a", 1, ticket["performance_start"])
        self.port.write(time.render())
        category = TextBox(self.port.offset_x, 280, "a", 1, ticket["category_name"])
        self.port.write(category.render())
        rate = TextBox(self.port.offset_x, 230, "a", 1, ticket["rate_name"])
        self.port.write(rate.render())
        dm = DataMatrix(self.port.offset_x + 610, 190, 7, str(ticket["id"]))
        self.port.write(dm.render())
        self.port.write(b"P1\r\n")
    
    def getID(self):
        return self.port.getID()

    def getSerialNumber(self):
        return self.port.getSerialNumber()
    
    def __str__(self):
        return self.port.__str__()
    
    def close(self):
        self.port.close()
        
        
        
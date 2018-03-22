class TicketPrinter:
    def __init__(self, port):
        self.port = port
        self.fallback = False
    
    def sendCommand(self, line):
        self.port.write(line.encode("utf-8") + b"\r\n")
        self.port.waitForOk()

    def printTicket(self, ticket):
        self.sendCommand("NASC \"UTF-8\"")
        self.sendCommand("BEEP")
        self.sendCommand("CLEAR")
        self.sendCommand("DIR 4")
        self.sendCommand("ALIGN 4")
        
        self.sendCommand("FONT \"OPTIBrianJamesBoldCond Bold\",25")
        
        self.sendCommand("PRPOS 480, 50")
        self.sendCommand("PRTXT \"" + ticket["show_name"] + "\"")
        
        self.sendCommand("FONT \"Montserrat SemiBold\",14,0,100")
        self.sendCommand("PRPOS 530, 50")
        self.sendCommand("PRTXT \"" + ticket["performance_start"] + "\"")
        self.sendCommand("PRPOS 580, 50")
        self.sendCommand("PRTXT \"" + ticket["category_name"] + ", " + ticket["rate_name"] + "\"")
        
#         self.sendCommand("FONT \"Montserrat SemiBold\",6,0,100")
#         self.sendCommand("PRPOS 640, 80")
#         self.sendCommand("PRTXT \"Kom gärna 20 minuter innan föreställningen börjar\"")
        
        self.sendCommand("PRPOS 520,650")
        self.sendCommand("BARSET \"DATAMATRIX\",1,1,10,0,0,20")
        self.sendCommand("BARFONT \"Univers\",10,8,5,1,1 ON")
        self.sendCommand("PRBAR \"" + str(ticket["id"]) + "\"")
        
        self.sendCommand("PRINTFEED")
    
    def getID(self):
        return self.port.getID()

    def __str__(self):
        return self.port.__str__()
    
    def close(self):
        self.port.close()
        
        
        
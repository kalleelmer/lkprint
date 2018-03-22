class TicketPrinter:
    def __init__(self, port):
        self.port = port
        self.fallback = False
    
    def writeLine(self, line):
        self.port.write(line.encode("utf-8") + b"\r\n")

    def printTicket(self, ticket):
        self.writeLine("NASC \"UTF-8\"")
        self.writeLine("BEEP")
        self.writeLine("CLEAR")
        self.writeLine("DIR 4")
        self.writeLine("ALIGN 4")
        
        self.writeLine("FONT \"OPTIBrianJamesBoldCond Bold\",25")
        
        self.writeLine("PRPOS 480, 50")
        self.writeLine("PRTXT \"" + ticket["show_name"] + "\"")
        
        self.writeLine("FONT \"Montserrat SemiBold\",14,0,100")
        self.writeLine("PRPOS 530, 50")
        self.writeLine("PRTXT \"" + ticket["performance_start"] + "\"")
        self.writeLine("PRPOS 580, 50")
        self.writeLine("PRTXT \"" + ticket["category_name"] + ", " + ticket["rate_name"] + "\"")
        
        self.writeLine("FONT \"Montserrat SemiBold\",6,0,100")
        self.writeLine("PRPOS 640, 80")
        self.writeLine("PRTXT \"Kom gärna 20 minuter innan föreställningen börjar\"")
        
        self.writeLine("PRPOS 520,650")
        self.writeLine("BARSET \"DATAMATRIX\",1,1,10,0,0,20")
        self.writeLine("BARFONT \"Univers\",10,8,5,1,1 ON")
        self.writeLine("PRBAR \"012345\"")
        
        self.writeLine("PRINTFEED")
    
    def getID(self):
        return self.port.getID()

    def __str__(self):
        return self.port.__str__()
    
    def close(self):
        self.port.close()
        
        
        
import requests


class Core:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {"Authorization" : "Token " + token}
        
    def getPrinter(self, pid):
        response = requests.get(self.url + "/desk/printers/" + str(pid), headers=self.headers)
        if response.status_code != 200:
            raise IOError("API response " + str(response.status_code))
        return response.json()
    
    def getPrinterBySerialNumber(self, serial_number):
        response = requests.get(self.url + "/desk/printers/sno/" + serial_number, headers=self.headers)
        if response.status_code != 200:
            raise IOError("API response " + str(response.status_code))
        return response.json()

    def setAlive(self, pid):
        response = requests.put(self.url + "/desk/printers/" + str(pid) + "/alive", headers=self.headers)
        if response.status_code != 204:
            raise IOError("API response " + str(response.status_code))
    
    def setTicketPrinted(self, pid, ticket_id):
        response = requests.put(self.url + "/desk/printers/" + str(pid) + "/printed/" + str(ticket_id), headers=self.headers)
        if response.status_code != 204:
            raise IOError("API response " + str(response.status_code))
        
    def getTicket(self, ticket_id):
        response = requests.get(self.url + "/desk/tickets/" + str(ticket_id), headers=self.headers)
        if response.status_code != 200:
            raise IOError("API response " + str(response.status_code))
        return response.json()
    
        
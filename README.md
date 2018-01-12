# LKPrint
LKPrint är en systemtjänst för utskrift av biljetter från LKTicket. Den letar efter en skrivare på en angiven serieport, som kan vara över USB. När en skrivare hittas hämtas dess information från biljettsystemets API. Därefter börjar programmet lyssna efter biljetter via Amazon SQS. Biljetter som tas emot skrivs ut med eSim. Programmet kollar periodiskt att skrivaren fortfarande är ansluten och skickar varje gång ett anrop till API:et med denna information.

## Installation

### Ubuntu 16.04
För Ubuntu 16.04 skapar Jenkins automatiskt ett DEB-paket som kan installeras från vårt repo. Följande fyra kommandon lägger till repot, importerar nyckeln, uppdaterar paketinformationen och installerar programmet.

    sudo add-apt-repository https://apt.lkticket.net
    wget -qO- https://apt.lkticket.net/Release.gpg | sudo apt-key add
    sudo apt update
    sudo apt install lkprint

Varje dator som kör programmet måste ha en token för API-åtkomst. Det krävs även nycklar för åtkomst till AWS.

Efter installationen kommer programmet automatiskt att köras som en tjänst med systemd.

### Övriga system
    Biljonsen har under 2018 inte haft något behov av att köra andra system, men det borde inte vara några problem att installera manuellt eftersom allting är skrivet i Python.


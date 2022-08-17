import socket

class PhoneBook:

    def __init__(self, filename):
        self.filename = filename
        file = open(filename, "r+")
        self.pb = dict()
        for line in file:
            contact = line.split()
            self.pb.update({contact[0]:contact[1]})
        file.close()

    def listContacts(self):
        outstring = "Name\t\tPhone\n"
        for i in sorted(self.pb.keys()):
            outstring = outstring + "{}\t\t{}\n".format(i, self.pb[i])
        return outstring

    def addContact(self, name, phno):
        if name not in self.pb.keys():
            self.pb.update({name:phno})
            outstring = "1 entry added"
        else:
            outstring = "entry exists"
        return outstring

    def searchByName(self, name):
        if name in self.pb.keys():
            outstring = "entry found - "+ name +"-" + self.pb[name]
        else:
            outstring = "entry not found"
        return outstring
    
    def searchByNumber(self, phno):
        if phno in self.pb.values():
            for k,v in self.pb.items():
                if phno == v:
                    name = k
                    break   
            outstring = "entry found - " + name + "-" + phno
        else:
            outstring = "entry not found"
        return outstring

    def deleteContact(self, name):
        if name in self.pb.keys():
            del self.pb[name]
            outstring = "1 entry ({}) deleted".format(name)
        else:
            outstring = "entry does not exist"
        return outstring

    def commit(self):
        file = open(self.filename, "w")
        for k,v in self.pb.items():
            file.write("{} {}\n".format(k,v))
        outstring = "Committed edits"
        file.close()
        return outstring

def server():
    book1 = PhoneBook("phonebook1.txt")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    port = 12345
    print(hostname)
    s.bind((hostname, port))
    s.listen(2)
    c, addr = s.accept()
    print('Got connection from', addr)
    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        else:
            cmd_s = str(data).split()
            if(cmd_s[0] == "ADD"):
                data = book1.addContact(cmd_s[1], cmd_s[2])
                c.send(data.encode())
            elif(cmd_s[0] == "SEARCH"):
                if(cmd_s[1] == "NAME"):
                    data = book1.searchByName(cmd_s[2])
                    c.send(data.encode())
                elif(cmd_s[1] == "NUM"):
                    data = book1.searchByNumber(cmd_s[2])
                    c.send(data.encode())
            elif(cmd_s[0] == "DELETE"):
                data = book1.deleteContact(cmd_s[1])
                c.send(data.encode())
            elif(cmd_s[0] == "COMMIT"):
                data = book1.commit()
                c.send(data.encode())
            elif(cmd_s[0] == "LIST"):
                data = book1.listContacts()
                c.send(data.encode())
            else:
                pass
    c.close()

if __name__ == '__main__':
    server()
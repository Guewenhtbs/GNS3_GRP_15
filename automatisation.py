import json
from datetime import datetime

with open('Donnees_test.json','r',encoding='utf-8') as f :
    data = json.load(f)

class AS :
    def  __init__(self, AS_data):
        self.number = AS_data["AS_number"]
        self.igp = AS_data["IGP"]
        self.router = []
        self.neighbors = AS_data["voisinage"]
        self.prefixes = AS_data["prefixes"]

    def __str__(self):
        return (f"Le numéro d'AS est {self.number}, le protocole interne est {self.igp}, les routeurs de l'AS sont {self.router}, les voisins sont {self.neighbors}, les préfixes réseaux sont {self.prefixes}.")
    
class ROUTER :
    def __init__(self, RTR_data, as_n):
        self.name = RTR_data["R_name"]
        self.ip = RTR_data["ip_address"]
        self.neighbors = RTR_data["voisins"]
        self.border = RTR_data["border"]
        self.as_n = as_n
        self.id = (f"{self.name}.{self.name}.{self.name}.{self.name}")

    def __str__(self):
        return (f"Le nom du routeur est R{self.name}, les adresses ip sont {self.ip}, qui sont associés aux voisins {self.neighbors}, le fait d'être un routeur de bordure est défini par {self.border}, son id BGP est {self.id}.")

    def __repr__(self):
        return (f"R{self.name}")


def lecture_json():
    liste_AS = []
    i = 0
    for AS_data in data["AS"]:
        liste_AS.append(AS(AS_data))
        for RTR_data in AS_data["routeur"]:
            liste_AS[i].router.append(ROUTER(RTR_data,liste_AS[i].number))
        i+=1
    for j in liste_AS :
        print(j)
        for k in j.router :
            print (k)
    return

##############MAIN#############
lecture_json()




def debut(name):
    now = datetime.utcnow()
    formatted_date = now.strftime("%H:%M:%S UTC %a %b %d %Y")
    fichier = open("conf"+ str(name) +".txt", "w")
    fichier.write("!\n\n!\n! Last configuration change at " + formatted_date + "\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostame R"+ name +"\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!")
    fichier.close()

debut("12")

def interfaces(ip,igp,name):
    fichier = open("conf.txt", "w")
    fichier.write(f"\ninterface Loopback0\n no ip address\n ipv6 address {ip[4]}/128\n ipv6 enable")
    if igp == "OSPF" :
        fichier.write(f"\n ipv6 ospf 15 area 0\n!")
    if igp == "RIP" :
        fichier.write(f"\n ipv6 rip 15 enable\n!")

    nom_interface : ["FastEthernet0/0","GigabitEthernet1/0","GigabitEthernet2/0","GigabitEthernet3/0"]

    for interface in nom_interface :
    
    fichier.write("\ninterface FastEthernet0/0")
    if ip[0]==None :
        fichier.write("\n shutdown\n  duplex full")
    else :
        aux_interfaces(ip[0],igp,)
    

    fichier.write("\ninterface GigabitEthernet1/0")
    if ip[1]==None :
        fichier.write("\n no ip address\n shutdown\n negotiation auto")
    else :
        aux_interfaces(ip[1],igp)

    fichier.write("\ninterface GigabitEthernet2/0")
    if ip[2]==None :
        fichier.write("\n no ip address\n shutdown\n negotiation auto")
    else :
        aux_interfaces(ip[2],igp)

    fichier.write("\ninterface GigabitEthernet3/0")
    if ip[3]==None :
        fichier.write("\n no ip address\n shutdown\n negotiation auto")
    else :
        aux_interfaces(ip[3],igp)
    fichier.close()


def aux_interfaces(adresse, igp,fichier):

    fichier.write(f"\n no ip address\n ipv6 address {adresse}/64\n ipv6 enable\n")
    if igp == "OSPF" :
        fichier.write(f"\n ipv6 ospf 15 area 0\n!")
    if igp == "RIP" :
        fichier.write(f"\n ipv6 rip 15 enable\n!")



interfaces(['2023:1::2', '2200:2::2', None, None, '3522::8'],"OSPF",8)
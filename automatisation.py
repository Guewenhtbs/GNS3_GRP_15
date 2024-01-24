import json
from datetime import datetime

with open("Donnees_bgp.json",'r',encoding='utf-8') as f :
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
    #for j in liste_AS :
    #    print(j)
    #    for k in j.router :
    #        print (k)
    return liste_AS
  
def debut(fichier, name):
    now = datetime.utcnow()
    formatted_date = now.strftime("%H:%M:%S UTC %a %b %d %Y")
    fichier.write("!\n\n!\n! Last configuration change at " + formatted_date + "\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname R" + str(name) + "\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n! \n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!")

def interfaces(fichier, ip, igp,interface_border):
    fichier.write(f"\ninterface Loopback0\n no ip address\n ipv6 address {ip[4]}/128\n ipv6 enable")
    ospf_ou_rip(igp, fichier)

    nom_interface = ["FastEthernet0/0", "GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"]

    fichier.write(f"\n!\ninterface {nom_interface[0]}")
    if ip[0] is None:
        fichier.write("\n no ip address\n shutdown\n duplex full\n!")
    else:
        fichier.write(f"\n no ip address\n duplex full\n ipv6 address {ip[0]}/64\n ipv6 enable")
        if 1 not in interface_border or igp == "OSPF":
            ospf_ou_rip(igp, fichier)
        fichier.write("\n!")
    for i in range(1, len(nom_interface)):
        fichier.write(f"\ninterface {nom_interface[i]}")
        if ip[i] is None:
            fichier.write("\n no ip address\n shutdown\n negotiation auto\n!")
        else:
            border = False
            if i+1 in interface_border :
                border = True
            aux_interfaces(fichier, ip[i], igp,border)

def aux_interfaces(fichier, adresse, igp, border):
    fichier.write(f"\n no ip address\n negotiation auto\n ipv6 address {adresse}/64\n ipv6 enable")
    if border == False or igp == "OSPF":
        ospf_ou_rip(igp, fichier)
    fichier.write("\n!")

def ospf_ou_rip(igp, fichier):
    if igp == "OSPF":
        fichier.write(f"\n ipv6 ospf 15 area 0")
    elif igp == "RIP":
        fichier.write(f"\n ipv6 rip 15 enable")
        
def BGP(fichier,AS,r_id,neighbors_BGP,prefixes) :
    fichier.write(f"\nrouter bgp {AS.number}\n bgp router-id {r_id}\n bgp log-neighbor-changes\n no bgp default ipv4-unicast")
    border = False
    for (ip,v_AS) in neighbors_BGP :
        if v_AS == AS.number :
            fichier.write(f"\n neighbor {ip} remote-as {v_AS}\n neighbor {ip} update-source Loopback0")
        else :
            fichier.write(f"\n neighbor {ip} remote-as {v_AS}")
            border = True
    fichier.write("\n !\n address-family ipv4\n exit-address-family\n !\n address-family ipv6")
    if border == True :
        for pref in prefixes :
            fichier.write(f"\n  network {pref} route-map tag_client")
    for (ip,v_AS) in neighbors_BGP :
        fichier.write(f"\n  neighbor {ip} activate")
        fichier.write(f"\n  neighbor {ip} send-community")
        if v_AS == AS.number :
            pass
        else :
            fichier.write(f"\n  neighbor {ip} route-map tag_{AS.neighbors[str(v_AS)]} in")
            if AS.neighbors[str(v_AS)] != "client" :
                fichier.write(f"\n  neighbor {ip} route-map block_{AS.neighbors[str(v_AS)]} out")
    fichier.write(f"\n exit-address-family\n!\nip forward-protocol nd\n!\nip bgp-community new-format\nip community-list standard client permit {AS.number}:150\nip community-list standard free_peer permit {AS.number}:120\nip community-list standard provider permit {AS.number}:50\n!\nno ip http server\nno ip http secure-server\n!")

def IGP(fichier,r_id,igp,passive) :
    if igp == "RIP" :
        fichier.write(f"\nipv6 router rip 15\n redistribute connected")
    elif igp == "OSPF" :
        fichier.write(f"\nipv6 router ospf 15\n router-id {r_id}")
        for interface in passive :
            fichier.write(f"\n passive-interface {interface}")
    fichier.write("\n!\n!")

def route_map(fichier,neighbors_BGP,AS) :
    for (_,v_AS) in neighbors_BGP :
        print ()
        if v_AS != AS.number :           
            fichier.write(f"\nroute-map tag_client permit 50\n set local-preference 150\n set community {AS.number}:150")
            if AS.neighbors[str(v_AS)] == "free_peer" :
                fichier.write(f"\n!\nroute-map tag_free_peer permit 50\n set local-preference 120\n set community {AS.number}:120\n!\nroute-map block_free_peer permit 50\n match community client")
            if AS.neighbors[str(v_AS)] == "provider" :
                fichier.write(f"\n!\nroute-map tag_provider permit 50\n set local-preference 50\n set community {AS.number}:50\n!\nroute-map block_provider permit 50\n match community client")
    fichier.write("\n!\n!\n!\ncontrol-plane\n!\n!\nline con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline vty 0 4\n login\n!\n!\nend\n")
def search_ip(r_name,v_name,liste_AS,AS_n) :
    for As in liste_AS :
        if As.number == str(AS_n) :
            for router in As.router :
                if router.name == v_name :
                    for index in range(4):
                        if router.neighbors[index] == r_name :
                            return router.ip[index]
    print(f"{r_name},{v_name}")
    print("IP non trouvé")
    return None
  
##############MAIN#############

liste_AS = lecture_json()
correspondance = {1 : "FastEthernet0/0", 2 : "GigabitEthernet1/0", 3 : "GigabitEthernet2/0", 4 : "GigabitEthernet3/0"}
for As in liste_AS :
    for router in As.router :
        with open(f"Config_bgp/i{router.name}_startup-config.cfg", "w") as fichier:
            debut(fichier, router.name)
            interface_border = []
            for i in range(router.border[0]) :
                interface_border.append(router.border[i+1])
            interfaces(fichier, router.ip, As.igp,interface_border)
            neighbors_bgp = []
            passive_int = []
            index = 1
            for neighbor in router.neighbors :
                for i in range(router.border[0]) :
                    if router.border[i*2+1] == index :
                        neighbors_bgp.append((search_ip(router.name,neighbor,liste_AS,router.border[i*2+2]),router.border[i*2+2]))
                        if As.igp == "OSPF" :
                            passive_int.append(correspondance[index])
                index+=1
            for v_router in As.router :
                if router != v_router :
                    neighbors_bgp.append((v_router.ip[4],As.number))
            BGP(fichier,As,router.id,neighbors_bgp,As.prefixes)
            IGP(fichier,router.id,As.igp,passive_int)
            route_map(fichier,neighbors_bgp,As)


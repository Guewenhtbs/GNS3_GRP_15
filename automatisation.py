import json 


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
    return liste_AS

def BGP(r_name,AS,r_id,neighbors_BGP,prefixes):
    fichier = open(f"./config_test/R{r_name}.txt","a")
    fichier.write(f"\nrouter bgp {AS}\n bgp router-id {r_id}\n bgp log-neighbor-changes\n no bgp default ipv4-unicast")
    for (ip,v_AS) in neighbors_BGP :
        if v_AS == AS :
            fichier.write(f"\n neighbor {ip} remote-as {v_AS}\n update-source Loopback0")
        else :
            fichier.write(f"\n neighbor {ip} remote-as {v_AS}")
    fichier.write("\n !\n address-family ipv4\n exit-address-family\n !\n address-family ipv6")
    for pref in prefixes :
        fichier.write(f"\n  network {pref}")
    for (ip,_) in neighbors_BGP :
        fichier.write(f"\n  neighbor {ip} activate")
    fichier.write("\n exit-address-family\n!\nipforward-protocol nd\n!\n!\nno ip http server\nno ip http secure-server\n")
    fichier.close()

def search_ip(r_name,v_name,liste_AS,AS_n):
    for As in liste_AS :
        if As.number == AS_n :
            for router in As.router :
                if router.name == v_name :
                    for index in range(4):
                        if router.neighbors[index] == r_name :
                            return router.ip_address[index]
    print("IP non trouvé")
    return None


##############MAIN#############
liste_AS = lecture_json()
for As in liste_AS :
    for router in As.router :
        debut(router.name)
        interface()
        neighbor_bgp = []
        index = 1
        for neighbor in router.neighbors :
            for i in range(router.border[0]) :
                if router.border[i*2+1] == index :
                    neighbor_bgp.append((search_ip(neighbor),router.border[i*2+2]))
            for v_router in As.router :
                if router != router :
                    neighbor_bgp.append((v_router.ip_address[4],As.number))
    

        BGP(router.name,As.number,router.id,)
    
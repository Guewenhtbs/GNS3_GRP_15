import json 

class AS :
    def  __init__(self, as_n:str, igp:str, router_list:list, neighbors_list:list):
        self.number = as_n
        self.igp = igp
        self.router = router_list
        self.neighbors = neighbors_list

    def __str__(self):
        return (f"Le numéro d'AS est {self.number}, le protocole interne est {self.igp}, les routeurs de l'AS sont {self.router}, les voisins sont {self.neighbors}.")
    
class ROUTER :
    def __init__(self, r_n:str, ip_list:list, neighbors_list:list, border_list:str, as_n:str):
        self.name = r_n
        self.ip = ip_list
        self.neighbors = neighbors_list
        self.border = border_list
        self.as_n = as_n

    def __str__(self):
        return (f"Le nom du routeur est {self.name}, les adresses ip sont {self.ip}, qui sont associés aux voisins {self.neighbors}, le fait d'être un routeur de bordure est défini par {self.border}.")

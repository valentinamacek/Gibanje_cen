from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime 


#definiramo vse podatkovne modele, ki jih bomo uporabljali v aplikaciji
@dataclass_json
@dataclass
class klasifikacija: 
    id : int = field(default=0)  # Za vsako polje povemo tip in privzeto vrednost
    ime : str = field(default="")
    ang_ime: str = field(default="")
    sifra: str = field(default="")
    raven: int = field(default=0)
    
@dataclass_json
@dataclass
class nivoji: 
    id_podskupine : int = field(default=0)  
    id_nadskupine : int = field(default=0)

@dataclass_json
@dataclass
class utezi_in_letni_indeks: 
    leto : int = field(default=0)  
    skupina_id : int = field(default=0)
    utezi: float = field(default=0)
    letni_iczp: float = field(default=0)

@dataclass_json
@dataclass
class letni_indeksDto: 
    leto : int = field(default=0)  
    skupina_ime: str = field(default="")
    skupina_sifra: str = field(default="")
    letni_iczp: float = field(default=0)

@dataclass_json
@dataclass
class hiczpDto: 
    leto : int = field(default=0)  
    drzava_ime:  str = field(default="")
    skupina_ime: str = field(default="")
    skupina_sifra: str = field(default="")
    utez_hiczp: float = field(default=0)
    letni_hiczp: float = field(default=0)

@dataclass_json
@dataclass
class utez_iczpDto: 
    leto : int = field(default=0)  
    skupina_ime: str = field(default="")
    skupina_sifra: str = field(default="")
    utez: float = field(default=0)

@dataclass_json
@dataclass
class iczp_hiczpDto: 
    leto : int = field(default=0)  
    skupina_ime: str = field(default="")
    skupina_sifra: str = field(default="")
    utez_iczp: float = field(default=0)
    iczp: float = field(default=0)
    utez_hiczp: float = field(default=0)
    hiczp: float = field(default=0)

@dataclass_json
@dataclass
class izdelek: 
    id : int = field(default=0)  
    ime : str = field(default="")
    id_skupine: int=field(default=0)

@dataclass_json
@dataclass
class gibanje_cen: 
    leto : int = field(default=0) 
    id_izdelka: int = field(default=0)
    cena: float = field(default=0)

@dataclass_json
@dataclass
class cenaizdelkaDto: 
    leto : int = field(default=0) 
    ime_izdelka: str = field(default="")
    cena: float = field(default=0)


@dataclass_json
@dataclass
class drzava: 
    id : int = field(default=0) 
    ime : str = field(default="")

@dataclass_json
@dataclass
class inflacija: 
    leto : int = field(default=0) 
    id_drzave : int = field(default=0)
    indeks_inflacije: float = field(default=0)

@dataclass_json
@dataclass
class hiczp: 
    leto : int = field(default=0)  
    skupina_id : int = field(default=0)
    id_drzave : int = field(default=0)
    utezi: float = field(default=0)
    harmoniziran_indeks: float = field(default=0)

@dataclass_json
@dataclass
class hiczpDto: 
    leto : int = field(default=0)  
    ime_skupine: str = field(default="")
    sifra_skupine: str = field(default="")
    ime_drzave: str = field(default="")
    utez: float = field(default=0)
    harmoniziran_indeks: float = field(default=0)

@dataclass_json
@dataclass
class Uporabnik:
    username: str = field(default="")
    role: str = field(default="")
    password_hash: str = field(default="")
    last_login: str = field(default="")

@dataclass
class UporabnikDto:
    username: str = field(default="")
    role: str = field(default="")
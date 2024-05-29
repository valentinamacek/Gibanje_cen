from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime 


#definiramo vse podatkovne modele, ki jih bomo uporabljali v aplikaciji
@dataclass_json
@dataclass
class klasifikacija: 
    id : int = field(default=0)  # Za vsako polje povemo tip in privzeto vrednost
    ime : str = field(default="")

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
class utezi_in_letni_indeksDto: 
    leto : int = field(default=0)  
    skupina_id : int = field(default=0)
    skupina_ime: str = field(default="")
    nadskupina_ime: str = field(default="")
    utezi: float = field(default=0)
    letni_iczp: float = field(default=0)

@dataclass_json
@dataclass
class gibanje_cen: 
    leto : int = field(default=0) 
    izdelek: str = field(default="") 
    id_skupine : int = field(default=0)
    gibanje_cene: float = field(default=0)

@dataclass_json
@dataclass
class gibanje_cenDto: 
    leto : int = field(default=0) 
    izdelek: str = field(default="") 
    id_skupine : int = field(default=0)
    ime_skupine: str = field(default="")
    gibanje_cene: float = field(default=0)

@dataclass_json
@dataclass
class države: 
    id : int = field(default=0) 
    ime : str = field(default="")

@dataclass_json
@dataclass
class inflacija: 
    leto : int = field(default=0) 
    id_drzave : int = field(default=0)
    inflacija_stopnja: float = field(default=0)

@dataclass_json
@dataclass
class hiczp: 
    leto : int = field(default=0)  
    skupina_id : int = field(default=0)
    id_drzave : int = field(default=0)
    utezi: float = field(default=0)
    harmoniziran_indeks: float = field(default=0)


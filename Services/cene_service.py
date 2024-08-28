from Data.repository import Repo
from Data.models import *
from typing import List

class CeneService: 
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_iczp(self) -> List[letni_indeksDto]: 
        return self.repo.dobi_letne_indekse_dto()
    
    def dobi_skupine(self) -> List[klasifikacija]: 
        return self.repo.dobi_skupine()

    def dobi_skupino(self, id) -> klasifikacija: 
        return self.repo.dobi_skupino_iz_id(id)

    def dobi_iczpje_skupine(self, id) -> List[utezi_in_letni_indeks]: 
        return self.repo.dobi_utezi_in_letne_indekse_skupine(id)

    def dobi_hiczpje_drzave_sk(self, id_sk, id_d) -> List[hiczp]: 
        return self.repo.dobi_hiczp_drzave_skupine(id_sk, id_d)
    

       
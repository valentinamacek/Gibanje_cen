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

    def dobi_iczpje_hiczpje_leta(self, leto) -> List[iczp_hiczpDto]: 
        return self.repo.dobi_iczpje_hiczpje_leta(leto)

    def dobi_hiczpje_drzave_sk(self, id_sk, id_d) -> List[hiczp]: 
        return self.repo.dobi_hiczp_drzave_skupine(id_sk, id_d)
    
    def dobi_utez_iczp(self, leto, id_sk) -> utezi_in_letni_indeks: 
        return self.repo.dobi_utez_in_letni_indeks(leto, id_sk)

    def dobi_utez_hiczp(self, leto, id_sk, id_d) -> hiczp: 
        return self.repo.dobi_utez_in_hiczp(leto, id_sk , id_d)

    def dobi_utezi_podskupin(self, leto, id_nadsk) -> List[utez_iczpDto]:
        return self.repo.dobi_utezi_podskupin(leto, id_nadsk)
    
    def dobi_drzave(self) -> List[drzava]: 
        return self.repo.dobi_drzave()

    def dobi_hiczp_drzav(self, leto, id_drzav) -> List[hiczpDto]:
        return self.repo.dobi_hiczp_drzav(leto, id_drzav)

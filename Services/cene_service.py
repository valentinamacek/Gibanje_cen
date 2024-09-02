from Data.repository import Repo
from Data.models import *
from typing import List

class CeneService: 
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_iczp(self) -> List[iczpDto]: 
        return self.repo.dobi_letne_indekse_dto()
    
    def dobi_skupine(self) -> List[klasifikacija]: 
        return self.repo.dobi_skupine()

    def dobi_skupino(self, id) -> klasifikacija: 
        return self.repo.dobi_skupino_iz_id(id)

    def dobi_skupino_iz_sifre(self, sifra) -> klasifikacija:
        return self.repo.dobi_skupino_iz_sifre(sifra)

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

    def dobi_drzavo(self, id_drzave) -> drzava: 
        return self.repo.dobi_drzavo(id_drzave)

    def dobi_inflacije_drzave(self, id_drzave)-> List[inflacija]: 
        return self.repo.dobi_ind_inflacije_drzave(id_drzave)

    def dobi_inflacijo(self, leto, id_drzave) -> inflacija: 
        return self.repo.dobi_inflacijo(leto, id_drzave)

    def dobi_hiczp_drzav(self, leto, id_drzav) -> List[hiczpDto]:
        return self.repo.dobi_hiczp_drzav(leto, id_drzav)

    def dobi_ceno_izdelkov_skupine(self, id_skupine, leto) -> List[cenaizdelkaDto]:
        return self.repo.dobi_ceno_izdelkov_skupine(id_skupine, leto)  

    def dobi_cene_dto(self) -> List[gibanje_cenDto]: 
        return self.repo.dobi_cene_dto()

    def dodaj_iczp(self, leto, skupina_id, utez, iczp): 
        uil = utezi_in_letni_indeks(leto = leto, skupina_id=skupina_id, utezi=utez, letni_iczp=iczp)
        return self.repo.dodaj_utez_in_letni_indeks(uil)

    def izbrisi_iczp(self, id_skupine, leto): 
        return self.repo.izbrisi_iczp(id_skupine, leto)
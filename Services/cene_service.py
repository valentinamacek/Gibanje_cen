from Data.repository import Repo
from Data.models import *
from typing import List

class CeneService: 
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_iczp(self) -> List[utezi_in_letni_indeks]: 
        return self.repo.dobi_utezi_in_letne_indekse()

       
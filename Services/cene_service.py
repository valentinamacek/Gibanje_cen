from Data.repository import Repo
from Data.models import *
from typing import List

class CeneService: 
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_iczp(self) -> List[letni_indeksDto]: 
        return self.repo.dobi_letne_indekse_dto()



       
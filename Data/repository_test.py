from repository import Repo
from models import *


repo = Repo()

# Dobimo vse osebe

skupine = repo.dobi_utezi_podskupin(2017, 1)

for s in skupine: 
    print(s)


  
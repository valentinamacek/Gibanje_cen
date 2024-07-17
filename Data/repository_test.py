from repository import Repo
from models import *


repo = Repo()

# Dobimo vse osebe

skupine = repo.dobi_utezi_in_letne_indekse()

for s in skupine: 
    print(s)
  
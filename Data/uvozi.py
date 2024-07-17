import pandas as pd
import numpy as np
from Data.repository import Repo
from Data.models import klasifikacija, nivoji

repo = Repo()

df = pd.read_excel('Data\ecoicop_klasifikacija.xlsx')

print(df.head())

data = df.to_numpy()
print(data[1])

#data-numpy array oblike: [2 '01.1' 'Hrana' 'Food' '01']
#                         [0raven 1sifra 2ime 3ang_ime 4sifra_starsa]
def uvoz_v_tabelo_klasifikacija(data, stevec): 
    for klas in data: 
        repo.dodaj_klas(klasifikacija(ime=klas[2],
                                      ang_ime=klas[3],
                                      sifra=klas[1],
                                      raven=klas[0]))
        stevec = stevec +1 
        if klas[0] != 1: 
           nad_skupina = repo.dobi_skupino_iz_sifre(klas[4])
           repo.dodaj_nivo(nivoji(id_podskupine=stevec, id_nadskupine=nad_skupina.id))

uvoz_v_tabelo_klasifikacija(data[65: ], 66)


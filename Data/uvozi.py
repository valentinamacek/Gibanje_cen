import pandas as pd
import numpy as np
from Data.repository import Repo
from Data.models import klasifikacija, nivoji, utezi_in_letni_indeks, drzava, inflacija, izdelek, gibanje_cen

repo = Repo()

df = pd.read_excel('Data\ecoicop_klasifikacija.xlsx')

# print(df.head())

data = df.to_numpy()


#data-numpy array oblike: [2 '01.1' 'Hrana' 'Food' '01']
#                         [0raven 1sifra 2ime 3ang_ime 4sifra_starsa]
def uvoz_v_tabelo_klasifikacija(data, stevec): 
    for klas in data: 
        stevec = stevec +1 
        repo.dodaj_klas(klasifikacija(id=stevec, 
                                      ime=klas[2],
                                      ang_ime=klas[3],
                                      sifra=klas[1],
                                      raven=klas[0]))
        if klas[0] != 1: 
           nad_skupina = repo.dobi_skupino_iz_sifre(klas[4])
           repo.dodaj_nivo(nivoji(id_podskupine=stevec, id_nadskupine=nad_skupina.id))

# uvoz_v_tabelo_klasifikacija(data[65: ], 66)

dfind = pd.read_excel('Data\\utezi_in_letni_iczp.xlsx')


dfind.replace(to_replace="...", value='', inplace=True)
dfind.replace(to_replace="-", value='', inplace=True)

data_ind=dfind.to_numpy()

print(data_ind[ :30])

k = len(data_ind)
 
# print(data_ind[k-20: ])

#['SKUPAJ' '2000M12' 100 nan '' nan]
#[0skupina 1leto 2utez 3 4iczp 5]

def uvoz_v_utezi_in_letni_indeks(data): 
    stevec = 0
    while stevec < len(data): 
        vrstica = data[stevec]
        if '2000M12'== vrstica[1]:
            if vrstica[0]== 'SKUPAJ': 
                skupina = repo.dobi_skupino_iz_sifre('0')
            else:
                sifra, ime =vrstica[0].split(' ',1)
                skupina = repo.dobi_skupino_iz_sifre(sifra)
            stevec_notranji = 0
            vrstica_skupine = vrstica 
            while vrstica_skupine[1] != '2024M06': 
                leto = int(vrstica_skupine[1][:4])
                utez = vrstica_skupine[2]
                letni_iczp = vrstica_skupine[4]
                repo.dodaj_utez_in_letni_indeks(utezi_in_letni_indeks(leto=leto, skupina_id=skupina.id, utezi=utez, letni_iczp=letni_iczp))
                stevec_notranji +=1
                vrstica_skupine = data[stevec + stevec_notranji]
            stevec = stevec + stevec_notranji + 1
        else: 
            stevec +=1 

            
# uvoz_v_utezi_in_letni_indeks(data_ind[: k-18])

dfinf = pd.ExcelFile('Data\\inflacija_n.xlsx')

data_inf = pd.read_excel(dfinf, 'Sheet 1')

data_inf = data_inf.to_numpy() 


def uvoz_v_tabelo_inflacija(data) : 
   
    for i,el in enumerate(data_inf):
        if 'TIME'==el[0]: 
            leta = el 
            ind = i 
            break 
    
#ind ind+1 Cr: ind+2 It: ind+3 Hu: ind+4 Au: ind+5 Sl: ind+6 
    id_drzave = 0
    for i in range(ind+2, ind+7): 
        id_drzave +=1
        vrstica_drzave = data[i]
        ime_drzave = vrstica_drzave[0]
        repo.dodaj_drzavo(drzava(id=id_drzave, ime=ime_drzave))
        j=0
        for infl in vrstica_drzave[1:]: 
            j +=1 
            if not pd.isna(infl) and infl != 'd': 
                leto = int(leta[j][ :4])
                indeks_infl = infl + 100 
                repo.dodaj_ind_inflacije(inflacija(leto=leto, id_drzave=id_drzave, indeks_inflacije=indeks_infl))

              
#uvoz_v_tabelo_inflacija(data_inf)
dfcene = pd.read_excel('Data\\povprecne_cene.xlsx')

data_cene = dfcene.to_numpy()

print(data_cene[:30])

# print(data_cene[2])

def uvoz_v_tabelo_gibanje_cen(data): 
    leta = data[2][1: ]
    skupina = 0
    stevec = 1
    for vrstica in data[3:]: 
        if vrstica[0] == 'DRUGI IZDELKI IN STORITVE': 
            break
        elif vrstica[0].startswith("..."): 
            ime_izdelka = vrstica[0].replace("...", "")
            repo.dodaj_izdelek(izdelek(id=stevec, ime=ime_izdelka, id_skupine=skupina))
            for i,cena in enumerate(vrstica[1:]):
                leto = int(leta[i])
                repo.dodaj_ceno(gibanje_cen(leto=leto, id_izdelka=stevec, cena=cena))
            stevec +=1
        else: 
            sifra, ime =vrstica[0].split(' ',1)
            sk = repo.dobi_skupino_iz_sifre(sifra)
            skupina = sk.id 
            
uvoz_v_tabelo_gibanje_cen(data_cene)

# def dobi_skupino_ali_ne(stri): 
#     try: 
#         sk = repo.dobi_skupino_iz_sifre(stri)
#         return sk 
#     except AttributeError: 
#         return None 

# dobi_skupino_ali_ne('13')
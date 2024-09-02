from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os
import io
import base64
import matplotlib.pyplot as plt
import math
import numpy as np

from Services.cene_service import CeneService 
from Services.auth_service import AuthService

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

auth = AuthService()
service = CeneService()


def generate_graf_indeksov(lst_indeksov, hiczp): 
    #izrise graf primerjave icžp in hizcžp(za Slovenijo)
    plt.clf()

    plt.figure(figsize=(12, 4)) 

    xy = []
    if lst_indeksov: 
     skupina_id = lst_indeksov[0].skupina_id
    else: 
     skupina_id = hiczp[0].skupina_id

    for indeks in lst_indeksov: 
        if indeks.letni_iczp != None: 
           xy.append((indeks.leto, indeks.letni_iczp) )
    xy.sort()
    x = []
    y = []
    for (zi, wi) in xy: 
        x.append(zi)
        y.append(wi)
    
    plt.plot(x,y, color='red', label='ICŽP')
 
    zw = []
    for hi in hiczp:
        if skupina_id != 1: 
         if hi.harmoniziran_indeks != None: 
            zw.append((hi.leto, hi.harmoniziran_indeks)) 
        else:
         if hi.indeks_inflacije != None: 
            zw.append((hi.leto, hi.indeks_inflacije)) 
    zw.sort()
    z = []
    w = []
    for (zi, wi) in zw: 
        z.append(zi)
        w.append(wi)
 
    plt.plot(z, w, color='blue', label='HICŽP za Slovenijo' )
    w.extend(y)
    r = math.ceil(max(w)) - math.floor(min(w))
    yticksh = [math.floor(min(w)) + i for i in range(0, r+1)]
    yticks = [math.floor(min(w)) + i for i in range(0, r+1,2)]

    plt.yticks(yticks)

    for yt in yticksh:
        plt.axhline(y=yt, color='gray', linestyle='--', linewidth=0.5)
    
    plt.xticks([i for i in range(2000, 2024)])
    plt.xlabel('Leto')
    plt.ylabel('icžp')
    plt.title('Primerjava icžp in hicžp po letih')
    plt.legend(title='Indeks', loc='best')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert the image to a base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
       
    return img_base64

def generate_graf_utezi(lst_indeksov, hiczp): 
    #izrise graf primerjave uteži icžp in hizcžp(za Slovenijo)
    plt.clf()

    plt.figure(figsize=(12, 4)) 

    xy = []

    for indeks in lst_indeksov: 
        if indeks.utezi != None: 
           xy.append((indeks.leto, indeks.utezi) )
    xy.sort()
    x = []
    y = []
    for (zi, wi) in xy: 
        x.append(zi)
        y.append(wi)
    
    plt.plot(x,y, color='red', label='uteži ICŽP')
 
    zw = []
    for hi in hiczp:
         if hi.utezi != None: 
            zw.append((hi.leto, hi.utezi)) 
    zw.sort()
    z = []
    w = []
    for (zi, wi) in zw: 
        z.append(zi)
        w.append(wi)
 
    plt.plot(z, w, color='blue', label='uteži HICŽP za Slovenijo' )
    w.extend(y)
    r = math.ceil(max(w)) - math.floor(min(w))
    yticksh = [math.floor(min(w)) + i for i in range(0, r+1)]
    yticks = [math.floor(min(w)) + i for i in range(0, r+1,2)]

    plt.yticks(yticks)

    for yt in yticksh:
        plt.axhline(y=yt, color='gray', linestyle='--', linewidth=0.5)
    
    plt.xticks([i for i in range(2000, 2024)])
    plt.xlabel('Leto')
    plt.ylabel('uteži')
    plt.title('Primerjava uteži za icžp in hicžp po letih')
    plt.legend(title='Indeks', loc='best')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert the image to a base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
       
    return img_base64

def generate_graf_inflacija(infl_list): 
    #izrise graf primerjave icžp in hizcžp(za Slovenijo)
    plt.clf()

    plt.figure(figsize=(12, 4)) 

    xy = []
   

    for infl in infl_list: 
        if infl.indeks_inflacije != None: 
           xy.append((infl.leto, infl.indeks_inflacije) )
    xy.sort()
    x = []
    y = []
    for (zi, wi) in xy: 
        x.append(zi)
        y.append(wi)
    
    plt.plot(x,y, color='red')
 
    r = math.ceil(max(y)) - math.floor(min(y))
    yticksh = [math.floor(min(y)) + i for i in range(0, r+1)]
    yticks = [math.floor(min(y)) + i for i in range(0, r+1,2)]

    plt.yticks(yticks)

    for yt in yticksh:
        plt.axhline(y=yt, color='gray', linestyle='--', linewidth=0.5)
    
    plt.xticks([i for i in range(2000, 2024)])
    plt.xlabel('Leto')
    plt.ylabel('indeks_inflacije')
    plt.title('Spreminjanje indeksa inflacije po letih')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert the image to a base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
       
    return img_base64

def generate_grafdrzav(skupina, nacin): 
    #sestavi graf, ki vsebuje grafikone spreminjanja hiczp / utezi cez leta za vse drzave
    plt.clf()

    plt.figure(figsize=(13, 4)) 
    vsi_y = []
    drzave = service.dobi_drzave()
    colors = ['red', 'blue', 'purple', 'orange', 'green']
    for i, drzava in enumerate(drzave): 
        if skupina.id != 1:
            hiczpji = service.dobi_hiczpje_drzave_sk(skupina.id, drzava.id)
            zw = []
            for hi in hiczpji:
                if nacin == 'hiczp': 
                    if hi.harmoniziran_indeks != None: 
                       zw.append((hi.leto, hi.harmoniziran_indeks)) 
                else:
                    if hi.utezi != None: 
                       zw.append((hi.leto, hi.utezi)) 
        else:
            inflacije = service.dobi_inflacije_drzave(drzava.id)
            zw = []
            for hi in inflacije:
                if hi.indeks_inflacije != None: 
                    zw.append((hi.leto, hi.indeks_inflacije)) 
        zw.sort()
        z = []
        w = []
        for (zi, wi) in zw: 
            z.append(zi)
            w.append(wi)
    
        plt.plot(z, w, color=colors[i], label=f'{drzava.ime}' )
        vsi_y.extend(w)

    r = math.ceil(max(vsi_y)) - math.floor(min(vsi_y))
    yticksh = [math.floor(min(vsi_y)) + i for i in range(0, r+1)]
    yticks = [math.floor(min(vsi_y)) + i for i in range(0, r+1,2)]

    plt.yticks(yticks)

    for yt in yticksh:
        plt.axhline(y=yt, color='gray', linestyle='--', linewidth=0.5)

    plt.xticks([i for i in range(2000, 2024)])
    plt.xlabel('Leto')
    plt.ylabel(f'{nacin}')
    plt.title(f'Primerjava {nacin} med državami po letih')
    plt.legend(title='Indeks', loc='best')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the image to a base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return img_base64

#za izpis dejanskih utezi v pie_chartu: 
def func(pct, allvals):
    absolute = np.round(pct/100.*np.sum(allvals),1)
    return f"{absolute}"

def generate_pie(lst_utezi): 

    plt.clf()
    
    velikosti = []
    labels = []
    for utez_dto in lst_utezi: 
        velikosti.append(utez_dto.utez)
        labels.append(utez_dto.skupina_ime)
    plt.pie(velikosti, labels=labels,  autopct=lambda pct: func(pct, velikosti))
    plt.title('Pomembnost podskupin v ICŽP', fontdict={'fontsize': 16, 'fontweight': 'bold'})

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert the image to a base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
       
    return img_base64


def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")
        
    return decorated

@get('/')
@cookie_required
def index(): 

    iczpji = service.dobi_iczp()
    return template_user('home.html', iczpji=iczpji)

@get('/izbrisi_iczp/<id_skupine:int>/<leto:int>')
@cookie_required
def izbrisi_iczp(id_skupine, leto):
    service.izbrisi_iczp(id_skupine, leto)

    iczpji = service.dobi_iczp()
    return template_user('home.html', iczpji=iczpji)

@get('/dodaj_iczp')
@cookie_required
def dodaj_iczp(): 
    return template_user('dodaj_iczp.html')

@post('/dodaj_iczp')
@cookie_required
def dodaj_iczp_post(): 
    leto = int(request.forms.get('leto'))
    sifra_skupine = request.forms.get('skupina')
    skupina = service.dobi_skupino_iz_sifre(sifra_skupine)
    utez = float(request.forms.get('utez'))
    iczp = float(request.forms.get('iczp'))
    service.dodaj_iczp(leto, skupina.id, utez, iczp)

    iczpji = service.dobi_iczp()
    return template_user('home.html', iczpji=iczpji)

@get('/skupine')
@cookie_required
def skupine(): 
      
    skupine = service.dobi_skupine()
    return template_user('skupine.html', skupine=skupine)

@get('/skupina/<id_skupine:int>')
@cookie_required
def skupina(id_skupine): 
      
    skupina = service.dobi_skupino(id_skupine)
    iczpji = service.dobi_iczpje_skupine(id_skupine)
    if id_skupine != 1:
        hiczp = service.dobi_hiczpje_drzave_sk(id_skupine, 5)
    else:
        hiczp = service.dobi_inflacije_drzave(5)
    if iczpji or hiczp: 
      graf_base64 = generate_graf_indeksov(iczpji, hiczp)
      return template_user('skupina.html', skupina= skupina, chart_base64=graf_base64, prikaz="hiczp in iczp", napaka='')
    else: 
      graf_base64 = ''
      return template_user('skupina.html', skupina= skupina, chart_base64=graf_base64, prikaz="hiczp in iczp", napaka='Za izbrano skupino ni podatkov')


@get('/skupinahd/<id_skupine:int>')
@cookie_required
def skupinahd(id_skupine): 
    skupina = service.dobi_skupino(id_skupine)
    hdgraf = generate_grafdrzav(skupina, 'hiczp')
    return template_user('skupina.html', skupina = skupina, chart_base64=hdgraf, prikaz="hiczp drzave")

@get('/skupinau/<id_skupine:int>')
@cookie_required
def skupinau(id_skupine): 
      
    skupina = service.dobi_skupino(id_skupine)
    iczpji = service.dobi_iczpje_skupine(id_skupine)
    hiczp = service.dobi_hiczpje_drzave_sk(id_skupine, 5)
    graf_base64 = generate_graf_utezi(iczpji, hiczp)
    return template_user('skupina.html', skupina= skupina, chart_base64=graf_base64, prikaz="utezi")
        
@get('/skupinahu/<id_skupine:int>')
@cookie_required
def skupinahu(id_skupine): 
    skupina = service.dobi_skupino(id_skupine)
    hdgraf = generate_grafdrzav(skupina, 'utezi')
    return template_user('skupina.html', skupina = skupina, chart_base64=hdgraf, prikaz="utezi drzave")



@get('/skupinaleto/<id_skupine:int>/<leto:int>')
@cookie_required
def skupinaleto(id_skupine, leto): 
    
    skupina = service.dobi_skupino(id_skupine)
    utez_iczp = service.dobi_utez_iczp(leto, id_skupine)
    if id_skupine != 1: 
       utez_hiczp = service.dobi_utez_hiczp(leto, id_skupine, 5)
    else: 
       utez_hiczp = service.dobi_inflacijo(leto, 5)
    cene_izdelkov = service.dobi_ceno_izdelkov_skupine( id_skupine, leto) 
    utezi_podskupin = service.dobi_utezi_podskupin(leto, id_skupine)
    if utezi_podskupin == []:
        return template_user('skupina_leto.html', skupina=skupina, utez_iczp = utez_iczp, utez_hiczp = utez_hiczp, cene_izdelkov=cene_izdelkov, chart_base64="" )
    else: 
        pie_base64 = generate_pie(utezi_podskupin)
        return template_user('skupina_leto.html', skupina=skupina, utez_iczp = utez_iczp, utez_hiczp = utez_hiczp, cene_izdelkov=cene_izdelkov, chart_base64=pie_base64)

@get('/cene')
@cookie_required
def cene(): 
    cene = service.dobi_cene_dto()
    return template_user('cene.html', cene=cene)


@get('/leta')
@cookie_required
def leta(): 
    leta = [i for i in range(2000, 2024)]
    return template_user('leta.html', leta=leta)

@post('/leta')
@cookie_required
def leta_post():
    leto = int(request.forms.get('leto'))
    primerjava = int(request.forms.get('prikaz'))

    if int(primerjava) == 1:  # Primerjava ICŽP in HICŽP
        indeksi = service.dobi_iczpje_hiczpje_leta(int(leto))
        return template_user('iczp_hiczp_leta.html', indeksi=indeksi)
    else:  # Primerjava po državah
        drzave = service.dobi_drzave()
        return template_user('leto_po_drzavah.html', leto=leto, drzave=drzave)
        
@get('/leto_drzave/<leto:int>')
@cookie_required
def leto_drzave(leto): 
    drzave = service.dobi_drzave()
    return template_user('leto_po_drzavah.html', leto=leto, drzave=drzave)
        

@post('/leto_drzave')
@cookie_required
def leto_drzave_post(): 
    leto = int(request.forms.get('leto'))
    id_list = request.forms.getall('countries')
    id_drzav = [int(id) for id in id_list]
    sez = service.dobi_hiczp_drzav(leto, id_drzav)
    return template_user('leto_izbrane_drzave', hiczpji=sez)

@get('/drzave')
@cookie_required
def drzave(): 
    drzave = service.dobi_drzave()
    return template_user('drzave.html', drzave=drzave)

@get('/drzava/<id_drzave:int>')
@cookie_required
def drzava(id_drzave): 
    inflacije = service.dobi_inflacije_drzave(id_drzave)
    drzava = service.dobi_drzavo(id_drzave)
    inflbase64 = generate_graf_inflacija(inflacije)
    return template_user('drzava.html', drzava = drzava, inflacije = inflacije, chart_base64 = inflbase64)


@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        auth.dodaj_uporabnika(username, 'visitor', password)

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)
        
        # redirect v večino primerov izgleda ne deluje
        redirect(url('/'))

        # Uporabimo kar template, kot v sami "index" funkciji

        # transakcije = service.dobi_transakcije()        
        # return template('transakcije.html', transakcije = transakcije)
        
    else:
        return template("prijava.html", uporabnik=None, rola=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")


auth.dodaj_uporabnika('vale', 'admin', 'izzy')

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
    
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    
    return template('prijava.html', uporabnik=None, rola=None, napaka=None)


@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


if __name__ == "__main__":

    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
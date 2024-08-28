from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os
import io
import base64
import matplotlib.pyplot as plt

from Services.cene_service import CeneService 
from Services.auth_service import AuthService

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

auth = AuthService()
service = CeneService()


def generate_graf_indeksov(lst_indeksov, hiczp): 

    plt.clf()

    plt.figure(figsize=(12, 4)) 

    xy = []

    for indeks in lst_indeksov: 
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
        zw.append((hi.leto, hi.harmoniziran_indeks)) 
    zw.sort()
    z = []
    w = []
    for (zi, wi) in zw: 
        z.append(zi)
        w.append(wi)
 
    plt.plot(z, w, color='blue', label='HICŽP za Slovenijo' )

    yticks = plt.yticks()[0]  # Get the current y-tick values
    for yt in yticks:
        plt.axhline(y=yt, color='gray', linestyle='--', linewidth=0.5)
    
    plt.xticks([i for i in range(2000, 2024)])
    plt.xlabel('Leto')
    plt.ylabel('icžp')
    plt.title('Spreminjanje icžp in hicžp z leti')
    plt.legend(title='Indeks', loc='best')
    
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
    hiczp = service.dobi_hiczpje_drzave_sk(id_skupine, 5)
    graf_base64 = generate_graf_indeksov(iczpji, hiczp)
    return template_user('skupina.html', skupina= skupina, chart_base64=graf_base64)

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


@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


if __name__ == "__main__":

    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
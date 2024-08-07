import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import os

from Data.models import klasifikacija, nivoji, utezi_in_letni_indeks, utezi_in_letni_indeksDto, gibanje_cen, izdelek, drzava, inflacija, hiczp, hiczpDto, Uporabnik, UporabnikDto
from typing import List 

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

#Repo je razred, ki bo vseboval metode za delo z bazo: 

class Repo: 
    def __init__(self): 
      self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
      self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    def dobi_skupino_iz_id(self, id_skupine: int) -> klasifikacija:
        self.cur.execute("""
            SELECT id, ime, ang_ime, sifra, raven
            FROM klasifikacija
            WHERE id = %s
        """, (id_skupine,))
        s = klasifikacija.from_dict(self.cur.fetchone())
        return s 

    def dobi_skupino_iz_sifre(self, sifra: str) -> klasifikacija: 
        self.cur.execute("""
            SELECT id, ime, ang_ime, sifra, raven
            FROM klasifikacija
            WHERE sifra = %s
        """, (sifra,))
        s = klasifikacija.from_dict(self.cur.fetchone())
        return s 

    def dobi_skupino_iz_ang_imena(self, ang_ime: str) -> List[klasifikacija]: 
        self.cur.execute("""
            SELECT id, ime, ang_ime, sifra, raven
            FROM klasifikacija
            WHERE ang_ime = %s
        """, (ang_ime,))
        skji = [klasifikacija.from_dict(t) for t in self.cur.fetchall()]
        if skji == []: 
            self.cur.execute("""
            SELECT id, ime, ang_ime, sifra, raven
            FROM klasifikacija
            WHERE ang_ime = %s
            """, (ang_ime.upper(),))
            skji = [klasifikacija.from_dict(t) for t in self.cur.fetchall()]
        return skji 

    def dodaj_klas(self, klas: klasifikacija):
        self.cur.execute("""
            INSERT into klasifikacija(id, ime, ang_ime, sifra, raven)
            VALUES (%s, %s, %s, %s, %s)
            """, (klas.id, klas.ime, klas.ang_ime, klas.sifra, klas.raven))
        self.conn.commit()
    
    def dodaj_nivo(self, nivoji: nivoji): 
        self.cur.execute("""
            INSERT into nivoji(id_podskupine, id_nadskupine)
            VALUES (%s, %s)
            """, (nivoji.id_podskupine, nivoji.id_nadskupine))
        self.conn.commit()

    #def dobi_visji_nivo_skupine(self) -> kaj ce ga nima?
    def dobi_utezi_in_letne_indekse(self) -> List[utezi_in_letni_indeks]:
        self.cur.execute("""
            SELECT leto, skupina_id, utezi, letni_iczp 
            FROM utezi_in_letni_indeks
        """)
        u_iczp = [utezi_in_letni_indeks.from_dict(t) for t in self.cur.fetchall()]
        return u_iczp

    def dobi_utez_in_letni_indeks(self, leto, skupina_id)-> utezi_in_letni_indeks: 
        self.cur.execute("""
            SELECT leto, skupina_id, utezi, letni_iczp 
            FROM utezi_in_letni_indeks
            WHERE leto = %s
            AND skupina_id =%s
        """,(leto, skupina_id))

        ul = utezi_in_letni_indeks.from_dict(self.cur.fetchone())
        return ul 
    
    def dobi_utezi_in_letne_indekse_skupine(self, skupina_id):
        self.cur.execute("""
            SELECT leto, skupina_id, utezi, letni_iczp 
            FROM utezi_in_letni_indeks
            WHERE skupina_id =%s
        """, (skupina_id,))
        u_iczp = [utezi_in_letni_indeks.from_dict(t) for t in self.cur.fetchall()]
        return u_iczp
        
    def dodaj_utez_in_letni_indeks(self, uil: utezi_in_letni_indeks): 
        if uil.utezi == '': 
            uil.utezi = None
        if uil.letni_iczp == '': 
            uil.letni_iczp = None 
        self.cur.execute("""
            INSERT into utezi_in_letni_indeks(leto, skupina_id, utezi, letni_iczp)
            VALUES (%s, %s, %s, %s)
            """, (uil.leto, uil.skupina_id, uil.utezi, uil.letni_iczp))
        self.conn.commit()
    
    def dodaj_hiczp(self, hiczp: hiczp): 
        self.cur.execute("""
            INSERT into hiczp(leto, skupina_id, id_drzave, utezi, harmoniziran_indeks)
            VALUES (%s, %s, %s, %s, %s)
            """, (hiczp.leto, hiczp.skupina_id, hiczp.id_drzave, hiczp.utezi, hiczp.harmoniziran_indeks))
        self.conn.commit()
    
    def dodaj_utez(self, hiczp: hiczp): 
        self.cur.execute("""
            UPDATE hiczp
            SET utezi=%s
            WHERE leto=%s
            AND skupina_id=%s 
            AND id_drzave=%s
            """, [hiczp.utezi, hiczp.leto, hiczp.skupina_id, hiczp.id_drzave])
        self.conn.commit()

    # UPDATE table_name
    # SET column1 = value1, column2 = value2, ...
    # WHERE condition;


    def dodaj_drzavo(self, drzava: drzava): 
        self.cur.execute("""
            INSERT into drzava(id, ime)
            VALUES (%s, %s)
            """, (drzava.id, drzava.ime))
        self.conn.commit()
    
    def dodaj_ind_inflacije(self, inflacija: inflacija): 
        self.cur.execute("""
            INSERT into inflacija(leto, id_drzave, indeks_inflacije)
            VALUES (%s, %s, %s)
            """, (inflacija.leto, inflacija.id_drzave, inflacija.indeks_inflacije))
        self.conn.commit()

    def dodaj_izdelek(self, izdelek:izdelek): 
        self.cur.execute("""
            INSERT into izdelki(id, ime, id_skupine)
            VALUES (%s, %s, %s)
            """, (izdelek.id, izdelek.ime, izdelek.id_skupine))
        self.conn.commit()

    def dodaj_ceno(self, cena:gibanje_cen):
        if cena.cena == '-' : 
           cena.cena = None 
        self.cur.execute("""
            INSERT into gibanje_cen(leto, id_izdelka, cena)
            VALUES (%s, %s, %s)
            """, (cena.leto, cena.id_izdelka, cena.cena))
        self.conn.commit()



    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT into uporabniki(username, role, password_hash, last_login)
            VALUES (%s, %s, %s, %s)
            """, (uporabnik.username,uporabnik.role, uporabnik.password_hash, uporabnik.last_login))
        self.conn.commit()

    def dobi_uporabnika(self, username:str) -> Uporabnik:
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cur.execute("""
            SELECT username, role, password_hash, last_login
            FROM uporabniki
            WHERE username = %s
        """, (username,))

        u = Uporabnik.from_dict(self.cur.fetchone())
        return u
    
    def posodobi_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            Update uporabniki set last_login = %s where username = %s
            """, (uporabnik.last_login,uporabnik.username))
        self.conn.commit()

    
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import os

from Data.models import klasifikacija, nivoji, utezi_in_letni_indeks, utezi_in_letni_indeksDto, gibanje_cen, gibanje_cenDto, drzava, inflacija, hiczp, hiczpDto, Uporabnik, UporabnikDto
from typing import List 

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

#Repo je razred, ki bo vseboval metode za delo z bazo: 

class Repo: 
    def __init__(self): 
      self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
      self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    def dobi_skupino(self, id_skupine: int) -> klasifikacija:
        self.cur.execute("""
            SELECT id, ime
            FROM klasifikacija
            WHERE id = %s
        """, (id_skupine,))
        s = klasifikacija.from_dict(self.cur.fetchone())
        return s 
    
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

    
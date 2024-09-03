import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import os

from Data.models import *
from typing import List 

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

#Repo je razred, ki bo vseboval metode za delo z bazo: 

class Repo: 
    def __init__(self): 
      self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
      self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    def dobi_skupine(self) -> List[klasifikacija]:
        self.cur.execute("""
            SELECT id, ime, ang_ime, sifra, raven
            FROM klasifikacija
            ORDER BY id 
        """)
        skupine = [klasifikacija.from_dict(t) for t in self.cur.fetchall()]
        return skupine

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

    def dobi_skupine_dol_ravni(self, raven) -> List[klasifikacija]: 
        self.cur.execute("""
            SELECT id, ime, ang_ime, sifra, raven
            FROM klasifikacija
            WHERE raven = %s
        """, (raven,))
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

    def dobi_letne_indekse_dto(self) -> List[iczpDto]:
        self.cur.execute("""
            SELECT leto, k.id AS skupina_id, k.ime AS skupina_ime, k.sifra AS skupina_sifra, utezi, letni_iczp
            FROM utezi_in_letni_indeks JOIN klasifikacija k ON skupina_id = id
        """)
        iczpdto = [iczpDto.from_dict(t) for t in self.cur.fetchall()]
        return iczpdto

    def dobi_utez_in_letni_indeks(self, leto, skupina_id)-> utezi_in_letni_indeks: 
        self.cur.execute("""
            SELECT leto, skupina_id, utezi, letni_iczp 
            FROM utezi_in_letni_indeks
            WHERE leto = %s
            AND skupina_id =%s
        """,(leto, skupina_id))

        ul = utezi_in_letni_indeks.from_dict(self.cur.fetchone())
        return ul 

    def izbrisi_iczp(self, skupina_id, leto): 
        self.cur.execute("""
            DELETE FROM utezi_in_letni_indeks
            WHERE skupina_id = %s
            AND leto = %s
            """, (skupina_id, leto))
        self.conn.commit()
    
    def dobi_utezi_in_letne_indekse_skupine(self, skupina_id)-> List[utezi_in_letni_indeks]:
        self.cur.execute("""
            SELECT leto, skupina_id, utezi, letni_iczp 
            FROM utezi_in_letni_indeks
            WHERE skupina_id =%s
        """, (skupina_id,))
        u_iczp = [utezi_in_letni_indeks.from_dict(t) for t in self.cur.fetchall()]
        return u_iczp
        
    def dobi_iczpje_hiczpje_leta(self, leto) -> List[iczp_hiczpDto]:
        self.cur.execute("""
            SELECT u.leto AS leto, k.ime AS skupina_ime, k.sifra AS skupina_sifra, u.utezi AS utez_iczp , u.letni_iczp AS iczp, h.utezi AS utez_hiczp , h.harmoniziran_indeks AS hiczp
            FROM utezi_in_letni_indeks u
            FULL JOIN hiczp h ON u.leto = h.leto AND u.skupina_id = h.skupina_id
            JOIN klasifikacija k ON u.skupina_id = k.id
            WHERE u.leto =%s
            AND h.id_drzave=%s
            ORDER BY k.id
        """, (leto,5))#to ustreza samo za hiczpje od Slovenije
        hi_iczp = [iczp_hiczpDto.from_dict(t) for t in self.cur.fetchall()]
        return hi_iczp
    
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

    def dobi_hiczp_drzave_skupine(self, skupina_id, drzava_id)-> List[hiczp]:
        self.cur.execute("""
            SELECT leto, skupina_id, id_drzave, utezi, harmoniziran_indeks 
            FROM hiczp
            WHERE skupina_id =%s
            AND id_drzave =%s
        """, (skupina_id, drzava_id))
        hiczpj = [hiczp.from_dict(t) for t in self.cur.fetchall()]
        return hiczpj

    def dobi_hiczp_drzave(self, drzava_id) -> List[hiczpDto]: 
        self.cur.execute("""
            SELECT leto, k.ime AS ime_skupine, k.sifra AS sifra_skupine, utezi AS utez, harmoniziran_indeks 
            FROM hiczp 
            JOIN klasifikacija k ON skupina_id = id 
            WHERE id_drzave =%s
        """, (drzava_id,))
        hiczpj = [hiczpDto.from_dict(t) for t in self.cur.fetchall()]
        return hiczpj

    def dobi_utez_in_hiczp(self, leto, skupina_id, drzava_id) -> hiczp:
        self.cur.execute("""
            SELECT leto, skupina_id, id_drzave, utezi, harmoniziran_indeks 
            FROM hiczp
            WHERE leto = %s
            AND skupina_id =%s
            AND id_drzave =%s
        """, (leto, skupina_id, drzava_id))
    
        ul = hiczp.from_dict(self.cur.fetchone())
        return ul 

    def dobi_utezi_podskupin(self, leto, id_nadskupine) -> List[utez_iczpDto]: 
        self.cur.execute("""
            SELECT u.leto AS leto, k.ime AS skupina_ime, k.sifra AS skupina_sifra, u.utezi AS utez
            FROM utezi_in_letni_indeks u
            JOIN klasifikacija k on u.skupina_id = k.id
            JOIN nivoji n on u.skupina_id = n.id_podskupine
            WHERE u.leto = %s
            AND n.id_nadskupine=%s
        """, (leto, id_nadskupine))
        utezi = [utez_iczpDto.from_dict(t) for t in self.cur.fetchall()]
        return utezi
    
    def dobi_hiczp_drzav(self, leto, id_drzav) -> List[hiczpDto]: 
        placeholders = ', '.join(['%s'] * len(id_drzav))
        id_drzav.append(leto)
        tupl_vseh = tuple(id_drzav)
        self.cur.execute(f"""
            SELECT h.leto AS leto, k.ime AS ime_skupine, k.sifra AS sifra_skupine, d.ime AS ime_drzave, h.utezi AS utez, h.harmoniziran_indeks AS harmoniziran_indeks
            FROM hiczp h 
            JOIN drzava d ON h.id_drzave = d.id
            JOIN klasifikacija k ON h.skupina_id = k.id
            WHERE h.id_drzave IN ({placeholders})
            AND h.leto = %s
            """, tupl_vseh
        )
        hiczpji = [hiczpDto.from_dict(t) for t in self.cur.fetchall()]
        return hiczpji 
    
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
    def dobi_drzave(self)-> List[drzava]: 
        self.cur.execute("""
            SELECT id, ime
            FROM drzava
        """)
        drzave = [drzava.from_dict(t) for t in self.cur.fetchall()]
        return drzave

    def dobi_drzavo(self, id_drzave)-> drzava: 
        self.cur.execute("""
            SELECT id, ime
            FROM drzava
            WHERE id=%s
        """, (id_drzave, ))
        d = drzava.from_dict(self.cur.fetchone())
        return d
 

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

    def dobi_ind_inflacije_drzave(self, id_drzave)-> List[inflacija]: 
        self.cur.execute("""
            SELECT leto, id_drzave, indeks_inflacije
            FROM inflacija
            WHERE id_drzave=%s
        """, (id_drzave,))
        infl = [inflacija.from_dict(t) for t in self.cur.fetchall()]
        return infl

    def dobi_inflacijo(self, leto, id_drzave) -> inflacija: 
        self.cur.execute("""
            SELECT leto, id_drzave, indeks_inflacije
            FROM inflacija
            WHERE id_drzave=%s
            AND leto=%s
        """, (id_drzave, leto))
        infl =inflacija.from_dict(self.cur.fetchone()) 
        return infl

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
    
    def dobi_cene_dto(self) -> List[gibanje_cenDto]: 
        self.cur.execute("""
            SELECT g.leto AS leto, g.id_izdelka AS id_izdelka, i.ime AS ime_izdelka , k.ime AS ime_skupine, k.sifra AS sifra_skupine, g.cena AS cena 
            FROM gibanje_cen g
            JOIN izdelki i ON g.id_izdelka = i.id
            JOIN klasifikacija k ON i.id_skupine = k.id
        """)
        cene = [gibanje_cenDto.from_dict(t) for t in self.cur.fetchall()]
        return cene

    def dobi_ceno_izdelkov_skupine(self, id_skupine, leto) -> List[cenaizdelkaDto]:
        #vrne povprecno ceno izdelkov za določeno leto, ki pripadajo izbrani skupini
        self.cur.execute("""
            SELECT g.leto AS leto, i.ime AS ime_izdelka , g.cena AS cena 
            FROM gibanje_cen g
            JOIN izdelki i ON g.id_izdelka = i.id
            WHERE i.id_skupine=%s
            AND g.leto = %s
        """, (id_skupine, leto))

        infl = [cenaizdelkaDto.from_dict(t) for t in self.cur.fetchall()]
        return infl

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

    
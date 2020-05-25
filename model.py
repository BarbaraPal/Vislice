import random

import json

STEVILO_DOVOLJENIH_NAPAK = 10

ZACETEK = 'Z'

# Konstante za rezultate ugibanj
PRAVILNA_CRKA = '+' 
PONOVLJENA_CRKA = 'o'
NAPACNA_CRKA = '-'

# Konstante za zmago in poraz
ZMAGA = 'W'
PORAZ = 'X'

bazen_besed = []
with open('besede.txt', encoding='utf-8') as datoteka_bazena:
    for beseda in datoteka_bazena:
        bazen_besed.append(beseda.strip().lower())

def nova_igra():
    nakljucna_beseda = random.choice(bazen_besed)
    return Igra(nakljucna_beseda)

class Igra:
    def __init__(self, geslo, crke=None):
        self.geslo = geslo.lower()
        if crke is None:
            self.crke = []
        else:
            self.crke = crke.lower()

    def napacne_crke(self):
        return [c for c in self.crke if c not in self.geslo]

    def pravilne_crke(self):
        return [c for c in self.crke if c in self.geslo]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK
    
    def zmaga(self):
        # ali z "return all(c in self.crke for c in self.geslo)"
        for c in self.geslo:
            if c not in self.crke:
                return False
        return True

    def pravilni_del_gesla(self):
        trenutno = ''
        for crka in self.geslo:
            if crka in self.crke:
                trenutno += crka
            else:
                trenutno += '_'
        return trenutno

    def nepravilni_ugibi(self):
        return ' '.join(self.napacne_crke())

    def ugibaj(self, ugibana_crka):
        ugibana_crka = ugibana_crka.lower()

        if ugibana_crka in self.crke:
            return PONOVLJENA_CRKA
        
        self.crke.append(ugibana_crka)

        if ugibana_crka in self.geslo:
            if self.zmaga():
                return ZMAGA
            else:
                return PRAVILNA_CRKA
        
        if ugibana_crka not in self.geslo:
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA

class Vislice:
    """
    Skrbi za trenutno stanje več iger (imel bo več objektov tipa Igra)
    """
    def __init__(self):
        # Slovar, ki ID-ju priredi objekt njegove igre
        self.igre = {}  # int -> (Igra, stanje)

    def prosti_ID_igre(self):
        """Vrne nek id, ki ga ne uporablja nobena igra"""

        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1
    
    def nova_igra(self):
        self.preberi_iz_datoteke()
        nov_id = self.prosti_ID_igre()
        sveza_igra = nova_igra()
        self.igre[nov_id] = (sveza_igra, ZACETEK)
        self.shrani_v_datoteko()
        return nov_id

    def ugibaj(self, id_igre, crka):
        self.preberi_iz_datoteke()
        trenutna_igra,_ = self.igre[id_igre]
        novo_stanje = trenutna_igra.ugibaj(crka)
        self.igre[id_igre] = (trenutna_igra, novo_stanje)
        self.shrani_v_datoteko()

    def shrani_v_datoteko(self):
        {id_igre : ((geslo, ugibane_crke), novo_stanje)}

        igre = {}

        for id_igre, (igra, stanje) in self.igre.items:
            igre[id_igre] = ((igra.geslo, igra.crke), stanje)

        # zapisano drugače
        # for id_igre, igra in self.igre.items:
        #    igre[id_igre] = ((igra[0].geslo, igra[0].crke), igra[1])

        with open("stanje_iger.json", "w") as out_file:
            json.dump(igre, out_file)

    def preberi_iz_datoteke(self):
        with open("stanje_iger.json", "r") as in_file:
            igre = json.load(in_file)

        self.igre = {}

        for id_igre ,((geslo, crke), stanje) in igre.items():
            (geslo, crke), stanje = igre[id_igre]
            self.igre[int(id_igre)] = Igra(geslo, crke), stanje
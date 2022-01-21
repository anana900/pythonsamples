'''
Created on Jan 13, 2022

@author: anana
'''

from functools import wraps

# ---------- funkcja jako dekorator ---------- 
def dekorator_pomiar_czasu(f):
    try:
        from time import time
    except ImportError:
        pass
    
    @wraps(f)
    def f_dekor(*args, **kwargs):
        t_start = time()
        f(*args, **kwargs)
        print("Execution time {} [s]".format(time()-t_start))
    
    return f_dekor

def dekorator_ramka(f):
    dlugosc = 60
    
    @wraps(f)
    def f_dekor(*args, **kwargs):
        print("-"*dlugosc)
        f(*args, **kwargs)
        print("-"*dlugosc)
    
    return f_dekor

def dekorator_multiplikator_parametr(ile=2):
    def f_dekor_main(f):
        
        @wraps(f)
        def f_dekor(*args, **kwargs):
            for _ in range(ile):
                f(*args, **kwargs)

        return f_dekor
    return f_dekor_main

@dekorator_multiplikator_parametr()
@dekorator_pomiar_czasu
@dekorator_ramka                                # sposób użycia dekoratora rekomendowany
def funkcja_powitanie(imie, nazwisko, zarobki):
    print("Witaj {} {}, widzę że zarabiasz {}".format(imie, nazwisko, zarobki))

# ---------- dekorator klasy ---------- 
def kolorowanie(kolor):
    def k_dekor_main(klasa):
        class k_dekor(object):
            def __init__(self, *args, **kwargs):
                self.k_dekor = klasa(*args)
                self.k_dekor.kolor = kolor
            def __getattr__(self, atrybut):
                print("Kolor {}".format(self.k_dekor.kolor))
                return getattr(self.k_dekor, atrybut)
            def nowa_metoda_od_dekoratora(self):
                print("Jestem metodą zaimplementowaną przez dekorator")
        return k_dekor
    return k_dekor_main

@kolorowanie(kolor=22)
class Dom:
    def __init__(self, typ):
        self.typ = typ
    def pokaz_dom(self):
        print("Pokazuję dom typu {}".format(self.typ))
    def usun_dom(self):
        print("Usunieto")

# ---------- klasa jako dekorator ---------- 
class dekorator_bez_parametru(object):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, *args, **kwargs):
        print("Dekorujemy funkcje z klasy")
        self.f(*args, **kwargs)

class dekorator_z_parametrem(object):
    def __init__(self, powtorzenia):
        self.powtorzenia = powtorzenia
    
    def __call__(self, f):
        @wraps(f)
        def f_wrapper(*args, **kwargs):
            for _ in range(self.powtorzenia):
                f(*args, **kwargs)
        return f_wrapper

@dekorator_bez_parametru
@dekorator_z_parametrem(powtorzenia=3)
def powitanie(ktoto='as'):
    print(f'Jestem {ktoto}')

class dekorator_serwowanie_danych(object):
    def __init__(self, *dane):
        self.d = dane
    
    def __call__(self, f):
        @wraps(f)
        def f_wrapper():
            for dana in self.d:
                f(dana)
        return f_wrapper

@dekorator_serwowanie_danych("Ala", "Ela", "Ola", 1212)
def witamwas(ktoto='as'):
    print(f'Jestem {ktoto}')

if __name__ == '__main__':
    # ---------- dekorator funkcji jako funkcja ---------- 
    funkcja_powitanie('a', 'b', 2855)
    print(funkcja_powitanie.__name__)
    
    # ---------- dekorator klasy jako funkcja ---------- 
    d1 = Dom(1)
    d1.pokaz_dom()
    d1.nowa_metoda_od_dekoratora()
    
    # ---------- dekorator funkcji jako klasa ---------- 
    powitanie()
    witamwas()


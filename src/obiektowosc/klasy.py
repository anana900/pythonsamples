# -- coding: utf8

# dziedziczenie
class Budynek(object):
    __zmienna_klasy_budynek = 100 # zmienna klasy, modyfikowana z poziomu klasy, wspólna dla instancji
    def __init__(self, powierzchnia = 1, ilosc_pieter = 11):
        self.powierzchnia = powierzchnia # zmienna instancji, tylko dla instancji
        self.ilosc_pieter = ilosc_pieter

class Okno(object):
    __zmienna_klasy_okno = 200
    def __init__(self, szerokosc = 2, wysokosc = 22, typ = 'typ_1'):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.__typ = typ
    
class Stodola(Budynek, Okno):
    def __init__(self, przeznaczenie = 'ogolne'):
        Okno.__init__(self)
        Budynek.__init__(self)
        self.przeznaczenie = przeznaczenie
    
    def mowa(self, dana, *dane, **superdane):
        print("dana {}".format(dana))
        for dana in dane:
            print("dane {}".format(dana))
        for nazwa, dana in superdane.items():
            print("superdane {} {}".format(nazwa, dana))
        #print("reszta z superdana {}".format(dana))

# polimorfizm
# ta sama nazwa funkcji moze mieć wiele implementacji
class Osa(object):
    def __init__(self, nazwa):
        self.nazwa = nazwa
    def czesc(self):
        print("Bz z z z z z zła osa {}".format(self.nazwa)) 

class Pszczola(object):
    def __init__(self, nazwa):
        self.nazwa = nazwa
    def czesc(self):
        print("Bzzzzzzzzz jestem pszczolka {}".format(self.nazwa)) 

def obsluga_czesc(obj_owad):
    obj_owad.czesc()

# metoda klasy, metoda instancji, metoda statyczna
# metoda instancji - bez dekoratora, można wywołać tylko z poziomu instancji
# metoda klasy - @classmethod, cls, wywołanie na rzecz całej klasy
# metoda statyczna - @staticmethod, jak zwykła funkcja, ale widoczna w zakresie Klasy
class Person(object):
    __ile_instancji = 0
    def __init__(self):
        Person.__ile_instancji += 1

    @classmethod
    def narodziny(cls):
        return 1

    @staticmethod
    def ile_instancji():
        return Person.__ile_instancji

    def instancja(self):
        print("Metoda instancji")


# klasy abstrakcyjne
# Abstrakcja polega na tworzeniu klasy bazowej która:
# - posiada metodę abstrakcyjną – taką która ma tylko nazwę bez implementacji. Dopiero w klasach dziedziczących implementujemy tą metodę.
# - dzięki metodzie abstrakcyjnej nie można stworzyć obiektu z klasy bazowej
# - klasa bazowa musi dziedziczyć po specjalnej klasie ABC
# - klasa abstrakcyjna posiada zarówno metody implementujące funkcjonalności jak metody abstrakcyjne.
from abc import ABC, abstractmethod
class Planeta(ABC):
    def __init__(self, masa, wiek):
        self.masa = masa
        self.wiek = wiek
    
    @abstractmethod
    def jak_wiruje(self):
        pass
    
    def _parametry(self):
        print("wiek {} masa {}".format(self.wiek, self.masa))

class Mars(Planeta):
    def jak_wiruje(self):
        print("Wiruje dość wolno")


# hermetyzacja, property - getters, setters
# - dostęp do zmiennych prywatnych poprzez metody
# - pozwala dodawać funkcjonalność do ustawiania i pobierania danych
class Kosmetyk(object):
    def __init__(self, cena):
        self.cena = cena
        
    @property
    def cena(self):
        print("Pobieranie ")
        return self.__cena
    
    @cena.setter
    def cena(self, val):
        print("Ustawianie ")
        if all(typ != type(val) for typ in [int, float]):
            print("Nieprawidłowy typ danych ", type(val))
            self.__cena = 0
        elif val < 0:
            self.__cena = 0
        else:
            self.__cena = val

if __name__ == '__main__':
    print("dziedziczenie".center(100, "-"))
    s1 = Stodola()
    print(s1.powierzchnia, s1.ilosc_pieter, s1.szerokosc, s1.wysokosc)
    
    #innedane=[11,22,33,44]
    #s1.mowa(1, *innedane, g=1, ala=33, sebastian=0)
    #print(s1.__getattribute__("szerokosc"))
    #print(getattr(s1, "szerokosc"))
    
    # polimorfizm
    print("polimorfizm".center(100, "-"))
    osa = Osa("Ala")
    pszczola = Pszczola("Maja")
    obsluga_czesc(osa)
    obsluga_czesc(pszczola)
    
    # classmethod staticmethod
    print("classmethod staticmethod".center(100, "-"))
    ala = Person()
    ola = Person.narodziny()
    print("Instancje ", Person().ile_instancji())

    # klasy abstrakcyjne
    print("Klasy abstrakcyjne".center(100, "-"))
    plm = Mars(12312, 2332)
    plm.jak_wiruje()
    plm._parametry()
    
    # hermetyzacja, property - getters, setters
    print("hermetyzacja, property - getters, setters".center(100, "-"))
    kosm = Kosmetyk(122)
    kosm.cena
    print(kosm.__dict__)
    
    

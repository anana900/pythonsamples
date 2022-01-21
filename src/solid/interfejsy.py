'''
Created on Jan 17, 2022

@author: anana
'''
from abc import ABC, abstractmethod

class IBaza(ABC):
    @abstractmethod
    def polaczDB(self):
        pass
    
    @abstractmethod
    def rozlaczDB(self):
        pass
    
class BazaMySql(IBaza):
    def polaczDB(self):
        print("Połaczenie z baza MySql")
    
    def rozlaczDB(self):
        print("Rozłączenie z baza MySql")

class BazaPSQL(IBaza):
    def polaczDB(self):
        print("Połaczenie z baza PSQL")
    
    def rozlaczDB(self):
        print("Rozłączenie z baza PSQL")

if __name__ == '__main__':
    nazwabazy = input("Dozwolone opcje: BazaMySql, BazaPSQL")
    klasa = globals()[nazwabazy] if nazwabazy in globals() else print(f"Nie ma takiego obiektu: {nazwabazy}")
    instancja_klasy = klasa()
    instancja_klasy.polaczDB()
    instancja_klasy.rozlaczDB()

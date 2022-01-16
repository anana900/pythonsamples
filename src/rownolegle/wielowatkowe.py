from threading import (
    Thread, 
    Lock, 
    Semaphore
)

from queue import Queue
from time import sleep
from random import randint
from time import time
from src.przeszukiwanie_strony import znajdz_stolice

# ------------------------------------------------------------------
# Thread
# Bez Join
# ------------------------------------------------------------------
def f_print_stdo(kto, ile_liczb):
    for element in range(ile_liczb):
        sleep(1.0/randint(10000, 1000000))
        print("{0}:{1}".format(kto, element))

def watek_wywolanie_bez_czekania_na_watek_glowny(iteracje=10):
    watek_1 = Thread(target=f_print_stdo,args=("w1a",iteracje,))
    watek_2 = Thread(target=f_print_stdo,args=("w2a",iteracje,))
    
    watek_1.start()
    watek_2.start()
    
    print("Watek głowny, koniec")

# ------------------------------------------------------------------
# Thread
# Join
# ------------------------------------------------------------------
def watek_wywolanie_z_czekaniem_na_watek_glowny(iteracje=10):
    watek_1 = Thread(target=f_print_stdo,args=("w1b",iteracje,))
    watek_2 = Thread(target=f_print_stdo,args=("w2b",iteracje,))

    watek_1.start()
    watek_2.start()
    watek_1.join()
    watek_2.join()    
    print("Watek głowny, koniec")

# ------------------------------------------------------------------
# Thread
# Lock
# ------------------------------------------------------------------
def f_print_stdo_lock(kto, ile_liczb, blokowanie):
    for element in range(ile_liczb):
        with blokowanie:
            sleep(1.0/randint(10000, 1000000))
            print("{0}:{1}".format(kto, element))

def watek_wywolanie_z_blokada(iteracje=10):
    blokada = Lock()
    watki = [Thread(target=f_print_stdo_lock, args=("w{}b".format(w), iteracje, blokada)) for w in range(2)]
    for w in watki:
        w.start()

# ------------------------------------------------------------------
# Thread
# Lock
# ------------------------------------------------------------------
def szukaj_stolic(blokada, panstwo):
    '''
    with lock
    '''
    stolica = znajdz_stolice([panstwo])
    with blokada:
        print(stolica)
        
def szukaj_stolic2(blokada, panstwo):
    '''
    lock.acquire(), lock.release()
    '''
    stolica = znajdz_stolice([panstwo])
    blokada.acquire()
    print(stolica)
    blokada.release()

def watek_blokada_wydajnosc_przeszukiwanie_strony(panstwa):
    '''
    Użycie blokady dla wyjścia STDIO sprawia że wyniki wyświetlane są prawidłowo,
    mimo że wiele wątków jednocześnie wyszukuje stolic dla kolejnych państw.
    '''
    blokada = Lock()
    czas_rozpoczecia = time()
    watki = [Thread(target=szukaj_stolic2, args=(blokada, p)) for p in panstwa]
    [w.start() for w in watki]
    [w.join() for w in watki]
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))

# ------------------------------------------------------------------
# Thread
# Lock, Semaphore
# ------------------------------------------------------------------
def szukaj_stolic3(blokada, semafor, panstwo):
    with semafor:
        stolica = znajdz_stolice([panstwo])
    with blokada:
        print(stolica)

def watek_semafor_blokada_przeszukiwanie_strony(panstwa):
    '''
    Semafor ogranicza nam maksymalną ilość wątków do 4 które mogą wywoływać
    funkcję wyszukującą stolice państw. W chwili gdu watek kończy prace, 
    wartość semafora jest zmniejszana i kolejny wątek może wystarować pracę.
    '''
    blokada = Lock()
    semafor = Semaphore(4)
    czas_rozpoczecia = time()
    watki = [Thread(target=szukaj_stolic3, args=(blokada, semafor, p)) for p in panstwa]
    [w.start() for w in watki]
    [w.join() for w in watki]
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))

# ------------------------------------------------------------------
# Thread
# Queue, Lock
# ------------------------------------------------------------------
def szukaj_stolic4(blokada_stdo, blokada_kolejki, kolejka):
    status_pracy = True                                 # bool do trzymania statusu kolejki
    while status_pracy:
        with blokada_kolejki:                           # blokujemy kolejkę na czas dostępu do niej
            if kolejka.empty():                         
                status_pracy = False
                break
            else:
                panstwo = kolejka.get()

        stolica = znajdz_stolice([panstwo])             # przeszukiwanie
        with blokada_stdo:                              # zabezpieczamy stdo na czas wyswietlania
            print(stolica)

def watek_kolejka_blokada_przeszukiwanie_strony(panstwa):
    '''
    Tworzymy kolejkę do której wkładamy elementy do przeprocesowania
    Tworzymy lock na wyswietlanie danych STDO
    Tworzymy lock na dostep do kolejki
    Określamy maksymalną ilość wątków roboczych
    '''
    q = Queue()
    [q.put(p) for p in panstwa]
    
    blokada_kolejki = Lock()
    blokada_stdo = Lock()
    no_watki_robocze = 10
    
    czas_rozpoczecia = time()
    watki = [Thread(target=szukaj_stolic4, args=(blokada_stdo, blokada_kolejki, q)) for p in range(no_watki_robocze)]
    [w.start() for w in watki]
    
    #watek_losowe_napelnianie_kolejki(q, panstwa)
    [w.join() for w in watki]
   
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))

def watek_losowe_napelnianie_kolejki(kolejka, panstwa):
    while True:
        sleep(10.0/randint(1000, 10000))
        kolejka.put(panstwa[randint(0,len(panstwa)-1)])

# ------------------------------------------------------------------
# Thread
# Lock w Klasie
# ------------------------------------------------------------------
class SzukajStolic(object):
    def __init__(self):
        self.blokada = Lock()
    
    def cls_znajdz_stolice(self, panstwo):
        szukaj_stolic(self.blokada, panstwo)

class SzukajStolicSemaphore(object):
    def __init__(self, sno):
        self.blokada = Lock()
        self.semafor = Semaphore(sno)
    
    def cls_znajdz_stolice(self, panstwo):
        szukaj_stolic3(self.blokada, self.semafor, panstwo)
        
def watek_klasa_blokada_przeszukiwanie_strony(panstwa):
    #szukaj_stolic_1 = SzukajStolic()
    szukaj_stolic_1 = SzukajStolicSemaphore(2)
    
    czas_rozpoczecia = time()
    watki = [Thread(target=szukaj_stolic_1.cls_znajdz_stolice, args=(p,)) for p in panstwa]
    [w.start() for w in watki]
    [w.join() for w in watki]
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))

class SzukajStolicKolejka(object):
    def __init__(self, kolejka):
        self.blokada_stdo = Lock()
        self.blokada_kolejki = Lock()
        self.kolejka = kolejka
    
    def cls_znajdz_stolice(self):
        szukaj_stolic4(self.blokada_stdo, self.blokada_kolejki, self.kolejka)

def watek_klasa_kolejka_blokada_przeszukiwanie_strony(panstwa):
    q = Queue()
    szukaj_stolic_1 = SzukajStolicKolejka(q)
    [q.put(p) for p in panstwa]
    no_watki_robocze = 6
    
    czas_rozpoczecia = time()
    watki = [Thread(target=szukaj_stolic_1.cls_znajdz_stolice) for _ in range(no_watki_robocze)]
    [w.start() for w in watki]
    [w.join() for w in watki]
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))


if __name__ == '__main__':
    #watek_wywolanie_bez_czekania_na_watek_glowny(5)
    #watek_wywolanie_z_czekaniem_na_watek_glowny(4)
    #watek_wywolanie_z_blokada(10)
    
    panstwa = ['Poland', 'Germany', 'Sweden', 'Ukraine', 'Belorus', 'Russia', 'Austria', 'France']
    #watek_blokada_wydajnosc_przeszukiwanie_strony(panstwa)
    #watek_semafor_blokada_przeszukiwanie_strony(panstwa)
    #watek_kolejka_blokada_przeszukiwanie_strony(panstwa)
    #watek_klasa_blokada_przeszukiwanie_strony(panstwa)
    #watek_klasa_kolejka_blokada_przeszukiwanie_strony(panstwa)


'''
    class iiter():
        def __init__(self, n):
            self.n = n
            self.i = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.n == self.i:
                raise StopIteration
            self.i += 1
            return self.i
    
    class sumiter(iiter):
        def __init__(self, n):
            super().__init__(n)
            self.current = 0
            
        def __iter__(self):
            return iiter.__iter__(self)

        def __next__(self):
            if self.n == self.i:
                raise StopIteration
            self.i += 1
            self.current += self.i
            return self.current            
    
    print([e for e in iiter(4)])
    print([e for e in sumiter(4)])
'''

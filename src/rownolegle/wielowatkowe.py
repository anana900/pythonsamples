"""
Wątek w Python jest instancją klasy threading.Thread. Po wystartowaniu wątku interpreter Python komunikuje się z
systemem w celu stworzenia natywnego wątka. Thread następnie udostepnia referencje do tego natywego wątku.

Cykl życia wątku:
1. nowy wątek - powstaje poprzez stworzenie instancji klasy Thread.
2. działający wątek - powstaje po wywołaniu metody start(). Działający wątek może być w stanie zablokowanym, a
następnie powrócić do stanu działający.
3. zakończony wątek - ten stan następuje po wykonaniu funkcji w watku lub poprzez zwrócenie błędu lub wyjątku.
Zakończonego wątku nie można zrestartować.

Wystartowanie wątku funkcją start() wykonuje go natychmiastowo. Główny wątek niejawnie czeka na zakończenie pobocznego.
Wywołanie dodatkowej funkcji join() sprawia że wywołanie wątku będzie w najbliższym dostępnym czasie procesora.
Główny wątek jawnie czekka na zakończenie wykonywania wątku pobocznego.

GIL - Global Interpreter Lock - mechanizm który sprawia ze w CPythonie w danym momencie czasowym dostęp do obiektów
Pythona ma tylko jeden wątek. Inaczej to oznacza że tak naprawdę kod nie wykonuje się równolegle. Sąoperacje które
moga być wykonywane w sposób równoległy (zwolnione sa o restrykcji GIL): operacji I/O np print, operacje na pliku,
operacje na Numpy, przetwarzanie obrazów, wykonujac C kod i jawnie zwalniając blokadę.
start() - uruchamia wątek (wątek przechodzi ze stanu nowy -> działający)
join() - sprawia że wątek główny jawnie czeka na zakończenie wątu pobocznego.
Lock() - tworzy obiekt lock który możeby wykozystywać do bezpiecznego dostępu do zasobów

"""
from threading import (
    Thread, 
    Lock, 
    Semaphore,
    current_thread,
    enumerate
)

from queue import Queue
from time import sleep
from random import randint
from time import time
from src.web.przeszukiwanie_strony import znajdz_stolice
from src.dekoratory.dekoratory import dekorator_pomiar_czasu

# ------------------------------------------------------------------
# Thread
# Bez Join. Wykonuję wątki poboczne natychmiastowo, a wątek główny nie czeka na wątki poboczne.
# ------------------------------------------------------------------
def f_print_stdo(nazwa_watku, ile_liczb):
    for element in range(ile_liczb):
        sleep(1.0/randint(10000, 1000000))
        print("{0}:{1}".format(nazwa_watku, element))

@dekorator_pomiar_czasu
def watek_wywolanie_bez_czekania_na_watek_glowny(iteracje=10):
    watek_1 = Thread(target=f_print_stdo, args=("w1a", iteracje,))
    watek_2 = Thread(target=f_print_stdo, args=("w2a", iteracje,))
    watek_1.start()
    watek_2.start()
    print("Watek głowny, kontynuacja nie czekając na zakonczenie wątków pobocznych.")

# ------------------------------------------------------------------
# Thread
# Join - wywołanie wątku w najbliższym dostępnym czasie procesora. Wątek główny czeka na zakończenie pobocznych.
# ------------------------------------------------------------------
@dekorator_pomiar_czasu
def watek_wywolanie_z_czekaniem_na_watek_glowny(iteracje=10):
    watek_1 = Thread(target=f_print_stdo,args=("w1b",iteracje,))
    watek_2 = Thread(target=f_print_stdo,args=("w2b",iteracje,))
    watek_1.start()
    watek_2.start()
    watek_1.join()
    watek_2.join()    
    print("Watek głowny, czekam na wykonanie wątków pobocznych dopiero kontynułuję wątek główny.")

# ------------------------------------------------------------------
# Thread
# Lock - pozwala synchronizować dostęp do wspólnych zasbów.
# ------------------------------------------------------------------
def f_print_stdo_lock(nazwa_watku, ile_liczb, blokowanie):
    for element in range(ile_liczb):
        with blokowanie:
            sleep(1.0/randint(10000, 1000000))
            print("{0}:{1}".format(nazwa_watku, element))

@dekorator_pomiar_czasu
def watek_wywolanie_z_blokada(iteracje=10):
    blokada = Lock()
    watki = [Thread(target=f_print_stdo_lock, args=("w{}b".format(w), iteracje, blokada)) for w in range(2)]
    for w in watki:
        w.start()

# ------------------------------------------------------------------
# Thread + Lock - przyklad z wyszukiwaniem panstw
# ------------------------------------------------------------------
def szukaj_stolic(blokada, panstwo):
    # with lock
    stolica = znajdz_stolice([panstwo])
    with blokada:
        print(stolica)
        
def szukaj_stolic2(blokada, panstwo):
    # lock.acquire(), lock.release()
    stolica = znajdz_stolice([panstwo])
    blokada.acquire()
    print(stolica)
    blokada.release()

@dekorator_pomiar_czasu
def watek_blokada_wydajnosc_przeszukiwanie_strony(panstwa):
    '''
    Użycie blokady dla wyjścia STDIO sprawia że wyniki wyświetlane są prawidłowo,
    mimo że wiele wątków jednocześnie wyszukuje stolic dla kolejnych państw.
    '''
    blokada = Lock()
    watki = [Thread(target=szukaj_stolic2, args=(blokada, p)) for p in panstwa]
    [w.start() for w in watki]
    [w.join() for w in watki]

# ------------------------------------------------------------------
# Thread
# Lock, Semaphore
# ------------------------------------------------------------------
def szukaj_stolic3(blokada, semafor, panstwo):
    with semafor:
        stolica = znajdz_stolice([panstwo])
    with blokada:
        print(stolica)

@dekorator_pomiar_czasu
def watek_semafor_blokada_przeszukiwanie_strony(panstwa):
    '''
    Semafor ogranicza nam maksymalną ilość wątków do 4 które mogą wywoływać
    funkcję wyszukującą stolice państw. W chwili gdu watek kończy prace, 
    wartość semafora jest zmniejszana i kolejny wątek może wystarować pracę.
    '''
    blokada = Lock()
    semafor = Semaphore(4)
    watki = [Thread(target=szukaj_stolic3, args=(blokada, semafor, p)) for p in panstwa]
    [w.start() for w in watki]
    [w.join() for w in watki]

# ------------------------------------------------------------------
# Thread
# Queue, Lock
# ------------------------------------------------------------------
def szukaj_stolic4(blokada_stdo, blokada_kolejki, kolejka):
    status_pracy = True                                 # bool do trzymania statusu kolejki
    while status_pracy:
        with blokada_kolejki:                           # blokujemy kolejkę na czas dostępu do niej
            if kolejka.empty():                         
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

@dekorator_pomiar_czasu
def watek_klasa_blokada_przeszukiwanie_strony(panstwa):
    #szukaj_stolic_1 = SzukajStolic()
    szukaj_stolic_1 = SzukajStolicSemaphore(2)
    
    watki = [Thread(target=szukaj_stolic_1.cls_znajdz_stolice, args=(p,)) for p in panstwa]
    [w.start() for w in watki]
    [w.join() for w in watki]

# ------------------------------------------------------------------
# Thread
# Queue, Lock w Klasie
# ------------------------------------------------------------------
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
    no_watki_robocze = 8
    
    czas_rozpoczecia = time()
    watki = [Thread(target=szukaj_stolic_1.cls_znajdz_stolice) for _ in range(no_watki_robocze)]
    [w.start() for w in watki]
    [w.join() for w in watki]
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))

# ------------------------------------------------------------------
# Thread
# Lock w Klasie dziedziczącej po Thread
# Nie można nadpisywać żadnych innych metod orócz __init__ oraz run.
# ------------------------------------------------------------------
class KlasaThreadLock(Thread):
    def __init__(self, panstwo):
        super().__init__()
        self.panstwo = panstwo
        self.blokada = Lock()
    
    def run(self):
        szukaj_stolic(self.blokada, self.panstwo)
        print(f"Wykonał wątek: {current_thread().ident}")

@dekorator_pomiar_czasu
def watek_klasa_thread_blokada_przeszukiwanie_strony(panstwa):
    lista_watkow = []
    
    for panstwo in panstwa:
        lista_watkow.append(KlasaThreadLock(panstwo))
        
    [w.start() for w in lista_watkow]
    print(f'Lista aktywnych wątków: {enumerate()}')
    [w.join() for w in lista_watkow]

"""
GIL
"""
def gil_io() -> None:
    pass

if __name__ == '__main__':
    panstwa_europa_full = (
        "Russia", "Germany", "United Kingdom", "France",
        "Italy", "Spain", "Ukraine", "Poland",
        "Romania", "Netherlands", "Belgium", "Czech Republic (Czechia)",
        "Greece", "Portugal", "Sweden", "Hungary",
        "Belarus", "Austria", "Serbia", "Switzerland",
        "Bulgaria", "Denmark", "Finland", "Slovakia",
        "Norway", "Ireland", "Croatia", "Moldova",
        "Bosnia and Herzegovina", "Albania", "Lithuania", "North Macedonia",
        "Slovenia", "Latvia", "Estonia", "Montenegro",
        "Luxembourg", "Malta", "Iceland", "Andorra",
        "Monaco", "Liechtenstein", "San Marino", "Holy See"
        )
    # watek_wywolanie_bez_czekania_na_watek_glowny(5)
    # watek_wywolanie_z_czekaniem_na_watek_glowny(4)
    # watek_wywolanie_z_blokada(10)
    # watek_blokada_wydajnosc_przeszukiwanie_strony(panstwa_europa_full[:8])
    watek_semafor_blokada_przeszukiwanie_strony(panstwa_europa_full[:8])
    # watek_kolejka_blokada_przeszukiwanie_strony(panstwa_europa_full[:8])
    # watek_klasa_blokada_przeszukiwanie_strony(panstwa_europa_full[:8])
    # watek_klasa_kolejka_blokada_przeszukiwanie_strony(panstwa_europa_full[:8])
    # watek_klasa_thread_blokada_przeszukiwanie_strony(panstwa_europa_full[:8])

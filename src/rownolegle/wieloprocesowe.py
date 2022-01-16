'''
Created on Jul 30, 2020

@author: anana
'''
import multiprocessing as mp
from click._compat import raw_input
import time

def oczko(name):
    print("Jestem procesem innym name:{} pid:{} process name:{}"\
          .format(name, mp.current_process().pid, mp.current_process().name))

def proces():
    print("Jestem procesem main {}".format(mp.current_process().pid))

    p1 = mp.Process(target=oczko, args=(1,))
    p2 = mp.Process(target=oczko, args=(2,))
    p1.start()
    p2.start()

def pula():
    l = ["ola", "asia", "klaudia", "viena"]
    ilosc_procesow = len(l)

    p = mp.Pool(ilosc_procesow)
    p.map(oczko, l)

def proces_anonimowy():
    imie = raw_input("Jak masz na imie?")
    ile_procesow = int(input("Ile procesow uruchomic"))

    for _ in range(ile_procesow):
        (mp.Process(target=oczko, args=(imie,))).start()

def proces_anonimowy_z_nawa():
    imie = raw_input("Jak masz na imie?")
    ile_procesow = int(input("Ile procesow uruchomic"))

    for name in range(ile_procesow):
        (mp.Process(target=oczko, args=(imie,), name = str(name))).start()

def oczko_lock(lock, shm_data):
    while shm_data.value < 100:
        lock.acquire()
        shm_data.value += 1
        lock.release()
        print("process {} {} {}".format(mp.current_process().name, mp.current_process().pid, shm_data.value))
        time.sleep(0.0001)

def proces_lock():
    lock = mp.Lock()
    shm_data = mp.Value('i', 10)    
    ile_procesow = int(input("Ile procesow uruchomic"))

    processes = []
    for name in range(ile_procesow):
        processes.append(mp.Process(target=oczko_lock, args=(lock, shm_data), name = str(name)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print(shm_data.value)

def oczko_kolejka(q):
    while True:
        data = q.get()
        if data:
            print("Hi {} {} {}".format(data, mp.current_process().name, mp.current_process().pid)) 

def proces_kolejka():
    q = mp.Queue()
    processes = []

    for _ in range(4):
        processes.append(mp.Process(target=oczko_kolejka,args=(q,)))

    for p in processes:
        p.start()

    counter = 0
    while True:
        time.sleep(0.01)
        counter += 1
        if counter < 33:
            q.put(counter)
        else:
            for p in processes:
                if p.is_alive():
                    p.terminate()
            break

    print("main koniec")

def modulo(ds,de,q):
    wynik = []
    for d in range(ds,de):
        if d%13 == 0:
            wynik.append(d)
    print("proces {} zakonczony".format(mp.current_process().pid))
    q.put(wynik)

def proces_kolejka_podzial():
    q = mp.Queue()

    liczba = int(input("Jaka liczbe procesowac?"))
    p_number = int(input("Ile procesow uzyc?"))
    d_przedzial = liczba//p_number
    d_start = 0
    procesy = []
    for p in range(p_number):
        procesy.append(mp.Process(target=modulo, args=(d_start, d_przedzial,q)))
        d_start = d_przedzial
        d_przedzial += d_przedzial
    
    for p in procesy:
        p.start()
        print("Startujemy proces")

    wynik = []
    for _ in procesy:
        w = q.get()
        wynik += w
    print(wynik)

def praca_na_liscie_akcja(ls, zakres):
    for item in range(1,zakres):
        ls.append(item)

def praca_na_liscie():
    ls = []
    praca_na_liscie_akcja(ls, 10)
    praca_na_liscie_akcja(ls, 10)
    print(ls)

def proc_praca_na_liscie():
    ls = []
    mp1 = mp.Process(target=praca_na_liscie_akcja, args=(ls,10))
    mp2 = mp.Process(target=praca_na_liscie_akcja, args=(ls,10))
    mp1.start()
    mp2.start()
    mp1.join()
    mp2.join()
    print(ls)

# proc_praca_na_liscie nie dziala bo lista nie jest widoczna przez procesy dzieci
# rozwiazanie 1 - uzycie kolejki
def praca_na_liscie_akcja_q(kolejka, zakres):
    for item in range(1,zakres):
        kolejka.put(item)
    print("koniec")

def proc_praca_na_liscie_q():
    ls = []
    q = mp.Queue()

    mp1 = mp.Process(target=praca_na_liscie_akcja_q, args=(q,10))
    mp2 = mp.Process(target=praca_na_liscie_akcja_q, args=(q,10))
    mp1.start()
    mp2.start()

    for _ in range(1,19):
        ls.append(q.get())
    print(ls)

#-----dzialania na duzej liscie za pomoca procesow-------
def podnies_do_kwadratu(q, ls, znacznik):
    print("proces {} start".format(mp.current_process().pid))
    wynik = list(map(lambda x:x*x, ls))
    #q.put(znacznik)
    q.put(wynik)
    print("proces {} koniec".format(mp.current_process().pid))

def proces_podnies_do_kwadratu():
    dane = list(range(1,11))
    print(dane)
    lp = 2
    przedzial = len(dane)//lp
    print(przedzial)
    
    q = mp.Queue()
    wynik = []
    procesy = []
    
    for p in range(1,lp+1):
        data = range((p-1)*przedzial+1, przedzial*p+1)
        procesy.append(mp.Process(target=podnies_do_kwadratu, args=(q, data, p)))

    for p in procesy:
        p.start()

    while True:
        dana = q.get()
        wynik += dana
        
        if len(wynik) == len(dane):
            break

    print(wynik)
    
# def glowica_posow(akcja, kanal_glowica):
#     if status == "IDLE":
#         try:
#             t_start = time.time()
# 
#             if akcja == "AK_WYSUN":
#                 status = "WORKING"
#                 kanal_glowica.put(status)
#                 motor_ruch("glowica",1)
#                 while get_status_glowica_wysuniety() == False:
#                     if time.time() - t_start > TIMER_POSOW_GLOWICY:
#                         motor_ruch("glowica",-1)
#                         status = "MS_GLOWICA_TIMEOUT_1"
#                         break
#                 status = "MS_GLOWICA_WYSUNIETA"
#
#             if akcja == "AK_WSUN":
#                 status = "WORKING"
#                 kanal_glowica.put(status)
#                 motor_ruch("glowica",0)
#                 while get_status_glowica_wsuniety() == False:
#                     if time.time() - t_start > TIMER_POSOW_GLOWICY:
#                         motor_ruch("glowica",-1)
#                         status = "MS_GLOWICA_TIMEOUT_0"
#                         break
#                 status = "MS_GLOWICA_WYSUNIETA"
#
#             if akcja == "AK_SERVIS_1":
#                 pass
#         except:
#             status = "ERROR"
#             print("problem")
#         finally:
#             motor_ruch("glowica",-1)
#             kanal_glowica.put(status)
#             if status not in ["ERROR", "MS_GLOWICA_TIMEOUT_0", "MS_GLOWICA_TIMEOUT_1"]:
#                 status = "IDLE"
#     else:
#         kanal_glowica.put(status)


if __name__ == '__main__':
    #proces()
    #pula()
    #proces_anonimowy()
    #proces_anonimowy_z_nawa()
    #proces_lock()
    #proces_kolejka()
    #proces_kolejka_podzial()
    #praca_na_liscie()
    #proc_praca_na_liscie()
    #proc_praca_na_liscie_q()
    proces_podnies_do_kwadratu()

'''
Created on Jan 19, 2022

@author: anana
'''
import unittest
import os
from functools import wraps

from src.testyjednostkowe.program_system_manipulacja import get_file_list

'''
Pojęcia:
test fixtures - represent preparation needed to perform one or more tests. setUp and tearDown functions.
'''

class PrzykladyAsercji(unittest.TestCase):
    '''
    Dostępne asercje
    '''

    def setUp(self):
        print('Przed testem')

    def tearDown(self):
        print('po tescie')

    def test_asserty(self):
        self.assertAlmostEqual(1, 1.29, msg='przybliżenie poza marginesem', delta=0.3)
        self.assertCountEqual([1,2,3], [2,1,3], 'zbiory tego samego typu. liczy wystąpienia każdego elementu i porównuje')
        #self.assertDictContainsSubset({2:2}, {1:1, 2:2}, msg='podzbiór nie istnieje w zbiorze')
        self.assertDictEqual({2:2, 1:1}, {1:1, 2:2}, 'slowniki róźnią się')
        self.assertEqual('ala', 'ala', 'sprawdzenie równości')
        self.assertFalse(12==22, 'niestety sa rowne')
        self.assertTrue(12==12, 'niestety nie sa rowne')
        self.assertGreater(3, 2, 'nie jest wiekszy')
        self.assertGreaterEqual(3, 2, 'nie jest wiekszy rowny')
        self.assertIn('a', {'a':1, 'b':2}, 'element nie istnieje w zbiorze. Szuka po kluczach')
        
        with self.assertRaises(IndexError):
            _ = [1,2,3][4]
        with self.assertRaises(TypeError):
            'ala'.split(123)
        
        with self.assertRaises(AssertionError):
            self.assertRegex('test', r'^a', 'bedzie blad jesli a rozpocznie napis test')
        self.assertRegex('atest', r'^a', 'Będzie błąd jeśli litera a nie rozpoczenie napisu test')


def DodajInnyPlik(katalog: str, lista_plikow: list = []):
    '''
    1 tworzy dodatkowe pliki przed wywołaniem funkcji
    2 usuwa dodatkowe pliki po wykonaniu funkcji
    '''
    def CreateMoreFilesWrap(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # stworzenie dodatkowych plików
            for plik in lista_plikow:
                with open(katalog + '/' + plik, 'w+'):
                    pass
            # właściwa funkcja
            retVal = func(self, *args, **kwargs)
            # usunięcie dodatkowych plików
            if os.path.exists(katalog):
                for file in lista_plikow:
                    plik_do_usuniecia = katalog +'/' + file
                    if os.path.exists(plik_do_usuniecia):
                        os.remove(plik_do_usuniecia)
            return retVal
        return wrapper
    return CreateMoreFilesWrap

class TestGetFileList(unittest.TestCase):
    '''
    Testowanie funkcji get_file_list
    '''
    
    nazwa_katalogu_plikow = "testowy_katalog"
    lista_plikow = ["file_1", "file_2"]
    
    def setUp(self):
        if self.nazwa_katalogu_plikow not in os.listdir():
            os.mkdir('./' + self.nazwa_katalogu_plikow)

    def tearDown(self):
        if os.path.exists(self.nazwa_katalogu_plikow):
            for file in os.listdir(self.nazwa_katalogu_plikow):
                os.remove(self.nazwa_katalogu_plikow +'/' + file)
            os.rmdir(self.nazwa_katalogu_plikow)
    
    
    def test_pusty_katalog(self):
        self.assertEqual(get_file_list(self.nazwa_katalogu_plikow), [],
                         "Katalog niepusty")

    def test_niepusty_katalog(self):
        for file in self.lista_plikow:
            with open(self.nazwa_katalogu_plikow + '/' + file, 'w+'):
                pass
        self.assertCountEqual(get_file_list(self.nazwa_katalogu_plikow), self.lista_plikow,
                              "Listy plików są różne")

    @DodajInnyPlik(katalog=nazwa_katalogu_plikow, lista_plikow=['ela', 'olel', 'le', 'l', 'e'])
    def test_niepusty_katalog_plik_pattern(self):
        for file in self.lista_plikow:
            with open(self.nazwa_katalogu_plikow + '/' + file, 'w+'):
                pass
        self.assertCountEqual(get_file_list(self.nazwa_katalogu_plikow, plik_pattern='el'), ['ela', 'olel'],
                              "Listy plików są różne")
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #xx = RemoveTestCase()
    #print(xx.__doc__)
    unittest.main()
    
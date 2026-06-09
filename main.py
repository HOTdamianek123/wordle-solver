import pyautogui as pa
import time as tm
import random

ans = []

with open("wordle-answers.txt", "r") as f:
    ans = f.readlines()

m = len(ans)

for i in range(m):
    ans[i] = ans[i].strip()

tm.sleep(3)

aktl = []
na_pewno = [0] * 5
nie_tu = [0] * 5
beda = 0
nie_beda = 0
moze_byc = [i for i in range (m)]

zm = 68
xs = 788
ys = 340
pop = 3

def kolor(rgb_dane):
    if rgb_dane[1] > 150 and rgb_dane[1] > rgb_dane[0] + 20 and rgb_dane[1] > rgb_dane[2]:
        return 0
    if rgb_dane[0] > rgb_dane[1] > rgb_dane[2] and rgb_dane[0] > 160:
        return 1
    #teraz walka pomiedczy bialy i szary
    if min(rgb_dane) > 200:
        return 3 #bialy
    else:
        return 2 #szary

def piksel(xx, yy):
    x = xs + zm * xx
    y = ys + zm * yy
    color = pa.pixel(x, y)
    pa.moveTo(x, y)
    return kolor(color)

def sprawdz_nowa_gra():
    global na_pewno
    global nie_tu
    global beda
    global nie_beda
    global aktl
    global moze_byc
    color = pa.pixel(798, 770)
    pa.moveTo(798, 770)
    if kolor(color) == 0:
        pa.click(798, 770)
        tm.sleep(0.5)
        na_pewno = [0] * 5
        nie_tu = [0] * 5
        beda = 0
        nie_beda = 0
        aktl = []
        moze_byc = [i for i in range (m)]
        return 1
    return 0

def kol(zn):
    return 2 ** (ord(zn) - ord('a'))

def czy_git(ind): #czy dany indeks jest zgodny z obecnym stanem wiedzy
    sl = ans[ind]
    for zn in sl:
        if nie_beda&kol(zn):
            return False
        
    for i in range(ord('a'), ord('z') + 1):
        v = kol(chr(i))
        if (beda&v) and (chr(i) not in sl):
            return False
        
    for i in range(5):
        if na_pewno[i] != 0:
            jaka = chr((na_pewno[i].bit_length() - 1) + ord('a'))
            if sl[i] != jaka:
                return False
        for j in range(ord('a'), ord('z') + 1):
            zn = chr(j)
            if nie_tu[i]&kol(zn) and sl[i] == zn:
                return False
    return True

def aktualizuj():
    global moze_byc
    nowa_lista = []
    for ele in moze_byc:
        if czy_git(ele):
            nowa_lista.append(ele)
    moze_byc = nowa_lista.copy()

def wpisz(slowo): #mozemy zalozyc ze nie jest ostatnie
    global beda
    global na_pewno
    global nie_tu
    global nie_beda
    if len(slowo) != 5:
        print("zla dlugosc ktora chciales wpisac")
        exit()
    slowo = slowo.lower()
    pa.write(slowo)
    pa.press("enter")
    aktl.append(slowo)
    tm.sleep(5)
    if sprawdz_nowa_gra(): #na wypadek gdy dobrze wpiszemy
        return
    #zakaldamy ofc ze nie ma nowej gry no i sprawdzamy co i jak
    bylo = 0
    val = [0] * 5
    for j in range(5):
        val[j] = piksel(j, len(aktl) - 1)
    
    for j in range(5):
        if val[j] == 0:
            v = kol(slowo[j])
            bylo |= v
            beda |= v
            na_pewno[j] |= v

    for j in range(5):
        if val[j] == 1:
            v = kol(slowo[j])
            beda |= v
            bylo |= v
            nie_tu[j] |= v
            
    for j in range(5):
        if val[j] == 2:
            v = kol(slowo[j])
            if bylo&v:
                continue
            nie_beda |= v

    aktualizuj()

pierwsze = ["crane", "sloth", "dumpy"]

def zrob_ruch():
    #pierwsze trzy ruchy robimy by zdobyc litery
    if len(aktl) < len(pierwsze) and len(moze_byc) > 4:
        do_wpisania = pierwsze[len(aktl)]
        wpisz(do_wpisania)
        return
    ind = random.randint(0, m)
    if len(moze_byc) > 0:
        ind = random.randint(0, len(moze_byc) - 1)
    wpisz(ans[moze_byc[ind]])

while True:
    zrob_ruch()

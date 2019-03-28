#!/bin/python
# -*- coding: utf-8 -*-

import pyxel

BREITE = 200
HOEHE = 150

RAUF = 1
RUNTER = 2
LINKS = 3
RECHTS = 4

class Seite:
    def __init__(self, wie_oft, zeilen):
        self.wie_oft = wie_oft
        self.zeilen = zeilen
        self.auswahl_zeile = 0
        self.auswahl_spalte = 0
        self.auswahl = []

        self.anz_spalten = 0
        for z in range(0, len(zeilen)):
            if len(zeilen[z]) > self.anz_spalten:
                self.anz_spalten = len(zeilen[z])
        
        self.spalten_breite = BREITE / self.anz_spalten
        self.zeilen_hoehe = HOEHE / len(self.zeilen)
                
    
    def zeige_auswahl(self, zeile, spalte, farbe):
        x1 = spalte * self.spalten_breite
        x2 = (spalte + 1) * self.spalten_breite - 1
        y1 = zeile * self.zeilen_hoehe
        y2 = (zeile + 1) * self.zeilen_hoehe - 1
        
        pyxel.rectb(x1, y1, x2, y2, farbe)
        

    def zeige(self):
        '''
        print("z=%d s=%d az=%d, as=%d" % (
            len(self.zeilen), self.anz_spalten, 
            self.auswahl_zeile, self.auswahl_spalte
        ))
        '''
        
        for auswahl in self.auswahl:
            self.zeige_auswahl(auswahl["zeile"], auswahl["spalte"], 6)
        self.zeige_auswahl(self.auswahl_zeile, self.auswahl_spalte, 9)
        
        for zeile in range(0, len(self.zeilen)):
            for spalte in range(0, self.anz_spalten):
                if spalte < len(self.zeilen[zeile]):
                    text = self.zeilen[zeile][spalte]
                else:
                    text = ""
                    
                x = round(spalte * self.spalten_breite + self.spalten_breite / 3, 0)
                y = round(zeile * self.zeilen_hoehe + self.zeilen_hoehe / 3, 0)
                pyxel.text(x, y, text, pyxel.frame_count % 16)
                

    def waehle(self, taste):
        if taste == RUNTER:
            if self.auswahl_zeile < len(self.zeilen) - 1:
                self.auswahl_zeile += 1
        if taste == RAUF:
            if self.auswahl_zeile > 0:
                self.auswahl_zeile -= 1
        if taste == RECHTS:
            if self.auswahl_spalte < self.anz_spalten - 1:
                self.auswahl_spalte += 1
        if taste == LINKS:
            if self.auswahl_spalte > 0:
                self.auswahl_spalte -= 1
                
    def merke(self):
        if not self.ist_ausgewaehlt():
            self.auswahl.append({"zeile": self.auswahl_zeile, "spalte": self.auswahl_spalte})
    
    def ist_ausgewaehlt(self):
        return len(self.auswahl) >= self.wie_oft


class App:
    def __init__(self):
        
        self.welche_seite = 0
        self.seiten = []
        self.seite = None
        
        self.seiten.append(Seite(1, [
            ["Drueckmich\nTiere"]
        ]))
        self.seiten.append(Seite(1, [
            ["Zootier"], 
            ["Haustier"]
        ]))
        self.seiten.append(Seite(1, [
            ["Pflegen", "Kuscheln"],
            ["Gehege/Klo\nsaeubern", "Spaziergang"]
        ]))
        self.seiten.append(Seite(2, [
            ["1", "2", "3", "4"],
            ["Drei-\neck", "Kreis", "Qua-\ndrat", "Recht-\neck"]
        ]))

        pyxel.init(BREITE, HOEHE, caption="Drück mich")
        pyxel.run(self.update, self.draw)


    def update(self):
        
        self.seite = self.seiten[self.welche_seite]

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.seite.merke()
            if self.seite.ist_ausgewaehlt():
                if self.welche_seite < len(self.seiten) - 1:
                    self.welche_seite += 1
                else:
                    print("AUSWERTUNG")
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.seite.waehle(LINKS)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.seite.waehle(RECHTS)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.seite.waehle(RAUF)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.seite.waehle(RUNTER)

    def draw(self):
        pyxel.cls(0)
        self.seite.zeige()

App()

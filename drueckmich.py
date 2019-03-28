#!/bin/python
# -*- coding: utf-8 -*-

import pyxel

BREITE = 200
HOEHE = 150

RAUF = 1
RUNTER = 2
LINKS = 3
RECHTS = 4

LAUFEND = 1
AUSWERTUNG = 2

class Seite:
    def __init__(self, wie_oft, zeilen):
        self.wie_oft = wie_oft
        self.zeilen = zeilen

        self.anz_spalten = 0
        for z in range(0, len(zeilen)):
            if len(zeilen[z]) > self.anz_spalten:
                self.anz_spalten = len(zeilen[z])
        
        self.spalten_breite = BREITE / self.anz_spalten
        self.zeilen_hoehe = HOEHE / len(self.zeilen)
        self.reset()
    
    def reset(self):
        self.auswahl_zeile = 0
        self.auswahl_spalte = 0
        self.auswahl = []        

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
            
            # Jede Zeile darf nur einmal ausgewählt werden
            for auswahl in self.auswahl:
                if self.auswahl_zeile == auswahl["zeile"]:
                    return

            self.auswahl.append({"zeile": self.auswahl_zeile, "spalte": self.auswahl_spalte})
    
    def ist_ausgewaehlt(self):
        return len(self.auswahl) >= self.wie_oft

    def als_zahl(self):
        zahl = 0
        
        for auswahl in self.auswahl:
            zahl += ((self.anz_spalten + 1) ** auswahl["zeile"]) * (auswahl["spalte"] + 1)
        
        return zahl


class Auswertung:
    def __init__(self, seiten):
        texte = {
            
            # Zootier
            1: {
                # Dreieck
                6: "einen Strauss",
                7: "einen Flamingo",
                8: "einen Papagei",
                9: "eine Fledermaus",
                
                # Kreis
                11: "einen Fuchs",
                12: "einen Wolf",
                13: "einen Ameisenbär",
                14: "ein Erdmaennchen",
                
                # Quadrat
                16: "einen Elefant",
                17: "eine Giraffe",
                18: "ein Nashorn",
                19: "ein Nilpferd",
                
                # Rechteck
                21: "ein Stachelschwein",
                22: "eine Ziege",
                23: "ein Huhn",
                24: "einen Hahn"
            },
            # Haustier
            2: {
                # Dreieck
                6: "ein Kaninchen",
                7: "ein Meerschweinchen",
                8: "einen Hamster",
                9: "einen Fisch",
                
                # Kreis
                11: "einen Frosch",
                12: "ein Hausschwein",
                13: "eine Garnele",
                14: "ein Huhn",
                
                # Quadrat
                16: "einen Hund",
                17: "einen Katze",
                18: "einen Papagei",
                19: "einen Wellensittich",
            
                # Rechteck
                21: "einen Hahn",
                22: "eine Maus",
                23: "eine Ratte",
                24: "eine Kakerlake"
            }
        }
        
        self.seite = Seite(0, [
            [ "Du brauchst\n" + texte[seiten[1].als_zahl()][seiten[3].als_zahl()] ]
        ])
    
    def zeige(self):
        return self.seite.zeige()


class App:
    def __init__(self):
        
        self.welche_seite = 0
        self.seiten = []
        self.seite = None
        self.phase = LAUFEND
        
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
        if self.phase == AUSWERTUNG:
            self.seite = Auswertung(self.seiten)
        else:
            self.seite = self.seiten[self.welche_seite]

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            
            if self.phase == AUSWERTUNG:
                self.welche_seite = 0
                self.phase = LAUFEND
                for seite in self.seiten:
                    seite.reset()
                return
            
            self.seite.merke()
            if self.seite.ist_ausgewaehlt():
                if self.welche_seite < len(self.seiten) - 1:
                    self.welche_seite += 1
                else:
                    self.phase = AUSWERTUNG
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

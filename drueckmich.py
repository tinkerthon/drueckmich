import upygame as upg
import umachine as um

upg.display.init()
screen_sf = upg.display.set_mode() # full screen

upg.display.set_palette_16bit([0,0x7a45,0xaac6,65535])

breite = 110.0
hoehe = 88.0

welche_seite = 0

class Seite:
    def __init__(self, zeilen):
        self.zeilen = zeilen
        self.auswahl_zeile = 0
        self.auswahl_spalte = 0

        self.anz_spalten = 0
        for z in range(0, len(zeilen)):
            if len(zeilen[z]) > self.anz_spalten:
                self.anz_spalten = len(zeilen[z])

    def zeige(self):
        print("z=%d s=%d az=%d, as=%d" % (
            len(self.zeilen), self.anz_spalten, 
            self.auswahl_zeile, self.auswahl_spalte
        ))
        for zeile in range(0, len(self.zeilen)):
            for spalte in range(0, self.anz_spalten):
                if spalte < len(self.zeilen[zeile]):
                    text = self.zeilen[zeile][spalte]
                else:
                    text = ""
                x = round(spalte * breite / self.anz_spalten, 0)
                y = round(zeile * hoehe / len(self.zeilen), 0)
                um.draw_text(x, y, text, 1) 

    def auswahl(self, key):
        if key == pygame.K_DOWN:
            if self.auswahl_zeile < len(self.zeilen) - 1:
                self.auswahl_zeile += 1
        if key == pygame.K_UP:
            if self.auswahl_zeile > 0:
                self.auswahl_zeile -= 1
        if key == pygame.K_RIGHT:
            if self.auswahl_spalte < self.anz_spalte - 1:
                self.auswahl_spalte += 1
        if key == pygame.K_LEFT:
            if self.auswahl_spalte > 0:
                self.auswahl_spalte -= 1

seiten = []

seiten.append(Seite([
    ["Drückmich\nTiere"]
]))
seiten.append(Seite([
    ["Zootier"], 
    ["Haustier"]
]))
seiten.append(Seite([
    ["Pflegen", "Kuscheln"],
    ["Gehege oder Klo säubern", "Spaziergang machen"]
]))
seiten.append(Seite([
    ["1", "2", "3", "4"],
    ["Dreieck", "Kreis", "Quadrat", "Rechteck"]
]))

while True:

    seite = seiten[welche_seite]

    eventtype = upg.event.poll()
    if eventtype != upg.NOEVENT:
        if eventtype.type== upg.KEYDOWN:
            if not gedrueckt:
                if eventtype.key == pygame.BUT_A:
                    if welche_seite < len(seiten) - 1:
                        welche_seite += 1
                else:
                    seite.auswahl(eventtype.key)
        if eventtype.type== upg.KEYUP:
            gedrueckt = False

    seite.zeige()

    upg.display.flip()


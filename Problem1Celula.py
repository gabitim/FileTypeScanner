class Celula:
    def get_lungime(self):
        raise NotImplementedError("get_lungime trebuie implementata")

    def get_nume(self):
        raise NotImplementedError("get_name trebuie implementata")


class FibraMusculara(Celula):

    def __init__(self, nume, lungime):
        self.nume = nume
        self.lungime = lungime

    def get_lungime(self):
        return self.nume

    def get_nume(self):
        return self.lungime


class FibraNervoasa(Celula):

    def __init__(self, nume, lungime):
        self.nume = nume
        self.lungime = lungime

    def get_lungime(self):
        return self.nume

    def get_nume(self):
        return self.lungime


class MuschiGeneric(FibraMusculara):
    fibra = []
    scop = []

    def __init__(self, muschi_fibra, nume, masa_musculara, scop):
        self.fibra.append(muschi_fibra)
        self.nume = nume
        self.masa_musculara = masa_musculara
        self.scop = scop

    def get_nume(self):
        return self.nume

    def get_masa_musculara(self):
        return self.masa_musculara

    def get_scop(self):
        return self.scop


class TrunchiNervos(FibraNervoasa):
    nervi = []
    specializare = []

    def __init__(self, nervi_fibra, nume, lungime, specializare):
        self.nervi.append(nervi_fibra)
        self.nume = nume
        self.lungime = lungime
        self.specializare = specializare

    def get_nume(self):
        return self.nume

    def get_lungime(self):
        return self.lungime

    def get_specializare(self):
        return self.specializare


class PrintMaster():
    def __init__(self, muschii , nervii):
        self.muschii = muschii
        self.nervii = nervii

    def print_masa_musculara(self):
        for muschi in self.muschii:
            print("Masa musculara a muschilor [", muschi.get_nume(), "]=", muschi.get_masa_musculara())

    def print_masa_musculara_totala(self):
        masa_t = 0
        for muschi in self.muschii:
            masa_t += muschi.get_masa_musculara()

        print("masa totala a muschilor = ", masa_t)

    def print_lungime_nervi(self):
        for nerv in self.nervii:
            print("Lungime sistem nervos [", nerv.get_nume(), "]=", nerv.get_lungime())

    def print_lungime_nervi_totala(self):
        lungime = 0
        for nerv in self.nervii:
            lungime += nerv.get_lungime()

        print("Lungimea axonilor din sistemul nervos =", lungime)

    def print_muschi_cu_functie_locomotorie(self):
        print("Urmatorii muschi au functie locomotorie:")
        for muschi in self.muschii:
            if 'locomotor' in muschi.get_scop():
                print(muschi.get_nume(), muschi.get_scop())


if __name__ == '__main__':
    fibra_musc = FibraMusculara("fibra", 2)
    fibra_nerv = FibraNervoasa("Nerv", 0.32545)

    Muschi1 = MuschiGeneric(fibra_musc, "Biceps Stang", 0.235235, ["locomotor", "incordare brat stang"])
    Muschi2 = MuschiGeneric(fibra_musc, "Biceps Drept", 0.462622, ["locomotor", "incordare brat drept"])
    Muschi3 = MuschiGeneric(fibra_musc, "Triceps Stang", 0.363262, ["locomotor", "relaxere brat stang"])
    Muschi4 = MuschiGeneric(fibra_musc, "Triceps Drept", 0.362342, ["stricat", "relaxare brat stang"])
    Muschi5 = MuschiGeneric(fibra_musc, "Gamba Stanga", 0.43223, ["locomotor", "miscare glezna stanga"])
    Muschi6 = MuschiGeneric(fibra_musc, "Gamba Dreapta", 10.43223, ["locomotor", "miscare glezna stanga"])

    Nerv1 = TrunchiNervos(fibra_nerv, "Emisfera Stanga", 123.235, ["control ", "auz"])
    Nerv2 = TrunchiNervos(fibra_nerv, "Emisfera Dreapta", 121.31333, ["control ", "auz"])

    Muschii = [Muschi1, Muschi2, Muschi3, Muschi4, Muschi5, Muschi6]
    Nervii = [Nerv1, Nerv2]

    # A
    # am implementat adaugarea de scopuri si specilazari multiple cu liste
    # print(Muschi1.get_scop())
    # print(Nerv1.get_specializare())

    # B & C
    printM = PrintMaster(Muschii, Nervii)

    printM.print_masa_musculara()
    printM.print_masa_musculara_totala()
    printM.print_lungime_nervi()
    printM.print_lungime_nervi_totala()
    printM.print_muschi_cu_functie_locomotorie()

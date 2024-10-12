import math
import random
import time

from Entity.Chromosome import Chromosome


class Manager:
    MAX = 15  # Mismo peso


    def __init__(self, tamPoblacion, nGeneracion):
        self.tamPoblacion = tamPoblacion
        self.nGeneracion = nGeneracion
        self.poblacion = list()

    def ga(self, tasaSupervivencia, tasaMutacion, tasaInmigracion):
        tiempoInicio = time.time()
        self.poblacion = self.iniciarPob(self.tamPoblacion)
        self.poblacion.sort(key=lambda c: c.score, reverse=True)
        t = 0

        while t != self.nGeneracion:
            t += 1
            print(f'\n{t}ª Generación: ', end="|")
            print(self.poblacion[0].getScore(), end="|")
            if self.poblacion[0].getScore() == self.MAX:
                print(f'\n\nRespuesta encontrada en ' + "{:.2f}".format(time.time() - tiempoInicio) + ' segundos:')
                print(f'\nGenotipo: {self.poblacion[0].getBinaryChromosome()}\n\nFenotipo:')
                print(self.poblacion[0])
                break
            self.poblacion.sort(key=lambda c: c.score, reverse=True)

            # SUPERVIVENCIA
            pobSuperviviente = self.supervivencia(tasaSupervivencia)

            # CRUCE
            pobCruzada = self.cruce(self.tamPoblacion - len(pobSuperviviente))

            # Transición de generaciones después del cruce
            self.poblacion.clear()
            self.poblacion.extend(pobSuperviviente)
            self.poblacion.extend(pobCruzada)
            self.poblacion.sort(key=lambda c: c.score, reverse=True)

            # MUTACIÓN
            self.mutacion(tasaMutacion)

            # INMIGRACIÓN
            self.inmigracion(tasaInmigracion)

        if self.poblacion[0].getScore() != 15:
            print(f'\n\nNo se encontró una respuesta satisfactoria para el problema.\nTiempo de ejecución: ' + "{:.2f}".format(time.time() - tiempoInicio) + ' segundos')


    def supervivencia(self, tasaSupervivencia):
        return self.poblacion[0: math.ceil(len(self.poblacion) * tasaSupervivencia / 100)]

    def cruce(self, tamNuevaPob):
        sumaAptitud = 0
        ruletaSeleccion = []
        pobCruzada = []

        for c in self.poblacion:
            sumaAptitud += c.getScore()

        for c in self.poblacion:
            aptitudRelativa = int((c.getScore() / sumaAptitud) ** 1.5)
            for i in range(0, aptitudRelativa+1):
                ruletaSeleccion.append(c)

        for i in range(tamNuevaPob):
            c1 = ruletaSeleccion[random.randint(0, len(ruletaSeleccion) - 1)]
            c2 = ruletaSeleccion[random.randint(0, len(ruletaSeleccion) - 1)]
            c3 = self.cruzar(c1, c2)
            pobCruzada.append(Chromosome(c3))
        pobCruzada.sort(key=lambda cromosoma: cromosoma.score, reverse=True)
        return pobCruzada

    def cruzar(self, c1, c2):
        c1Binario = list(c1.getBinaryChromosome())
        c2Binario = list(c2.getBinaryChromosome())

        for i in range(0, 61, 15):
            c1Binario[i + 6: i + 15] = c2Binario[i + 6: i + 15]
        hijoBinario = ''.join(str(i) for i in c1Binario)

        return hijoBinario

    def mutacion(self, tasaMutacion):
        for i in range(int(self.tamPoblacion/100) * tasaMutacion):
            indicePob = random.randint(0, self.tamPoblacion-1)
            nuevoCromosomaBinario = list(self.poblacion[indicePob].getBinaryChromosome())

            casa = [0, 1, 2, 3, 4]
            casaAleatoria1 = casa.pop(random.randint(0, len(casa)-1))
            casaAleatoria2 = casa.pop(random.randint(0, len(casa)-1))
            casaAleatoria3 = casa.pop(random.randint(0, len(casa) - 1))
            casaAleatoria4 = casa.pop(random.randint(0, len(casa) - 1))

            alelo = random.randint(0, 4)
            casa1AleloBinario = list(nuevoCromosomaBinario[casaAleatoria1 * 15 + alelo * 3: casaAleatoria1 * 15 + alelo * 3 + 3])
            casa2AleloBinario = list(nuevoCromosomaBinario[casaAleatoria2 * 15 + alelo * 3: casaAleatoria2 * 15 + alelo * 3 + 3])

            # Alelo de Casa2 <- Alelo de Casa1, Alelo de Casa1 <- Alelo de Casa2
            nuevoCromosomaBinario[casaAleatoria2 * 15 + alelo * 3: casaAleatoria2 * 15 + alelo * 3 + 3], nuevoCromosomaBinario[casaAleatoria1 * 15 + alelo * 3: casaAleatoria1 * 15 + alelo * 3 + 3] = casa1AleloBinario, casa2AleloBinario

            alelo = random.randint(0, 4)
            casa3AleloBinario = list(nuevoCromosomaBinario[casaAleatoria3 * 15 + alelo * 3: casaAleatoria3 * 15 + alelo * 3 + 3])
            casa4AleloBinario = list(nuevoCromosomaBinario[casaAleatoria4 * 15 + alelo * 3: casaAleatoria4 * 15 + alelo * 3 + 3])

            # Alelo de Casa4 <- Alelo de Casa3, Alelo de Casa3 <- Alelo de Casa4
            nuevoCromosomaBinario[casaAleatoria4 * 15 + alelo * 3: casaAleatoria4 * 15 + alelo * 3 + 3], nuevoCromosomaBinario[casaAleatoria3 * 15 + alelo * 3: casaAleatoria3 * 15 + alelo * 3 + 3] = casa3AleloBinario, casa4AleloBinario

            # Construyendo binario del cromosoma mutado
            nuevoCromosomaBinarioString = ''.join(str(i) for i in nuevoCromosomaBinario)

            nuevoCromosoma = Chromosome(nuevoCromosomaBinarioString)

            self.poblacion.pop(indicePob)
            self.poblacion.append(nuevoCromosoma)

        self.poblacion.sort(key=lambda c: c.score, reverse=True)

    def inmigracion(self, tasaInmigracion):
        for i in range(int(self.tamPoblacion / 100) * tasaInmigracion):
            indicePob = random.randint(0, self.tamPoblacion - 1)
            self.poblacion.pop(indicePob)
            self.poblacion.append(self.generarCromosoma())
        self.poblacion.sort(key=lambda c: c.score, reverse=True)

    def iniciarPob(self, tamPoblacion):
        return [self.generarCromosoma() for i in range(tamPoblacion)]

    def generarCromosoma(self):

        cromosomaBinario = ""

        alelo = list()

        # Una lista para cada casa
        for i in range(0, 5):
            alelo.append(list())

        # Genera las 25 casas
        for i in range(1, 26):
            listaAlelos = [0, 1, 2, 3, 4]
            aleloAleatorio = listaAlelos.pop(random.randint(0, len(listaAlelos) - 1))

            # Tratamiento para que no haya alelos repetidos en cada casa
            while aleloAleatorio in alelo[(i - 1) % 5]:
                aleloAleatorio = listaAlelos.pop(random.randint(0, len(listaAlelos) - 1))

            alelo[(i - 1) % 5].append(aleloAleatorio)
            cromosomaBinario += format(aleloAleatorio, '03b')

        return Chromosome(cromosomaBinario)
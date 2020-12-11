import time
import threading
from random import randrange


#Inciando a classe herdando a classe Threading
class Filosofos(threading.Thread):
    com_fome = True
    quem_comeu = []

    def __init__(self, index, g_esq, g_dir):
        threading.Thread.__init__(self)
        self.index = index # Indice do filosofo
        self.g_esq = g_esq # Garfo na esquerda
        self.g_dir = g_dir # Garfo na direita



    def run(self):
        while(self.com_fome):
            # Filosofo pensando (sleep)
            time.sleep(randrange(10))
            print ('O filosofo %s esta com fome.' % self.index)
            self.comer()

    def comendo(self):
        self.quem_comeu.append(self.index)
        print ('O filosofo %s iniciou a comer. '% self.index)
        time.sleep(randrange(10))
        print ('O filosofo %s terminou e largou os garfos para pensar.' % self.index)

    def comer(self):
        g_esq = self.g_esq
        g_dir = self.g_dir

        while self.com_fome:
            g_esq.acquire() # Operação de threading, aguardar garfo da esquerda 
            locked = g_dir.acquire(False)  # Travado enquanto 
            if locked: break #Se o garfo direito não estiver disponivel, largar o esquedo
            g_esq.release()

            print ('Filosofo %s trocou de garfo.' % self.index)
            g_esq,g_dir = g_dir,g_esq # inverter os garfos

        else:
            return
        #Iniciam a comer
        self.comendo()
        #Largar os dois garfos após comer
        g_esq.release()
        g_dir.release()
 

   

def main():

    n = 5 # Numero de filosofos

    #Iniciar array dos garfos do semaforo
    g = [threading.Semaphore() for n in range(n)] #initialising array of semaphore i.e forks

    #(i+1)%n  usado para obter os garfos circulando entre 1 e o numero de filosofos.
    filosofos = [Filosofos(i, g[i%n], g[(i+1)%n])
            for i in range(n)]

    Filosofos.com_fome = True
    # Cada filosofo inciando o thread
    for f in filosofos: 
        f.start()

    time.sleep(randrange(50))
    Filosofos.com_fome = False
    print ("Finalizando\n")
    print("Filosofos que comeram:\n",Filosofos.quem_comeu)


if __name__ == "__main__":
    main()

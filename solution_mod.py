#!/usr/bin/python
import threading
import time
from random import randrange

class Semaphore(object):

    def __init__(self, initial):
        self.lock = threading.Condition(threading.Lock())
        self.value = initial

    def up(self):
        with self.lock:
            self.value += 1
            self.lock.notify()

    def down(self):
        with self.lock:
            while self.value == 0:
                self.lock.wait()
            self.value -= 1

class Garfo(object):

    def __init__(self, number):
        self.number = number           # id do Garfo stick ID
        self.user = -1                 # filosofo usando o garfo
        self.lock = threading.Condition(threading.Lock())
        self.taken = False

    def take(self, user):         # sync
        with self.lock:
            while self.taken == True:
                self.lock.wait()
            self.user = user
            self.taken = True
            print('Filosofo %s pegou o garfo %s\n'% (user,self.number))
            self.lock.notifyAll()

    def drop(self, user):         # sync
        with self.lock:
            while self.taken == False:
                self.lock.wait()
            self.user = -1
            self.taken = False
            print('Filosofo %s largou o garfo %s\n'% (user,self.number))
            self.lock.notifyAll()


class Filosofo (threading.Thread):
    quem_comeu = []
    def __init__(self, index, esquerda, direita, garc):
        threading.Thread.__init__(self)
        self.index = index  # index do filosofo
        self.dir = direita # garfo a direita
        self.esq = esquerda # garfo a esquerda
        self.garc = garc #garcon 
      

    def run(self):
        for i in range(20):
            self.garc.down()      
            print('Filosofo %s esta pensando\n'% (self.index))
            #time.sleep(randrange(10))    # simular tempo de pensar 
            self.esq.take(self.index)    # pegar garfo a esquerda
            #time.sleep(randrange(10))    # aguardar/evitar deadlock
            self.dir.take(self.index)    # pegar garfo a direita
            print('Filosofo %s esta comendo\n'% (self.index))
            #time.sleep(randrange(10))    # comer
            self.dir.drop(self.index)    # soltar garfo da direita
            self.esq.drop(self.index)    # soltar garfo da esquerda
            self.quem_comeu.append(self.index)
            self.garc.up()               # finalizar 
        print('Filosofo %s comeu \n'% (self.index))
        


def main(): 
    n = 5   # Numero de filosofos / garfos
    garc = Semaphore(n-1)   # garcon para evitar deadlock(n-1) 
    g = [Garfo(i) for i in range(n)] # lista de garfos

    # lista de filosofos
    f = [Filosofo(i, g[i], g[(i+1)%n], garc) for i in range(n)]
    for i in range(n): #percorre a lista
        f[i].start()
    
    print('Quem comeu foi: %s'%(Filosofo.quem_comeu))


if __name__ == "__main__":
    main()

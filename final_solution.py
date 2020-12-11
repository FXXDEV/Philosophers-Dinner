import time
import threading
from random import randrange




class Fork(object):
    def __init__(self, index):
        self.index = -1                 # keep track of philosopher using it
        self.lock = threading.Condition(threading.Lock())
        self.taken = False

    def take_fork(self,index, fork_side): #sync
       with self.lock:
            while self.taken == True:
                self.lock.wait()
            self.index = index
            self.taken = True
            print('O filosofo %s pegou o garfo da %s' % (index,fork_side))
            self.lock.notifyAll()
    def drop_fork(self,index, fork_side): #sync
       with self.lock:
            while self.taken == False:
                self.lock.wait()
            self.index = -1
            self.taken = False
            print('O filosofo %s largou o garfo da %s' % (index,fork_side))
            self.lock.notifyAll()
class Philosopher(threading.Thread):
    #Checa se todo mundo comeu
    done_eating = True
    test = 0 

    def __init__(self,index,left,right):
        threading.Thread.__init__(self)
        self.index = index #Philosepher index
        self.right = right 
        self.left = left


    def run(self):
        while(self.done_eating):
           #Philosopher is thinking ( sleeping between 1 and 10 seconds)
            time.sleep(randrange(10))
            print('O filosofo %s esta com fome' % self.index)
            self.eat()


    def eat(self):
        fork_left = self.left
        fork_right = self.right

        #while self.done_eating:
        fork_left.take_fork(self.index, 'esquerda') # pickup left fork
        #time.sleep(randrange(10)) #thinking
        fork_right.take_fork(self.index, 'direita') # pickup right fork
        #time.sleep(randrange(10)) #eating

        print('O filosofo %s jantou' % self.index)
        fork_right.drop_fork(self.index, 'esquerda')    # drop right fork
        fork_left.drop_fork(self.index, 'direita') # drop left fork
        self.test = self.test+1
    



def main():
    # Numero de filosofos / garfos
    n = 5 
    #List of forks, initialising array of semaphore
    #f = [threading.Semaphore() for i in range (n)] 
    
    


    f = [Fork(i) for i in range(n)]

    # List of philosophers :  (i+1%)5 = get right and left forks  circulary between 1 and 5 
    p = [Philosopher(i, f[i%n], f[(i+1)%n]) for i in range(n)]

    # Each philosophers start the threading 
    Philosopher.done_eating = True
    for philosopher in p:
        philosopher.start()

    #time.sleep(100)
    Philosopher.done_eating = False
    #Philosopher.done_eating = False
  



if __name__ == "__main__":
    main()
from Control.Manager import Manager

if __name__ == '__main__':
    popSize = 500
    nGeneration = 10000

    manager = Manager(popSize, nGeneration)
    manager.ga(8, 5, 1)
    

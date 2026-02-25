from algorithms.sort import Sort

class BubbleSort(Sort):
    def __init__(self, values):
        self.values = values
        self.edge = 0
        self.barrier = len(values)-1

    def generator(self):
        i = 0
        
        while True:
            self.edge = 0
            if self.barrier == 0:
                while True:
                    
                    self.edge = -1
                    yield (i,i+1,self.values, self.edge)

            if i == self.barrier:
                i = 0
                self.barrier -= 1
                self.edge = 1
                
            if self.values[i+1] < self.values[i]:
                    
                    temp = self.values[i+1]
                    self.values[i+1] = self.values[i]
                    self.values[i] = temp
            yield (i,i+1,self.values, self.edge)
            i+=1       
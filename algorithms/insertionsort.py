from algorithms.sort import Sort

class InsertionSort(Sort):
    def __init__(self, values):
        self.values = values
        

    def generator(self):

        for j in range(1, len(self.values)):
            key = self.values[j]
            i = j-1

            while i >= 0 and self.values[i] > key:
                self.values[i+1] = self.values[i]
                yield (self.values, i, j, 0)
                i -= 1
                
            self.values[i+1] = key 
            yield (self.values, i, j, 1)
        while True:
            yield (self.values, i, j, -1)
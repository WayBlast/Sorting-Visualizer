from algorithms.sort import Sort

class SelectionSort(Sort):
    def __init__(self, values):
        self.values = values

    def generator(self):
        n = len(self.values)
        for j in range(n-1):
            
            min_index = j

            for i in range(j+1, n):
                if self.values[i] < self.values[min_index]:

                    min_index = i
                yield (i, j, self.values, 0)
            self.values[j], self.values[min_index] = self.values[min_index], self.values[j] 
            yield (i, j, self.values, 1)

        while True:
            yield (0, 0, self.values, -1)



from algorithms.sort import Sort

class MergeSort(Sort):
    def __init__(self, values):
        self.values = values
        
    def generator(self, start, end, edge):
        
        if end - start > 1:

            middle = (start + end) // 2

            yield from self.generator(start, middle, 0) 
            yield from self.generator(middle, end, 0)

            left = self.values[start:middle]
            right  = self.values[middle:end]

            i = 0
            j = 0
            c = start

            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    self.values[c] = left[i]
                    i += 1
                else:
                    self.values[c] = right[j]
                    j += 1
                yield (i, j, c, self.values, 0)
                c += 1

            while i < len(left):
                self.values[c] = left[i] 
                i += 1
                c += 1
                

            while j < len(right):
                self.values[c] = right[j]
                j += 1
                c += 1
                
            
            yield (start, end, c, self.values, 1) 
            
            



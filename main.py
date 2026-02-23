import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import functools
import random

MAX_VALUE = 100
NO_ELEMENTS = 15



def bubblesort(values: list[int], i):
    # 1 step

    new_values = values
    
    done = True
    if new_values[i+1] < new_values[i]:
            done = False
            temp = new_values[i+1]
            new_values[i+1] = new_values[i]
            new_values[i] = temp
                
    return (new_values, True) if done else (new_values, False)

def draw(values: list, barcollection: plt.bar, fig: plt.figure, sort: str):
    
    match sort:
        case 'bubble':
            index = [0]
            barrier = [len(values)-1]
    
            def animate(i):
                
                if barrier[0] == 0:
                    anim.event_source.stop()
                if index[0] == barrier[0]:
                    index[0] = 0
                    barrier[0] -= 1

                y, done = bubblesort(values, index[0])
                
                for i, b in enumerate(barcollection):
                    b.set_height(y[i])
                index[0] += 1

            n = NO_ELEMENTS*NO_ELEMENTS #Number of frames
            anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n,
                                    interval=100)
            plt.show()
        case _:
            raise ValueError("Sorting Algorithm not implemented")
          

if __name__ =="__main__":
        #-------- Basics ------------#
        # 1. Generate random int list - check
        # 2. Plot to histogram - check
        # 3. Run algorithms 
        # 4. Plot result
        #-------- Animation ---------#
        # 5. Re-plot histogram for each step
        # 6. Current blocks are different color
        # ------- Fluff  ------------#
        # 7. Convert to GUI
    
    values = np.array([random.randint(1,MAX_VALUE) for _ in range(NO_ELEMENTS)])
    fig = plt.figure()
    barcollection = plt.bar(range(len(values)), values)

    
    draw(values, barcollection, fig, sort='bubble')
    
    

        


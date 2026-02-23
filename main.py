import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import functools
import random

MAX_VALUE = 100
NO_ELEMENTS = 50


def bubblesort(values: list[int], i):
    # 1 step

    values
    if values[i+1] < values[i]:
            
            temp = values[i+1]
            values[i+1] = values[i]
            values[i] = temp
                
    return values

def generateData():
    values = random.sample(range(MAX_VALUE), NO_ELEMENTS)
    fig = plt.figure()
    barcollection = plt.bar(range(len(values)), values)

    return values, fig, barcollection

def draw(values: list, fig: plt.figure ,barcollection: plt.bar, sort: str):
    
    match sort:
        case 'bubble':
            index = [0]
            barrier = [len(values)-1]
            last = [0,0]

            def animate(i):
               
                barcollection[last[0]].set_color("blue")
                barcollection[last[1]].set_color("blue")
                
                if barrier[0] == 0:
                    for bar in barcollection:
                        bar.set_color("green")
                    
                    anim.event_source.stop()
                    return barcollection

                else:
                    if index[0] == barrier[0]:
                        barcollection[index[0]].set_color("green")
                        index[0] = 0
                        barrier[0] -= 1

                
                    barcollection[index[0]].set_color("red")
                    barcollection[index[0]+1].set_color("yellow")
                
                    y = bubblesort(values, index[0])
                    
                    barcollection[index[0]].set_height(y[index[0]])
                    barcollection[index[0]+1].set_height(y[index[0]+1])

                    last[0] = index[0]
                    last[1] = index[0] + 1
                    index[0] += 1
                return barcollection
            
            n = NO_ELEMENTS*NO_ELEMENTS #Number of frames
            anim=animation.FuncAnimation(fig,animate,repeat=False,blit=True,frames=n,
                                    interval=1)
            plt.show()
        case _:
            raise ValueError("Sorting Algorithm not implemented")
          

if __name__ =="__main__":
        # 7. Convert to GUI
    
    values, fig, barcollection = generateData()
    draw(values, fig, barcollection, sort='bubble')
    
    

        


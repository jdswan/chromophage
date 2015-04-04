#!/usr/bin/python3

"""
Demo.py places 1 to 3 phages with random color channel attributes onto a
test image. An updated image is displayed every 50 turns, and upon colony death.
Un-commenting indicated line below prints turn number and colony population
each turn while simulation runs.
"""

from IPython.utils.jsonutil import PNG
import PIL.Image
from random import randint

from Simulation import Simulation


def main():
    
    s = Simulation()
    s.load_image("./Tests/sign128.png")
    
    for i in range(randint(1, 3)):
        s.add_phage_to_colony("AsexualPhage", randint(0,s.img.size[0]-1), randint(0,s.img.size[1]-1), health_max=4, 
                              old_age=2, waste_immunity=1, pop_immunity=2, reproduction_min_health=1, 
                              reproduction_cooldown=1, reproduction_penalty=2)
    
    for phage in s.colony:
        phage.set_channel_attrs_RANDOM()
        
    print("Running simulation. This could take a very long time.")
    for i in range(10000):                                  #just in case some stable ecosystem is found
        if i % 10 == 0:
            #s.img.show()
            out = s.img.resize((256,256), PIL.Image.ANTIALIAS)
            out.save("/home/jefe/chromophage/"+str(i)+".png")
        #print("TURN {}, POP {} ".format(i, len(s.colony)))        ##UNCOMMENT FOR ENHANCED OUTPUT##
        if len(s.colony) > 0:
            print(len(s.colony))
            s.advance_simulation()
        else:                                               #exit simulation if no phages
            break
        
    s.img.show()
    
if __name__ == "__main__":
    main()

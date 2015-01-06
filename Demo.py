#!/usr/bin/python3

from Simulation import Simulation
from random import randint

"""
Demo.py places 1 to 3 phages with random color channel attributes onto a
test image. An updated image is displayed every 50 turns, and upon colony death.
Un-commenting indicated line below prints turn number and colony population
each turn while simulation runs.
"""

def main():
    
    s = Simulation()
    s.load_image("./Tests/testImg_flag.jpg")
    
    for i in range(randint(1,3)):
        s.add_phage_to_colony("AsexualPhage", randint(0,159), randint(0,159), health_max=5, 
                              old_age=3, waste_immunity=1, pop_immunity=5, reproduction_min_health=1, 
                              reproduction_cooldown=1, reproduction_penalty=0)
    for phage in s.colony:
        phage.set_channel_attrs_RANDOM()
        
    print("Running simulation. This could take a very long time.")
    for i in range(10000):                                  #just in case some stable ecosystem is found
        if i % 50 == 0:
            s.img.show()
        #print("TURN {}, POP {} ".format(i, len(s.colony)))        ##UNCOMMENT FOR ENHANCED OUTPUT##
        if len(s.colony) > 0:
            s.advance_simulation()
        else:                                               #exit simulation if no phages
            break
        
    s.img.show()
    
if __name__ == "__main__":
    main()

#!/usr/bin/python3

import random
from Phages.SimplePhage import SimplePhage

class MortalPhage(SimplePhage):
    """Extends the SimplePhage with health related attributes
    MortalPhage can "die" by means of Simulation.remove_dead_phages()"""
    
    def __init__(self, x, y, health_max, old_age, waste_immunity, pop_immunity):
        super(MortalPhage, self).__init__(x, y)
        
        self.health_max = health_max                                #maximum possible health
        self.health = self.health_max                               #current health
        
        #old_age is turn when phage starts to take age-proportional health penalty
        self.old_age = old_age
        
        #waste_immunity represents resistance to an organism's own waste
        self.waste_immunity = waste_immunity                        #values above 8 have no added effect
        
        #pop_immunity represents resistance to over-population pressures
        self.pop_immunity = pop_immunity
        
    def update_health(self, color_tuple, local_population):
        """Process health penalties and bonuses"""
        #health penalty for not eating previous turn 
        if self.full == False:
            self.health -= 1
        #or health bonus for having eating previous turn
        elif (self.full == True) and (self.health < self.health_max):
            self.health += 1
        #adjust health for waste toxicity
        if color_tuple[self.waste] >> 2**self.waste_immunity:
            self.health -= 1
        #adjust health for over-population, -1 health for each phage above pop_immunity
        if local_population > self.pop_immunity:
            self.health -= (local_population - self.pop_immunity)
        #adjust health for old age
        if self.age >= self.old_age:                      #if the organism is "old"
            self.health += (self.old_age - self.age)      #take age-scaled health penalty
            
    #def health_impact_pop(self, local_population):
            
    def update(self, pixel_data, *args):
        """Update health
        Eat, poop, move
        Increment age
        Return an RBG tuple representing the state of the pixel after the SimpleEater is done"""
        c = pixel_data.color_tuple                  #RBG tuple holder
        c_coord = pixel_data.coord                  #coords set
        #health update
        local_pop = pixel_data.population
        self.update_health(c, local_pop)            #update health before pooping, else permaFalse
        #behavioral checks
        c = self.poop(c) if self.poop_check() else c    #change RBG tuple if poops
        c = self.eat(c) if self.eat_check(c) else c     #change RBG tuple if eats
        #move if necessary
        self.move(pixel_data.neighboring_pixels) if self.move_check(c, pixel_data.population) else False
        
        self.age += 1                               #increment age
        return tuple((c_coord, c))                  #return updated pixel information

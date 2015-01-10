#!/usr/bin/python3

from Phages.MortalPhage import MortalPhage
from copy import deepcopy

class AsexualPhage(MortalPhage):
    
    def __init__(self, x, y, health_max, old_age, waste_immunity, pop_immunity, 
                 reproduction_min_health, reproduction_cooldown, reproduction_penalty, *args):
        super(AsexualPhage, self).__init__(x, y, health_max, old_age, waste_immunity, pop_immunity)
        
        #phage will not reproduce when health is below this value
        self.reproduction_min_health = reproduction_min_health
        #number of turns between reproductive cycles
        self.reproduction_cooldown = reproduction_cooldown
        #number of turns until next reproductive cycle
        self.reproduction_cooldown_counter = self.reproduction_cooldown
        #amount of health lost as a result of reproducing
        self.reproduction_penalty = reproduction_penalty
        
    def reproduce(self, colony):
        """Add copy of self to colony if allowed"""
        self.reproduction_cooldown_counter = self.reproduction_cooldown         #reset reproduction countdown
        phage = deepcopy(self)                                                  #make copy of self
        phage.age = 0                                                           #reset age of copy
        phage.health = phage.health_max                                         #reset health of copy
        colony.append(phage)                                                    #add copy to colony
        self.health -= self.reproduction_penalty                                #health penalty
        
    def reproduction_check(self):
        """Return True if healthy and cooldown period has expired"""
        return True if (self.health >= self.reproduction_min_health 
                        and self.reproduction_cooldown_counter <= 0
                        ) else False
                        
                        
    def update(self, pixel_data, colony, *args):
        """Update health
        Reproduce, eat, poop, move
        Increment age, decrement reproduction cooldown counter
        Return an RBG tuple representing the state of the pixel after the SimpleEater is done"""
        c = pixel_data.color_tuple                  #RBG tuple holder
        c_coord = pixel_data.coord                  #coords set
        #health update
        local_pop = pixel_data.population
        self.update_health(c, local_pop)
        #behavioral checks
        self.reproduce(colony) if self.reproduction_check() else False
        c = self.poop(c) if self.poop_check() else c    #change RBG tuple if poops
        c = self.eat(c) if self.eat_check(c) else c     #change RBG tuple if eats
        #move if necessary
        self.move(pixel_data.neighboring_pixels) if self.move_check(c, pixel_data.population) else False
        
        self.reproduction_cooldown_counter -= 1     #decrement reproduction cooldown counter
        self.age += 1                               #increment age
        return tuple((c_coord, c))                  #return updated pixel information

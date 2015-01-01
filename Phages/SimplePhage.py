from PIL import Image
import random

class SimplePhage(object):
    """SimplePhage eats, poops, and moves"""
    
    def __init__(self, x, y):
        super(SimplePhage, self).__init__()
        self.age = 0                                #number of turns since phage created
        self.full = False                           #did phage eat last turn?
        self.health = 1                             #phage health
        self.x = x                                  #x pixel coordinate
        self.y = y                                  #y pixel coordinate
        self.consume = 4                            #phage eats 2^n bits of color value per turn
        self.excrete = 3                            #phage excretes 2^n bits of color value per turn
        #channel_attrs are int values, 0-2, corresponding to RBG channels
        self.food = int                                  
        self.waste = int
        
    ###One of these methods must be run after init
    def set_channel_attrs(self, food, waste):
        """Assign RBG channel attributes"""
        choices = ["red", "blue", "green"]
        self.food = choices.index(food)
        self.waste = choices.index(waste)
        
    def set_channel_attrs_RANDOM(self):
        """Randomly assign RBG channel attributes, poop eating prohibited"""
        _attributes = ["food", "waste", "nothing"]
        random.shuffle(_attributes)                 #randomize attribute names
        for x in range(0,3):                        #for i in {0, 1, 2}
            setattr(self, _attributes.pop(), x)     #set attribute to i
    ####
            
    def update_location(self, coord):
        """Set phage coords to (x,y) tuple"""
        self.x, self.y = coord[0], coord[1]
        
    def return_coords(self):
        """Return (x,y) tuple"""
        return tuple((self.x, self.y))
    
    def eat(self, color_tuple):                     #color_tuple is RBG value tuple
        """Return RBG color tuple modified by eating"""
        colors = [color for color in color_tuple]   #tuple dosn't support assignment, make list
        colors[self.food] -= 2**self.consume        #decrement appropriate color value
        self.full = True                            #toggle self.full
        return tuple(color for color in colors)     #return modified RBG value tuple
    
    def poop(self, color_tuple):                    #color_tuple is RBG value tuple
        """Return RBG color tuple modified by pooping"""
        colors = [color for color in color_tuple]   #tuple dosn't support assignment, make list
        colors[self.waste] += 2**self.excrete       #increment appropriate color value
        self.full = False                           #toggle self.full
        return tuple(color for color in colors)     #return modified RBG value tuple
    
    def eat_check(self, color_tuple):
        """Return True is phage is able to eat at current pixel"""
        return True if (color_tuple[self.food] > 2**self.consume) else False
    
    def poop_check(self):
        """Return True if phage needs to poop"""
        return True if (self.full) else False
    
    def move_check(self, color_tuple, pxl_population):
        """Return True if there is more poop than available food at current pixel"""
        return True if ((color_tuple[self.food] / pxl_population) < color_tuple[self.waste]) else False
        
    def move(self, neighboring_pxl_data):
        """Choose best neighboring pixel. If none exists, choose random."""
        pxls = neighboring_pxl_data
        selection = random.choice(pxls)             #random first selection
        current_food = selection.color_tuple[self.food]
        current_waste = selection.color_tuple[self.waste]
        for choice in pxls:                         #iterate through neighboring pixels
            available_food = choice.color_tuple[self.food]
            waste_present = choice.color_tuple[self.waste]
            if available_food > 0:                  #if pixel has food
                try:                                #try catches division by zero if RBG value = 0
                    #compare ratio of food to waste, choose larger
                    if ((available_food / selection.population) / waste_present 
                        > (current_food / choice.population) / current_waste ):
                        selection = choice
                except ZeroDivisionError:           #if waste or food == 0          
                    #compare food amount adjusted for population, choose larger
                    try:                            #try catches division by zero if population = 0
                        if available_food / selection.population > current_food / choice.population:
                            selection = choice
                    except ZeroDivisionError:       #if population == 0
                        #compare food amount only
                        if available_food > current_food:
                            selection = choice
        #change self location to selection coordinates
        self.update_location(selection.coord)
        
    def update(self, pixel_data, *args):
        """Eat, poop, move
        Increment age
        Return an RBG tuple representing the state of the pixel after the SimpleEater is done
        
        Every subclass of SimpleEater will have an extended version of this method"""
        c = pixel_data.color_tuple                  #RBG tuple holder
        c_coord = pixel_data.coord                  #coords set
        #behavioral checks
        c = self.poop(c) if self.poop_check() else c    #change RBG tuple if poops
        c = self.eat(c) if self.eat_check(c) else c     #change RBG tuple if eats
        #move if necessary
        self.move(pixel_data.neighboring_pixels) if self.move_check(c, pixel_data.population) else False
        
        self.age += 1                               #increment age
        return tuple((c_coord, c))                  #return updated pixel information
            
    
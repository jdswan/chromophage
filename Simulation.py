#!/usr/bin/python3

from PIL import Image
from PixelData import PixelData

class Simulation:
    
    def __init__(self, size=160):
        
        self.sim_size = size            #simulation runs on n x n pixel image
        self.colony = []                #list of Phage objects
        self.img = Image                #Image object / simulation map / petri dish
        self.populations = {}           #population map as coord : int(population) pairs
       
    def advance_simulation(self):
        self.update_populations()
        for phage in self.colony:
            pixel_data = self.make_pixel_data(phage.x, phage.y)
            new_pxl = phage.update(pixel_data, self.colony)
            self.img.putpixel((new_pxl[0][0], new_pxl[0][1]), self.bound_rbg_tuple(new_pxl[1]))
            self.remove_dead_phages()
            
    ###SETUP FUNCTIONS    
    def add_phage_to_colony(self, phage_class, x, y, **kwargs):
        """Place initial phages on image"""
        module = __import__("Phages."+phage_class, fromlist=[phage_class])
        self.colony.append(getattr(module, phage_class)(x, y, **kwargs))

    def load_image(self, image):
        """Open, resize, and load image for simulation"""
        self.img = Image.open(image)
        self.img.load()
    ###
        
    ###PixelData FUNCTIONS
    def get_neighboring_coords(self, coord):
        """Get all coords bordering pixel (coord), diagonals included"""
        x, y = coord[0], coord[1]
        #get all coordinate sets adjacent to (x,y)
        return [(_x, _y) for _x in range(x-1, x+2) for _y in range(y-1, y+2)
        #skip coordinates with values less than 0 or > image size and remove original (x,y)
                  if _x >= 0 and _y >= 0 and _x <= (self.img.size[0] - 1) 
                  and _y <= (self.img.size[1] - 1) and (x, y) != (_x, _y)
                ]

    def neighboring_pixel_data(self, x, y):
        """Return list of (coordinate, RGB_tuple) pairs"""     
        return [PixelData(coord, self.img.getpixel(coord), self.get_population(coord))
                for coord in self.get_neighboring_coords((x, y))]
        
    def get_population(self, coord):
        """Get population of pixel (coord)"""
        return self.populations[coord] if coord in self.populations.keys() else 0    
        
    def make_pixel_data(self, x, y):
        """Return PixelData object for pixel (x,y)"""
        coord = (x,y)
        p = PixelData(coord, self.img.getpixel(coord), self.get_population(coord))
        p.neighboring_pixels = self.neighboring_pixel_data(x, y)
        return p
    ###
    
    ###CLEANUP FUNCTIONS
    def remove_dead_phages(self):
        """Replace colony list with one excluding all phages having no health"""
        self.colony = [phage for phage in self.colony if phage.health > 0]
        
    def bound_rbg_tuple(self, color_tuple):
        """Return RBG tuple with 0/255 as min/max value for each color channel"""
        top_bound = []
        for value in color_tuple:
            top_bound.append(value) if (value <= 255) else top_bound.append(255)
        bound = []
        for value in top_bound:
            bound.append(value) if (value >=0) else bound.append(0)
        return tuple(value for value in bound)
    
    def update_populations(self):
        """Remake populations dict with current counts"""
        self.populations = {}
        for phage in self.colony:
            if phage.return_coords() in self.populations.keys():
                self.populations[phage.return_coords()] += 1
            else:
                self.populations[phage.return_coords()] = 1
    ###

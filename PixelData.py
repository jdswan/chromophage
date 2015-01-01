

class PixelData:
    def __init__(self, coord, color_tuple, population):
        self.coord = coord
        self.color_tuple = color_tuple
        self.population = population
        
        self.neighboring_pixels = [] # list of PixelData objects for surrounding pixels
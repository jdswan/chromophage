import unittest

from Phages.SimplePhage import SimplePhage
from PixelData import PixelData

class SimplePhageTest(unittest.TestCase):
    
    ###Test location methods
    def test_update_location_x(self):
        phage = SimplePhage(0,0)
        phage.update_location((3,0))
        self.assertEqual(phage.x, 3)
        
    def test_update_location_y(self):
        phage = SimplePhage(0,0)
        phage.update_location((0,3))
        self.assertEqual(phage.y, 3)
        
    def test_return_coords(self):
        phage = SimplePhage(0,0)
        phage.update_location((3,3))
        self.assertEqual(phage.return_coords(), (3,3))
        
    ###Test set_attributes_RANDOM()
    def test_set_channel_attrs(self):
        phage = SimplePhage(0,0)
        phage.set_channel_attrs(food="red", waste="blue")
        attr_values = [getattr(phage, attr) for attr in ["food", "waste"]]
        attr_values.sort()
        self.assertTrue(0 <= attr_values[0] < attr_values[1] <=2)
        
    def test_set_channel_attrs_RANDOM(self):
        phage = SimplePhage(0,0)
        phage.set_channel_attrs_RANDOM()
        attr_values = [getattr(phage, attr) for attr in ["food", "waste", "nothing"]]
        attr_values.sort()
        self.assertEqual(attr_values, [0,1,2])
        
    ###Test eating mechanism
    def test_eat(self):
        phage = SimplePhage(0,0)
        phage.food = 0
        color_tuple = tuple((246, 14, 64))
        self.assertEqual(phage.eat(color_tuple), tuple(((246 - 2**phage.consume), 14, 64)))
        
    def test_eat_check_pos(self):
        phage = SimplePhage(0,0)
        phage.food = 0
        color_tuple = tuple((246, 14, 0))
        self.assertTrue(phage.eat_check(color_tuple))
        
    def test_eat_check_neg(self):
        phage = SimplePhage(0,0)
        phage.food = 0
        color_tuple = tuple((0, 0, 0))
        self.assertFalse(phage.eat_check(color_tuple))
        
    ###Test pooping mechanism
    def test_poop(self):
        phage = SimplePhage(0,0)
        phage.waste = 1
        color_tuple = tuple((246, 14, 64))
        self.assertEqual(phage.poop(color_tuple), tuple((246, (14 + 2**phage.excrete), 64)))
            
    def test_poop_check_pos(self):
        phage = SimplePhage(0,0)
        phage.full = True
        self.assertTrue(phage.poop_check())
        
    def test_poop_check_neg(self):
        phage = SimplePhage(0,0)
        phage.full = False
        self.assertFalse(phage.poop_check())
    
    ###Test move mechanism
    def test_move_check_pos(self):
        phage = SimplePhage(0,0)
        phage.food = 1
        phage.waste = 0
        color_tuple = tuple((246, 14, 0))
        pxl_pop = 1
        self.assertTrue(phage.move_check(color_tuple, pxl_pop))
        
    def test_move_check_neg(self):
        phage = SimplePhage(0,0)
        phage.food = 0
        phage.waste = 1
        color_tuple = tuple((246, 14, 0))
        pxl_pop = 1
        self.assertFalse(phage.move_check(color_tuple, pxl_pop))
        
    def test_move_check_pos_on_pop(self):
        phage = SimplePhage(0,0)
        phage.food = 0
        phage.waste = 1
        color_tuple = tuple((199, 100, 0))
        pxl_pop = 2
        self.assertTrue(phage.move_check(color_tuple, pxl_pop))
        
    def test_move(self):
        phage = SimplePhage(0,0)
        phage.x = 0
        phage.y = 0
        phage.food = 0
        phage.waste = 1
        p = PixelData((0,0), (0,0,0,), 1)
        p.neighboring_pxls = [PixelData((0,1), (0, 255, 255), 0),
                              PixelData((1,0), (0, 255, 255), 0),
                              PixelData((1,1), (255, 0, 0), 0)]
        phage.move(p.neighboring_pxls)
        self.assertTrue((phage.x == 1) and (phage.y == 1))
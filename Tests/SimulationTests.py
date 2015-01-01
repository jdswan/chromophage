import unittest
from PIL import ImageFile

from Simulation import Simulation

class SimulationTest(unittest.TestCase):

    def test_load_img(self):
        s = Simulation()
        s.load_image("./Tests/testImg_flag.jpg")
        self.assertIsInstance(s.img, ImageFile.ImageFile) 
     
    def test_get_neighboring_coords_corner(self):
        s = Simulation()
        s.load_image("./Tests/testImg_flag.jpg")
        self.assertEqual(s.get_neighboring_coords((0,0)), [(0,1), (1,0), (1, 1)])
        
    def test_get_neighboring_coords_edge(self):
        s = Simulation()
        s.load_image("./Tests/testImg_flag.jpg")
        self.assertEqual(s.get_neighboring_coords((0,1)), [(0,0), (0,2), (1,0), (1, 1), (1,2)])
        
    def test_get_neighboring_coords_middle(self):
        s = Simulation()
        s.load_image("./Tests/testImg_flag.jpg")
        self.assertEqual(s.get_neighboring_coords((1,1)), [(0,0), (0,1), (0,2)
                                                         ,(1,0), (1,2)
                                                         ,(2,0), (2, 1), (2,2)])

    def test_bound_rbg_tuple_max(self):
        s = Simulation()
        color_tuple = (860, 256, 1000)
        self.assertEqual(s.bound_rbg_tuple(color_tuple), (255, 255, 255))
        
    def test_bound_rbg_tuple_min(self):
        s = Simulation()
        color_tuple = (-1, -120, -2120)
        self.assertEqual(s.bound_rbg_tuple(color_tuple), (0, 0, 0))



        
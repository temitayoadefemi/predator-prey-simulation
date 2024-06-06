import unittest
import numpy as np
from io import StringIO
from unittest.mock import patch
from predator_prey.Landscape import Landscape

class TestLandscape(unittest.TestCase):
    """
    Unit test class for testing the Landscape class.
    """

    def setUp(self):
        """
        Set up method for unit tests. Creates an instance of the Landscape class.
        """
        self.landscape = Landscape("map.dat")
        
    def test_init(self):
        """
        Test the initialization of the Landscape class. It checks if the width, height,
        landscape and neighbours attributes are correctly set.
        """
        self.assertEqual(self.landscape.width, 10)
        self.assertEqual(self.landscape.height, 20)
        self.assertIsNotNone(self.landscape.landscape)
        self.assertIsNotNone(self.landscape.neighbours)
        
    def test_load_landscape(self):
        """
        Test the 'load_landscape' method of the Landscape class. It tests both valid and invalid landscapes.
        """
        # Test valid landscape
        with patch('builtins.open', return_value=StringIO('10 20\n' + (('1 '*10).strip()+'\n')*20)) as mock_file:
            landscape = Landscape("landscape.txt")
            self.assertEqual(landscape.width, 10)
            self.assertEqual(landscape.height, 20)
            self.assertEqual(landscape.landscape.shape, (22, 12))
            self.assertEqual(landscape.landscape[1][1], 1)
        
        # Test invalid landscape: non-integer dimensions
        with patch('builtins.open', return_value=StringIO('10a 20\n' + (('1 '*10).strip()+'\n')*20)) as mock_file:
            with self.assertRaises(RuntimeError):
                Landscape("map.dat")

        # Test invalid landscape: wrong line length
        with patch('builtins.open', return_value=StringIO('10 20\n' + (('1 '*9).strip()+'\n')*20)) as mock_file:
            with self.assertRaises(RuntimeError):
                Landscape("map.dat")



    def test_calculate_neighbours(self):
        """
        Test the 'calculate_neighbours' method. It checks the 
        generated neighbours matrix against the expected matrix.
        """
        # Load the landscape from the 'map.dat' file
        landscape_file = "map.dat"
        landscape = Landscape(landscape_file)

        # Generate the neighbours matrix
        calculated_neighbours = landscape.calculate_neighbours()

        # Create 'expected_neighbours' array.
        expected_neighbours = np.full((landscape.height+2, landscape.width+2), 4)  # Fill all inner cells with 4.
        expected_neighbours[0, :] = expected_neighbours[-1, :] = 1  # Top and bottom edge.
        expected_neighbours[:, 0] = expected_neighbours[:, -1] = 1  # Left and right edge.
        expected_neighbours[1:-1, 1] = expected_neighbours[1:-1, -2] = 3  # Second column and second last column
        expected_neighbours[1, 1:-1] = expected_neighbours[-2, 1:-1] = 3  # Second row and second last row
        expected_neighbours[0, 0] = expected_neighbours[0, -1] = expected_neighbours[-1, 0] = expected_neighbours[-1, -1] = 0  # Corners.
        expected_neighbours[1, 1] = expected_neighbours[1, -2] = expected_neighbours[-2, 1] = expected_neighbours[-2, -2] = 2  # Second corners.

        # Assert that the calculated neighbours match the expected neighbours
        np.testing.assert_array_equal(calculated_neighbours, expected_neighbours)



    def test_calculate_land_only(self):
        """
        Test the 'calculate_land_only' method of the Landscape class. It checks if 
        the method returns the correct number of land cells.
        """
        self.assertEqual(self.landscape.land_squares, 200)


    def test_repr(self):
        """
        Test the '__repr__' method of the Landscape class. It checks if the method 
        returns the correct representation of the object.
        """
        self.assertEqual(repr(self.landscape), "<Landscape shape=(22, 12)>")


class CustomTestRunner(unittest.TextTestRunner):
    """
    Custom Test Runner class that overrides the 'run' method of TextTestRunner to print a success message 
    when all tests pass.
    """

    def run(self, test):
        """
        Run the given test case or test suite.
        """
        result = super().run(test)
        if result.wasSuccessful():
            print("All tests ran successfully.")
        return result
    
if __name__ == "__main__":
    # Run unit tests with the custom test runner
    unittest.main(testRunner=CustomTestRunner())
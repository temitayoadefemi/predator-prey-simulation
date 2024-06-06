import unittest
import numpy as np
from io import StringIO
from unittest.mock import patch, Mock
from predator_prey.Animal import AnimalModel


class TestAnimalModel(unittest.TestCase):
    """
    Unit test class for testing the AnimalModel class.
    """

    def setUp(self):
        """
        Set up method for unit tests. Creates an instance of the AnimalModel class 
        with a mock landscape object.
        """
        self.mock_landscape = Mock()
        self.mock_landscape.landscape = np.zeros((5, 5))  # Mock landscape as a 5x5 zeroed numpy array
        self.animal = AnimalModel(1, 0.5, 0.5, 0.5, self.mock_landscape, 'Animal')

    def test_validate_rate(self):
        """
        Test the method 'validate_rate' raises a ValueError for invalid rate values 
        and correctly returns the rate for a valid input.
        """
        with self.assertRaises(ValueError):
            self.animal.validate_rate(-1)
        with self.assertRaises(ValueError):
            self.animal.validate_rate(1.5)
        self.assertEqual(self.animal.validate_rate(0.5), 0.5)

    def test_calculate_max(self):
        """
        Test the method 'calculate_max' correctly identifies the maximum population 
        in the given landscape.
        """
        self.animal.population = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.assertEqual(self.animal.calculate_max(), 8)

    def test_calculate_average(self):
        """
        Test the method 'calculate_average' correctly calculates the average population 
        in the given landscape.
        """
        self.animal.population = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.assertEqual(self.animal.calculate_average(9), 4)  # 9 = total number of cells in population array

    def test_validate_coordinates(self):
        """
        Test the method 'validate_coordinates' raises an IndexError for invalid coordinates 
        and returns True for valid ones.
        """
        with self.assertRaises(IndexError):
            self.animal.validate_coordinates((-1, 0))
            self.animal.validate_coordinates((0, -1))
            self.animal.validate_coordinates((5, 0))
            self.animal.validate_coordinates((0, 5))
        self.assertTrue(self.animal.validate_coordinates((2, 2)))

    def test_initialize_population(self):
        """
        Test the method 'initialize_population' correctly initializes the population 
        based on the given landscape and seed.
        """
        self.mock_landscape.landscape = np.array([[0, 1], [1, 0]])
        self.animal = AnimalModel(1, 0.5, 0.5, 0.5, self.mock_landscape, 'Animal')
        self.animal.seed = 0
        self.assertEqual(self.animal.initialize_population().tolist(), [[0.0, 1.0], [1.0, 0.0]])  # with seed = 0


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
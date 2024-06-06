import unittest
import os
import numpy as np
from predator_prey.Helpers import SimulationHelpers

class TestSimulationHelpers(unittest.TestCase):
    """
    Unit test class for testing the SimulationHelpers class.
    """

    def setUp(self):
        """
        Set up method for unit tests. Creates an instance of the SimulationHelpers class.
        """
        self.sim_helpers = SimulationHelpers()

    def test_getVersion(self):
        """
        Test the method 'getVersion' correctly returns the version number.
        """
        self.assertEqual(self.sim_helpers.getVersion(), 3.0)

    def test_log_averages(self):
        """
        Placeholder for the 'log_averages' method test.
        """
        pass

    def test_write_population_map(self):
        """
        Test the method 'write_population_map' correctly generates a '.ppm' file 
        with the expected filename.
        """
        # Create some mock data
        h, w = 5, 5
        lscape = np.ones((h+2, w+2))
        mice = np.full((h+2, w+2), 10)
        fox = np.full((h+2, w+2), 20)

        # Call the method
        self.sim_helpers.write_population_map(1, mice, fox, 10, 20, lscape)

        # Check that the file was created
        self.assertTrue(os.path.isfile('map_0001.ppm'))

        # Clean up
        os.remove('map_0001.ppm')

    def test_write_avg_file(self):
        """
        Test the method 'write_avg_file' correctly generates a '.txt' file 
        with the expected filename and content.
        """
        filename = "test_file.txt"
        
        # Call the method
        self.sim_helpers.write_avg_file(filename, 1, 2.0, 3.0, 4.0)
        
        # Check that the file was created
        self.assertTrue(os.path.isfile(filename))
        
        # Check the content of the file
        with open(filename, 'r') as file:
            content = file.read()
            self.assertEqual(content, '1,2.0,3.00000000000000000,4.00000000000000000\n')
        
        # Clean up
        os.remove(filename)

    def test_validate_log_interval(self):
        """
        Test the 'validate_log_interval' method correctly raises ValueError for invalid inputs.
        """
        with self.assertRaises(ValueError):
            self.sim_helpers.validate_log_interval(10, 5)
        with self.assertRaises(ValueError):
            self.sim_helpers.validate_log_interval(-1, 10)
        # Test for a valid input
        try:
            self.sim_helpers.validate_log_interval(5, 10)
        except ValueError:
            self.fail("validate_log_interval() raised ValueError unexpectedly!")

    def test_validate_duration(self):
        """
        Test the 'validate_duration' method correctly raises ValueError for invalid inputs.
        """
        with self.assertRaises(ValueError):
            self.sim_helpers.validate_duration(0)
        with self.assertRaises(ValueError):
            self.sim_helpers.validate_duration(-1)
        # Test for a valid input
        try:
            self.sim_helpers.validate_duration(10)
        except ValueError:
            self.fail("validate_duration() raised ValueError unexpectedly!")

    def test_validate_delta(self):
        """
        Test the 'validate_delta' method correctly raises ValueError for invalid inputs and 
        correctly returns the value for valid inputs.
        """
        with self.assertRaises(ValueError):
            self.sim_helpers.validate_delta(-0.1)
        with self.assertRaises(ValueError):
            self.sim_helpers.validate_delta(1.5)
        # Test for valid inputs
        self.assertEqual(self.sim_helpers.validate_delta(0), 0)
        self.assertEqual(self.sim_helpers.validate_delta(0.5), 0.5)
        self.assertEqual(self.sim_helpers.validate_delta(1), 1) ,


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
import unittest
from unittest.mock import Mock
import numpy as np
from predator_prey.Simulation import Simulation
from flexmock import flexmock
from predator_prey.Animal import Mice, Fox
from predator_prey.Simulation import Landscape

class TestSimulation(unittest.TestCase):
    """
    Unit test class for testing the Simulation class.
    """

    def setUp(self):
        """
        Set up method for unit tests. It creates mocks for the entities involved in the simulation.
        """
        self.landscape = flexmock(Landscape("map.dat"))
        self.mice = flexmock(Mice(seed=0, diffusion_rate=0.1, birth_rate=0.2, death_rate=0.1, landscape=self.landscape))
        self.fox = flexmock(Fox(seed=0, diffusion_rate=0.1, birth_rate=0.2, death_rate=0.1, landscape=self.landscape))
        self.timestep = 1

        # Set some default return values for our mocks
        self.mice.population = np.full((3, 3), 10)
        self.fox.population = np.full((3, 3), 10)
        self.mice.birth_rate = 0.2
        self.mice.death_rate = 0.1
        self.mice.diffusion_rate = 0.1
        self.fox.birth_rate = 0.2
        self.fox.death_rate = 0.1
        self.fox.diffusion_rate = 0.1
        self.landscape.landscape = np.ones((3, 3), dtype=bool)
        self.landscape.should_receive('land_squares').and_return(9)
        self.landscape.neighbours = np.full((3, 3), 4)
        self.landscape.height = 1
        self.landscape.width = 1

        # Initialize the simulation
        self.simulation = Simulation(self.mice, self.fox, self.landscape, self.timestep)

    def test_calculate_population_average(self):
        """
        Test the 'calculate_population_average' method of Simulation class. It checks 
        if the method returns the correct average population for mice and foxes.
        """
        # Test for mice
        self.mice.calculate_average(self.landscape.land_squares)
        avg = self.simulation.get_mice_avg
        self.assertEqual(avg, 10.0)

        # Test for foxes
        self.fox.calculate_average(self.landscape.land_squares)
        avg = self.simulation.get_fox_avg
        self.assertEqual(avg, 10.0)

    def test_calculate_diffusion(self):
        """
        Test the 'calculate_diffusion' method of Simulation class. It checks if the 
        method successfully calculates the diffusion for the given population, coordinates, 
        and diffusion rate.
        """
        current_pop = np.full((5, 5), 10)
        x, y = 2, 2
        diffusion_rate = 0.1
        self.landscape.neighbours = np.full((5, 5), 4)
        diffusion = self.simulation.calculate_diffusion(current_pop, x, y, diffusion_rate)
        self.assertEqual(diffusion, 0.0)

    def test_calculate_population_max(self):
        """
        Test the 'calculate_population_max' method of Simulation class. It checks 
        if the method returns the correct maximum population for mice and foxes.
        """
        # Test for mice
        self.mice.calculate_max()
        max_pop = self.simulation.get_mice_max
        self.assertEqual(max_pop, 10)

        # Test for foxes
        self.fox.calculate_max()
        max_pop = self.simulation.get_fox_max
        self.assertEqual(max_pop, 10)

    def test_update_population(self):
        """
        Test the 'update_population' method of Simulation class. It checks if the 
        method updates the population correctly for mice and foxes.
        """
        x, y = 1, 1

        # Test for mice
        self.mice.birth_rate = 0.2
        self.mice.death_rate = 0.1
        self.mice.diffusion_rate = 0.1
        self.simulation.update_mice_population(x, y)
        self.assertTrue(self.simulation.next_mice_pop[x, y] >= 0)

        # Test for foxes
        self.fox.birth_rate = 0.2
        self.fox.death_rate = 0.1
        self.fox.diffusion_rate = 0.1
        self.simulation.update_fox_population(x, y)
        self.assertTrue(self.simulation.next_fox_pop[x, y] >= 0)

    def test_run(self):
        """
        Test the 'run' method of Simulation class. It checks if the method properly 
        updates the current populations of mice and foxes.
        """
        self.simulation.run()
        self.assertTrue(np.all(self.simulation.current_mice_pop >= 0))
        self.assertTrue(np.all(self.simulation.current_fox_pop >= 0))


class CustomTestRunner(unittest.TextTestRunner):
    """
    Custom Test Runner class that overrides the 'run'```python
class CustomTestRunner(unittest.TextTestRunner):
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
import unittest
import numpy as np
from predator_prey.Animal import Mice
from predator_prey.Animal import Fox
from predator_prey.Landscape import Landscape
from predator_prey.Simulation import Simulation

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """
        Set up data for the tests. This method is run before each test.
        """
        self.landscape = Landscape("map.dat")
        self.mice = Mice(birth_rate=0.1, death_rate=0.01, diffusion_rate=0.1, seed=1, landscape=self.landscape)
        self.fox = Fox(birth_rate=0.05, death_rate=0.1, diffusion_rate=0.05, seed=1, landscape=self.landscape)
        
        self.timestep = 1
        self.simulation = Simulation(self.mice, self.fox, self.landscape, self.timestep)
    
    def test_run_simulation(self):
        """
        Test the 'run' method of the Simulation class.
        """
        # Run the simulation
        self.simulation.run()
        
        # Check if the populations have been updated
        self.assertNotEqual(self.simulation.current_mice_pop.tolist(), self.mice.population.tolist())
        self.assertNotEqual(self.simulation.current_fox_pop.tolist(), self.fox.population.tolist())

    # Add more tests as needed...


class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        if result.wasSuccessful():
            print("All tests ran successfully.")
        return result

if __name__ == "__main__":
    unittest.main(testRunner=CustomTestRunner())
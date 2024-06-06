import numpy as np
from .Landscape import Landscape
from .Animal import Mice, Fox

class Simulation(object):
    """
    Main class for the animal model simulation.
    """

    def __init__(self, mice, fox, landscape, timestep):

        """
        Initializes Simulation with Mice, Fox, Landscape instances, and a timestep.

        mice (Mice): Instance of Mice class representing the mice population.
        fox (Fox): Instance of Fox class representing the fox population.
        landscape (Landscape): Instance of Landscape class representing the environment.
        timestep (int): The time interval for each simulation step.
        """
              
        # Input validation
        if not all(isinstance(x, (Mice, Fox)) for x in [mice, fox]):
            raise ValueError("Mice and Fox should be instances of the Mice and Fox classes.")
        if not isinstance(landscape, Landscape):
            raise ValueError("Landscape should be an instance of the Landscape class.")

        # Initialize the parameters
        self.mice = mice
        self.fox = fox
        self.landscape = landscape
        self.current_mice_pop = mice.population
        self.next_mice_pop = mice.population.copy()
        self.current_fox_pop = fox.population
        self.next_fox_pop = fox.population.copy()
        self.timestep = timestep

        # Cache the indices of land squares for efficiency
        self.land_squares = np.where(self.landscape.landscape == 1)

    def calculate_diffusion(self, current_pop, diffusion_rate):
        # Make use of numpy's vectorized operations to calculate diffusion for all cells at once

        """
        Calculates diffusion based on the current population state and diffusion rate.

        current_pop (ndarray): Current population grid.
        x (int): x-coordinate of the landscape.
        y (int): y-coordinate of the landscape.
        diffusion_rate (float): Diffusion rate.
        
        Returns:
        float: Calculated diffusion.
        """
        
        diffused_pop = diffusion_rate * (
            np.roll(current_pop, -1, axis=0) + np.roll(current_pop, 1, axis=0) +
            np.roll(current_pop, -1, axis=1) + np.roll(current_pop, 1, axis=1) -
            self.landscape.neighbours * current_pop
        )
        return diffused_pop
    
    @property
    def get_mice_max(self):

        """
        Gets the maximum population of mice.

        Returns:
        int: The maximum population of mice.
        """
        
        return self.mice.calculate_max()

    @property
    def get_fox_max(self):
        """
        Gets the maximum population of fox.

        Returns:
        int: The maximum population of fox.
        """

        return self.fox.calculate_max()
    
    @property
    def get_mice_avg(self):
        """
        Gets the average population of mice.

        Returns:
        float: The average population of mice.
        """
        
        return self.mice.calculate_average(self.landscape.land_squares)

    @property
    def get_fox_avg(self):
        """
        Gets the average population of fox.

        Returns:
        float: The average population of fox.
        """
        return self.fox.calculate_average(self.landscape.land_squares)

    def calculate_diffusion(self, current_pop, x, y, diffusion_rate):
        """
        Calculates the diffusion for population based on current state and parameters.

        Parameters:
        current_pop (ndarray): The current population grid.
        x (int): The x-coordinate of the landscape.
        y (int): The y-coordinate of the landscape.
        diffusion_rate (float): The diffusion rate.

        Returns:
        float: The calculated diffusion.
        """
        return diffusion_rate * (current_pop[x - 1, y] + current_pop[x + 1, y] + current_pop[x, y - 1] + current_pop[x, y + 1] - self.landscape.neighbours[x, y] * current_pop[x, y])

    def update_mice_population(self, x, y):
        """
        Updates mice population based on current state and parameters.

        Parameters:
        x (int): The x-coordinate of the landscape.
        y (int): The y-coordinate of the landscape.
        """
        # Calculate birth, death, and diffusion rates for mice
        mouse_birth = self.mice.birth_rate * self.current_mice_pop[x, y]
        mouse_death = self.mice.death_rate * self.current_mice_pop[x, y] * self.current_fox_pop[x, y]
        mouse_diffusion = self.calculate_diffusion(self.current_mice_pop, x, y, self.mice.diffusion_rate)
        # Update next population
        self.next_mice_pop[x, y] = max(0, self.current_mice_pop[x, y] + self.timestep * (mouse_birth - mouse_death + mouse_diffusion))

    def update_fox_population(self, x, y):
        """
        Updates fox population based on current state and parameters.

        Parameters:
        x (int): The x-coordinate of the landscape.
        y (int): The y-coordinate of the landscape.
        """
        # Calculate birth, death, and diffusion rates for fox
        fox_birth = self.fox.birth_rate * self.current_mice_pop[x, y] * self.current_fox_pop[x, y]
        fox_death = self.fox.death_rate * self.current_fox_pop[x, y]
        fox_diffusion = self.calculate_diffusion(self.current_fox_pop, x, y, self.fox.diffusion_rate)
        # Update next population
        self.next_fox_pop[x, y] = max(0, self.current_fox_pop[x, y] + self.timestep * (fox_birth - fox_death + fox_diffusion))

    def run(self):
        """
        Runs the simulation for each time step.
        """
        # Loop over each time step
        for x in range(1, self.landscape.height + 1):
            for y in range(1, self.landscape.width + 1):
                # If the cell at (x, y) is land, update the mice and fox populations
                if self.landscape.landscape[x, y]:
                    self.update_mice_population(x, y)
                    self.update_fox_population(x, y)

        # Swap the current and next populations for the next iteration
        self.current_mice_pop, self.next_mice_pop = self.next_mice_pop, self.current_mice_pop
        self.current_fox_pop, self.next_fox_pop = self.next_fox_pop, self.current_fox_pop
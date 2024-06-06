import numpy as np
import random


class AnimalModel(object):
    """
    Main class for the animal model simulation.
    This class simulates the population distribution of a particular animal type over time in a landscape.
    """
    def __init__(self, seed, diffusion_rate, birth_rate, death_rate, landscape, animal_type):
        """
        Initializes the animal model with given parameters.

        Parameters:
        seed (int): Seed for random number generator. Determines the initial distribution of animals.
        diffusion_rate (float): Rate at which animals spread across the landscape.
        birth_rate (float): Rate at which animals reproduce.
        death_rate (float): Rate at which animals die.
        landscape (Landscape): The landscape where the animals live.
        animal_type (str): The type of animals being simulated.
        """
        self.seed = seed
        self.diffusion_rate = self.validate_rate(diffusion_rate)  # Validate the input rates
        self.birth_rate = self.validate_rate(birth_rate)
        self.death_rate = self.validate_rate(death_rate)
        self.landscape = landscape
        self.population = self.initialize_population()  # Initialize the population distribution
        self.animal_type = animal_type

    def validate_rate(self, rate):
        """
        Validates that rate values are between 0 and 1.

        Parameters:
        rate (float): Rate value to validate.

        Returns:
        float: Validated rate value.

        Raises:
        ValueError: If rate is not between 0 and 1.
        """
        if 0 <= rate <= 1:
            return rate
        else:
            raise ValueError("Rate must be between 0 and 1.")

    def calculate_max(self):
        """
        Calculate the maximum population across the landscape.

        Returns:
        float: Maximum population.
        """
        return np.max(self.population)

    def calculate_average(self, nlands):
        """
        Calculate the average population across the landscape.

        Parameters:
        nlands (int): The number of lands.

        Returns:
        float: Average population.
        """
        if nlands != 0:
            average = np.sum(self.population)/nlands
        else:
            average=0
        return average

    def validate_coordinates(self, coords):
        """
        Validates that coordinates are within the landscape bounds.

        Parameters:
        coords (tuple): Coordinates to validate.

        Returns:
        bool: True if coordinates are valid. 

        Raises:
        IndexError: If coordinates are out of range.
        """
        if 0 <= coords[0] < self.landscape.landscape.shape[0] and 0 <= coords[1] < self.landscape.landscape.shape[1]:
            return True
        else:
            raise IndexError("Coordinates are out of range.")

    def initialize_population(self):
        """
        Initializes the population distribution based on the given seed.

        Returns:
        np.array: Initial population distribution.
        """
        random.seed(self.seed)
        population = self.landscape.landscape.astype(float).copy()
        for x in range(1, self.landscape.landscape.shape[0] - 1):
            for y in range(1, self.landscape.landscape.shape[1] - 1):
                if self.seed == 0:
                    population[x, y] = 0  # No population if seed is zero
                else:
                    if self.landscape.landscape[x, y]:
                        population[x, y] = random.uniform(0, 5.0)  # Random population between 0 and 5.0 if landscape exists
                    else:
                        population[x, y] = 0  # No population if no landscape
        return population
    
    
    
class Mice(AnimalModel):
    def __init__(self, seed, diffusion_rate, birth_rate, death_rate, landscape):
        super().__init__(seed, diffusion_rate, birth_rate, death_rate, landscape, 'Mice')
        # The animal_type is specified directly in the super() call.


class Fox(AnimalModel):
    def __init__(self, seed, diffusion_rate, birth_rate, death_rate, landscape):
        super().__init__(seed, diffusion_rate, birth_rate, death_rate, landscape, 'Fox')
        # The animal_type is specified directly in the super() call.

    

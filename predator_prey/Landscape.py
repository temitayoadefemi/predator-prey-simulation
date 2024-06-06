import numpy as np
from scipy.signal import convolve2d

class Landscape(object):
    """
    Class representing a landscape, which is a spatial grid loaded from a file.
    Each cell in the grid can either be habitable or not.
    """

    def __init__(self, landscape_file):
        """
        Initializes the landscape by loading it from a file.

        Parameters:
        landscape_file (str): The file from which to load the landscape.
        """
        self.width = None
        self.height = None
        self.landscape = self.load_landscape(landscape_file)
        self.neighbours = self.calculate_neighbours()

    def load_landscape(self, landscape_file):
        """
        Loads a landscape from a file.

        Parameters:
        landscape_file (str): The file from which to load the landscape.

        Returns:
        np.array: 2D numpy array representing the landscape.
        """
        try:
            with open(landscape_file, "r") as f:
                lines = f.readlines()
            if not lines:
                raise ValueError("File is empty.")

            w, h = map(int, lines[0].split())
            self.width = w
            self.height = h
            if not (w > 0 and h > 0):
                raise ValueError(f"Invalid landscape dimensions: {w}, {h}")

            if len(lines[1:]) != h:
                raise ValueError(f"Expected {h} lines in file, but found {len(lines[1:])}")

            landscape = np.zeros((h+2, w+2), int)

            # Load landscape from the file, line by line
            for i, line in enumerate(lines[1:]):
                row = [0] + list(map(int, line.split())) + [0]
                if len(row) != w + 2:
                    raise ValueError(f"Line {i+1} in the file does not have {w} integers.")
                landscape[i+1] = row

            return landscape

        except (IOError, FileNotFoundError):
            raise RuntimeError(f"Error opening file: {landscape_file}")
        except ValueError as ve:
            raise RuntimeError(f"Error loading landscape file: {ve}")

    def calculate_neighbours(self):
        """
        Calculates the number of habitable neighbours for each cell in the landscape.

        Returns:
        np.array: 2D numpy array where each cell contains the number of habitable neighbours.
        """
        kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        neighbours = convolve2d(self.landscape, kernel, mode='same', boundary='wrap')
        print(neighbours)
        return neighbours

    def __repr__(self):
        """
        Returns a string representation of the Landscape object.

        Returns:
        str: String representation of the Landscape object.
        """
        return f"<Landscape shape={self.landscape.shape}>"
    
    @property
    def land_squares(self):
        """
        Returns the number of land squares in the landscape.

        Returns:
        int: The number of land squares in the landscape.
        """
        return np.count_nonzero(self.landscape)
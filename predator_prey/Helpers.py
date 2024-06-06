
import numpy as np

class SimulationHelpers(object):


    def getVersion(self):
        """
        Retrieve the current version of the simulation.

        Returns:
            float: The current version number.
        """
        return 3.0
    

    def log_averages(self, i, step, mice_avg, fox_avg):

        """
        Logs the average values for each timestep.

        Args:
        i (int): The current timestep.
        step (float): The current time in seconds.
        mice_avg (float): The average number of mice.
        fox_avg (float): The average number of foxes.

        """

        print("Averages. Timestep: {} Time (s): {:.1f} Mice: {:.17f} Foxes: {:.17f}".format(i, step, mice_avg, fox_avg))

    
    def calculate_color_codes(self, mice, fox, mm, mf, lscape):
        """
        Calculate the color codes based on the mouse and fox populations in each cell of the landscape.

        Args:
            mice (numpy.ndarray): A 2D array representing the number of mice in each cell.
            fox (numpy.ndarray): A 2D array representing the number of foxes in each cell.
            mm (float): The maximum number of mice, used for normalizing the mouse color code.
            mf (float): The maximum number of foxes, used for normalizing the fox color code.
            lscape (numpy.ndarray): A 2D array representing the landscape. Non-zero values indicate cells where animals can live.

        Returns:
            mcols (numpy.ndarray): A 2D array representing the mouse color codes for each cell.
            fcols (numpy.ndarray): A 2D array representing the fox color codes for each cell.
        """
        h, w = lscape.shape[0] - 2, lscape.shape[1] - 2
        mcols = np.zeros((h, w), int)
        fcols = np.zeros((h, w), int)

        for x in range(1, h+1):
            for y in range(1, w+1):
                if lscape[x, y]:
                    mcol = (mice[x, y] / mm) * 255 if mm != 0 else 0
                    fcol = (fox[x, y] / mf) * 255 if mf != 0 else 0
                    mcols[x-1, y-1] = mcol
                    fcols[x-1, y-1] = fcol
        
        return mcols, fcols

    def write_population_map(self, i, mice, fox, mm, mf, lscape):
        """
        Writes the population data of mice and foxes on a landscape to a PPM image file.

        The function creates color codes based on the mouse and fox populations in each cell of the landscape. 
        These color codes are then written to a PPM file, where each pixel corresponds to a cell in the landscape. 
        The color code for each pixel is determined by the number of mice and foxes in the corresponding cell.

        Args:
            i (int): The current timestep, used in the filename of the output PPM file.
            mice (numpy.ndarray): A 2D array representing the number of mice in each cell.
            fox (numpy.ndarray): A 2D array representing the number of foxes in each cell.
            mm (float): The maximum number of mice, used for normalizing the mouse color code.
            mf (float): The maximum number of foxes, used for normalizing the fox color code.
            lscape (numpy.ndarray): A 2D array representing the landscape. Non-zero values indicate cells where animals can live.

        Outputs:
            A PPM file named "map_{i:04d}.ppm" where `i` is the current timestep. The PPM file visualizes the populations of mice and foxes on the landscape.
            Each pixel's RGB values are determined by the number of foxes (R), mice (G), and a fixed zero value (B).
            Cells where animals cannot live are colored with a fixed RGB value (0, 200, 255).
        """
        mcols, fcols = self.calculate_color_codes(mice, fox, mm, mf, lscape)
        
        h, w = lscape.shape[0] - 2, lscape.shape[1] - 2

        with open("map_{:04d}.ppm".format(i), "w") as f:
            hdr = "P3\n{} {}\n{}\n".format(w, h, 255)
            f.write(hdr)
            for x in range(0, h):
                for y in range(0, w):
                    if lscape[x+1, y+1]:
                        f.write("{} {} {}\n".format(fcols[x, y], mcols[x, y], 0))
                    else:
                        f.write("{} {} {}\n".format(0, 200, 255))
    


    def write_avg_file(self, filename, timestep, time, mice, foxes):

        """
        Writes the average values for each timestep to a file.

        Args:
            timestep (int): The current timestep.
            time (float): The current time in seconds.
            mice (float): The average number of mice.
            foxes (float): The average number of foxes.
        """
     
        with open(filename,"a") as f:
            f.write("{},{:.1f},{:.17f},{:.17f}\n".format(timestep,time,mice,foxes))


    def validate_log_interval(self, log_interval, duration):
        """
        Validate the logging interval.

        Args:
            log_interval (int): The interval at which the simulation state is logged.
            duration (int): The total duration of the simulation.

        Raises:
            ValueError: If log_interval is more than duration or less than 0.
        """
        if log_interval > duration:
            raise ValueError("Time Step can't be more than the duration")
        elif log_interval < 0:
            raise ValueError("Time Step can't be less than 0")
        
    def validate_duration(self, duration):
        """
        Validate the total duration of the simulation.

        Args:
            duration (int): The total duration of the simulation.

        Raises:
            ValueError: If duration is less than or equal to 0.
        """
        if duration <= 0:
            raise ValueError("Duration can't be less than or equal to 0")

    def validate_delta(self, delta):
        """
        Validate the delta value.

        Args:
            delta (float): The change in value over a single time step in the simulation.

        Returns:
            float: The validated delta.

        Raises:
            ValueError: If delta is not between 0 and 1.
        """
        if 0 <= delta <= 1:
            return delta
        else:
            raise ValueError("Delta must be between 0 and 1.")
'''Predator-prey simulation. Foxes and mice.

Version 3.0, last updated in September 2023.
'''
from argparse import ArgumentParser
import numpy as np
from .Landscape import Landscape
from .Animal import Fox, Mice
from .Simulation import Simulation
from .Helpers import SimulationHelpers


def simCommLineIntf():
    """
    The command-line interface for the simulation, setting up the parameters for the simulation.
    """
    par=ArgumentParser()
    par.add_argument("-r","--birth-mice",type=float,default=0.1,help="Birth rate of mice")
    par.add_argument("-a","--death-mice",type=float,default=0.05,help="Rate at which foxes eat mice")
    par.add_argument("-k","--diffusion-mice",type=float,default=0.2,help="Diffusion rate of mice")
    par.add_argument("-b","--birth-foxes",type=float,default=0.03,help="Birth rate of foxes")
    par.add_argument("-m","--death-foxes",type=float,default=0.09,help="Rate at which foxes starve")
    par.add_argument("-l","--diffusion-foxes",type=float,default=0.2,help="Diffusion rate of foxes")
    par.add_argument("-dt","--delta-t",type=float,default=0.5,help="Time step size")
    par.add_argument("-t","--time_step",type=int,default=10,help="Number of time steps at which to output files")
    par.add_argument("-d","--duration",type=int,default=500,help="Time to run the simulation (in timesteps)")
    par.add_argument("-f","--landscape-file",type=str,required=True,
                        help="Input landscape file")
    par.add_argument("-ms","--mouse-seed",type=int,default=1,help="Random seed for initialising mouse densities")
    par.add_argument("-fs","--fox-seed",type=int,default=1,help="Random seed for initialising fox densities")
    # Parsing arguments
    args=par.parse_args()
    # Running the simulation with arguments
    sim(args.birth_mice,args.death_mice,args.diffusion_mice,args.birth_foxes,args.death_foxes,args.diffusion_foxes,args.delta_t,args.time_step,args.duration,args.landscape_file,args.mouse_seed,args.fox_seed)


def sim(r,a,k,b,m,l,dt,t,d,lfile,mseed,fseed):
    """
    The main function for running the simulation based on parsed arguments.
    """
    helper = SimulationHelpers()

    # Validating simulation parameters
    helper.validate_delta(dt)
    helper.validate_duration(d)
    helper.validate_log_interval(t, d)
    
    # Setting up parameters for simulation
    parameters = {"mice birth rate": r, "mice death rate": a, "mice diffusion": k, "fox birth rate": b,
                  "fox death rate": m, "fox diffusion": l, "time step": dt, "print interval": t, "duration": d, 
                  "landscape file": lfile, "mice seed": mseed, "fox seed": fseed}

    # Load the landscape from the given file and calculate the number of land cells
    landscape = Landscape(parameters["landscape file"])

    # Initialize mice and fox populations from the given seed files and parameters
    mice = Mice(parameters["mice seed"], parameters["mice diffusion"], parameters["mice birth rate"], parameters["mice death rate"], landscape)
    fox = Fox(parameters["fox seed"], parameters["fox diffusion"], parameters["fox birth rate"], parameters["fox death rate"], landscape)
    predator_prey = Simulation(mice, fox, landscape, parameters["time step"])
    
    total_time_steps = int(parameters["duration"] / parameters["time step"])
    helper.log_averages(0, 0, predator_prey.get_mice_avg, predator_prey.get_fox_avg)

    with open("averages.csv","w") as f:
        hdr="Timestep,Time,Mice,Foxes\n"
        f.write(hdr)

    # Loop over each time step
    for i in range(0, total_time_steps):
        if not i % parameters["print interval"]:
            helper.write_avg_file("averages.csv", i, i * parameters["time step"], predator_prey.get_mice_avg, predator_prey.get_fox_avg)
            helper.log_averages(i, i * parameters["time step"], predator_prey.get_mice_avg, predator_prey.get_fox_avg)
            helper.write_population_map(i, mice.population, fox.population, predator_prey.get_mice_max, predator_prey.get_fox_max, landscape.landscape)

        predator_prey.run()


if __name__ == "__main__":
    simCommLineIntf()
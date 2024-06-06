# MSc Programming Skills Python predator-prey simulation

## Requirements

* Python 3.x
* [numpy](https://numpy.org/)
* [scipy](https://scipy.org/)
* 

To get Python 3 on Cirrus, run:

```console
$ module load anaconda/python3
```

The Anaconda Python distribution includes numpy and many other useful Python packages.

---

## Usage

To see help:

```console
$ python3 -m predator_prey.simulate_predator_prey -h
```

To run the simulation:

```console
$ python -m predator_prey.simulate_predator_prey \
    [-r BIRTH_MICE] [-a DEATH_MICE] \
    [-k DIFFUSION_MICE] [-b BIRTH_FOXES] \
    [-m DEATH_FOXES] [-l DIFFUSION_FOXES] \
    [-dt DELTA_T] [-t TIME_STEP] [-d DURATION] \
    -f LANDSCAPE_FILE [-ms MOUSE_SEED] \
    [-fs FOX_SEED]
```

(where `\` denotes a line continuation character)

For example, to run using map.dat with default values for the other parameters:

```console
$ python -m predator_prey.simulate_predator_prey -f map.dat
```

### Command-line parameters

| Flag | Parameter | Description | Default Value |
| ---- | --------- |------------ | ------------- |
| -h | --help | Show help message and exit | - |
| -r | --birth-mice | Birth rate of mice | 0.08 |
| -a | --death-mice | Rate at which foxes eat mice | 0.04 |
| -k | --diffusion-mice | Diffusion rate of mice | 0.2 |
| -b | --birth-foxes | Birth rate of foxes | 0.02 |
| -m | --death-foxes  | Rate at which foxes starve | 0.06 |
| -l | --diffusion-foxes | Diffusion rate of foxes | 0.2 |
| -dt | --delta-t | Time step size (seconds) | 0.4 |
| -t | --time_step | Number of time steps at which to output files | 10 |
| -d | --duration  | Time to run the simulation (seconds) | 500 |
| -f | --landscape-file | Input landscape file | - |
| -ms | --mouse-seed | Random seed for initialising mouse densities. If 0 then the density in each square will be 0, else each square's density will be set to a random value between 0.0 and 5.0 | 1 |
| -fs | --fox-seed | Random seed for initialising fox densities. If 0 then the density in each square will be 0, else each square's density will be set to a random value between 0.0 and 5.0 | 1 |

### Input files

Map files are expected to be plain-text files of form:

* One line giving Nx, the number of columns, and Ny, the number of rows
* Ny lines, each consisting of a sequence of Nx space-separated ones and zeros (land=1, water=0).

For example:

```
7 7
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 0 1 1
1 1 1 1 0 0 1
1 1 1 0 0 0 0
1 1 1 0 0 0 0
1 0 0 0 0 0 0
```

### PPM output files

"Plain PPM" image files are output every `TIME_STEP` timesteps.  These files are named `map_<NNNN>.ppm` and are a visualisation of the density of mice and foxes and water-only squares.

These files do not include the halo as the use of a halo is an implementation detail.

These files are plain-text so you can view them as you would any plain-text file e.g.:

```console
$ cat map<NNNN>.ppm
```

PPM files can be viewed graphically using ImageMagick commands as follows.

Cirrus users will need first need to run:

```console
$ module load ImageMagick
```

To view a PPM file, run:

```console
$ display map<NNNN>.ppm
```

To animate a series of PPM files:

```console
$ animate map*.ppm
```

For more information on the PPM file format, run `man ppm` or see [ppm](http://netpbm.sourceforge.net/doc/ppm.html).

### CSV averages output file

A plain-text comma-separated values file, `averages.csv`, has the average density of mice and foxes (across the land-only squares) calculated every `TIME_STEP` timesteps. The file has four columns and a header row:

```csv
Timestep,Time,Mice,Foxes
```

where:

* `Timestep`: timestep from 0 .. `DURATION` / `DELTA_T`
* `Time`: time in seconds from 0 .. `DURATION`
* `Mice`: average density of mice.
* `Foxes`: average density of foxes.

This file is plain-text so you can view it as you would any plain-text file e.g.:

```console
$ cat averages.csv
```

---

## Running automated tests

There are several automated tests for each module in the directory.

### Unit Tests

To run the unit tests for the Animal module

```console
$ python3 -m tests.unit_tests.test_animal_model
```

To run the unit tests for the Helpers module

```console
$ python3 -m tests.unit_tests.test_helpers
```

To run the unit tests for the Landscape module

```console
$ python3 -m tests.unit_tests.test_landscape
```

To run the unit tests for the Simulation module

```console
$ python3 -m tests.unit_tests.test_simulation
```

### Integration Tests

To run the Integration tests

```console
$ python3 -m tests.integration_tests.test_integration
```
---


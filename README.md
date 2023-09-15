# Computer System Analysis M/M/1/Q Simulator
Simulation of a M/M/1/Q in python


## Usage:


```bash
usage: argmark [-h] [-n N] [-l L] [-u U] [-t] [-i I] [-c C] [-f]

```
## Arguments

|short|long|default|help|
| :--- | :--- | :--- | :--- |
|`-h`|`--help`||show this help message and exit|
|`-N`||`0`|Select the number of arrivals to simulate|
|`-L`||`1.0`|Add a custom lambda for exponential distribution for interarrival times|
|`-U`||`1.0`|Add a custom mu for exponential distribution for service times|
|`-T`||`False`|Load events from example|
|`-I`||`1`|Select the number of runs for the simulation|
|`-C`||`0.95`|Select the confidence interval for generated results|
|`-F`||`False`|Print on file|



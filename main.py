import argparse
from sim import Server

parser = argparse.ArgumentParser(description="Simulation of a M/M/1/Q")



# parser.add_argument("-g", help="Show graphs at the end of simulation", action="store_true")
parser.add_argument("-n", help="Number of arrivals to simulate", default=0, type=int)
parser.add_argument("-l", help="Custom lambda for exponential distribution (interarrivals)", default=1.0, type=float)
parser.add_argument("-u", help="Custom mu for exponential distribution (service times)", default=1.0, type=float)
# parser.add_argument("-f", help="Log simulation results to file rather than stdout")
parser.add_argument("-t", help="Preload events from example", default=False, type=bool)
parser.add_argument("-i", help="Number of runs for the simulation", default=1, type=int)
parser.add_argument("-c", help="Confidence interval for generated results", default=0.95, type=float)


args = parser.parse_args()

simulation = Server(args.l, args.u)
if (args.i):
    for i in range(args.i):
        simulation.run(args.n)

if (args.t):
    simulation.run(args.i,args.t)
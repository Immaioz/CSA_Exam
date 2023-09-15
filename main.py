import argparse
from sim import Server

parser = argparse.ArgumentParser(description="Simulation of a M/M/1/Q in python")



# parser.add_argument("-g", help="Show graphs at the end of simulation", action="store_true")
parser.add_argument("-n", "-N",help="Select the number of arrivals to simulate", default=0, type=int)
parser.add_argument("-l", "-L", help="Add a custom lambda for exponential distribution for interarrival times", default=1.0, type=float)
parser.add_argument("-u", "-U", help="Add a custom mu for exponential distribution for service times", default=1.0, type=float)
parser.add_argument("-t", "-T", help="Load events from example", action='store_true')
parser.add_argument("-i", "-I", help="Select the number of runs for the simulation", default=1, type=int)
parser.add_argument("-c", "-C", help="Select the confidence interval for generated results", default=0.95, type=float)
parser.add_argument("-f", "-F", help="Print on file", action='store_true')


args = parser.parse_args()

simulation = Server(args.l, args.u)
if (args.i or args.n):
    for i in range(args.i):
        simulation.run(max_arrival= args.n, test = args.t, print_file=args.f)
else:
    simulation.run(max_arrival= args.n, test = args.t, print_file=args.f)
import argparse
from sim import Server
import numpy as np
import scipy.stats as st

parser = argparse.ArgumentParser(description="Simulation of a M/M/1/Q in python")

q_lenght = []
avg_time = []
utilization_rate = []

parser.add_argument("-n", "-N",help="Select the number of arrivals to simulate", default=5, type=int)
parser.add_argument("-l", "-L", help="Add a custom lambda for exponential distribution for interarrival times", default=1.0, type=float)
parser.add_argument("-u", "-U", help="Add a custom mu for exponential distribution for service times", default=1.0, type=float)
parser.add_argument("-t", "-T", help="Load events from example", action='store_true', default=False)
parser.add_argument("-i", "-I", help="Select the number of runs for the simulation", default=1, type=int)
parser.add_argument("-c", "-C", help="Select the confidence interval for generated results", default=0.95, type=float)
parser.add_argument("-f", "-F", help="Print on file", action='store_true', default=False) 


args = parser.parse_args()

simulation = Server(args.l, args.u)
if (args.i or args.n):
    for i in range(args.i):
        q, time, util = simulation.run(max_arrival= args.n, test = args.t, print_file=args.f)
        q_lenght.append(q)
        avg_time.append(time)
        utilization_rate.append(util)
    if args.c :

        queue_len_conf = st.t.interval(args.c, df=len(q_lenght)-1, loc=np.mean(q_lenght), scale=st.sem(q_lenght))
        waiting_time_conf = st.t.interval(args.c, df=len(avg_time)-1, loc=np.mean(avg_time), scale=st.sem(avg_time))
        utilization_rate_conf = st.t.interval(args.c, df=len(utilization_rate)-1, loc=np.mean(utilization_rate), scale=st.sem(utilization_rate))

else:
    q_lenght, avg_time, util_rate = simulation.run(max_arrival= args.n, test = args.t, print_file=args.f)


if args.c:
    print(f"Confidence level {args.c}")
    print(f"Average waiting time: {waiting_time_conf[0]}; Confidence interval: {waiting_time_conf[1]}")
    print(f"Utilization rate: {utilization_rate_conf[0]}; Confidence interval: {utilization_rate_conf[1]}")
    print(f"Expected queue lenght: {queue_len_conf[0]}; Confidence interval: {queue_len_conf[1]}")
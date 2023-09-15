import argparse
from sim import Server
import numpy as np
import scipy.stats as st

parser = argparse.ArgumentParser(description="Simulation of a M/M/1/Q in python")

q_l = []
avg_tm = []
util = []

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
        q_lenght, avg_time, util_rate = simulation.run(max_arrival= args.n, test = args.t, print_file=args.f)
        q_l.append(q_lenght)
        avg_tm.append(avg_time)
        util.append(util_rate)
        if args.c :

            queue_len_conf = st.t.interval(args.c, df=len(q_l)-1, loc=np.mean(q_l), scale=st.sem(q_l))
            waiting_time_conf = st.t.interval(args.c, df=len(avg_tm)-1, loc=np.mean(avg_tm), scale=st.sem(avg_tm))
            utilization_rate_conf = st.t.interval(args.c, df=len(avg_tm)-1, loc=np.mean(util), scale=st.sem(util))

else:
    q_lenght, avg_time, util_rate = simulation.run(max_arrival= args.n, test = args.t, print_file=args.f)


if args.c:
    print(f"Confidence level {args.c}")
    print(f"Average time wait: {waiting_time_conf[0]}. Confidence interval: {waiting_time_conf[1]}")
    print(f"Utilization rate: {utilization_rate_conf[0]}. Confidence interval: {utilization_rate_conf[1]}")
    print(f"Expected queue lenght: {queue_len_conf[0]}. Confidence interval: {queue_len_conf[1]}")
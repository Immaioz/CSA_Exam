import numpy as np
from bisect import insort
import statistics
from Event import event
import sys

class Server:
    ARRIVAL = "arrival"
    DEPARTURE = "departure"

    def __init__(self, scale_lambda=1, scale_mu=1):
        self._lambda = scale_lambda
        self._mu = scale_mu
    
    def run(self, max_arrival=0, test = False, print_file=False):
        self._instance()
        self._maximum_events = max_arrival
        file_path = "output.txt"
        if test:
            self._test_data()
        while (True):
            if(self._maximum_events==0):
                break
            else:
                if(self._maximum_events>0 and self._time == 0):
                    self._total_events +=1
                    if not test:
                        self._genArrival()

                if(self._EventList):
                    e = self._EventList.pop(0)
                    self._total_events +=1
                    self._EventHandler(e)
                    self._update_T(e)

                if(e.event_type == self.ARRIVAL and self._customers < self._maximum_events):
                    if not test:
                        self._genArrival()

                if not self._EventList:
                    break

        if (self._maximum_events >= 2):
            q_lenght, avg_time, util_rate = self._calculate_statistics()
            #print("Total Arrivals: ", self._customers)
            if print_file:
                file = open(file_path, "a")
            else:
                file= sys.stdout
            print("calendar: \n", file=file)
            print(self._calendar, file=file)
            for i in range(len(self._theta)):
                print("Thetha ", i ," = ", self._theta[i], file=file)
            for i in range(len(self._T)):
                print("T(", i ,") = ", self._T[i], file=file)
            print("Expected queue lenght =", q_lenght, file=file)
            print("Average waiting time =", avg_time, file=file)
            print("Utilization rate =", util_rate, file=file)
            return q_lenght, avg_time, util_rate
        if print_file:
            file.close()

    def _calculate_statistics(self):
        expected_q_lenght = []
        avg_waiting_time = []
        utilization_rate = []
        aux = 0
        for index in range (len(self._T)):
            aux += index * self._T[index]
        expected_q_lenght.append(aux / self._time)
        avg_waiting_time.append(np.mean(self._theta))
        utilization_rate.append(1 - (self._T[0]/self._time))

        return expected_q_lenght[0], avg_waiting_time[0], utilization_rate[0]


    def _genArrival(self):
            self._customers +=1
            ia_time = np.random.exponential(scale = self._lambda)
            arrival = self._time + ia_time
            sv_time = np.random.exponential(scale = self._mu)
            e = event(self._customers, arrival, self.ARRIVAL , arrival, sv_time, ia_time)
            insort(self._EventList, e)

    def _EventHandler(self, e):
        self._time = e.event_time
        #print("Time: ", self._time)
        #Gestisco arrival
        if(e.event_type == self.ARRIVAL):
            if(not self._busy):
                a = event(e.id, e.arrival_time, self.ARRIVAL, e.arrival_time, e.service_time, e.interarrival_time)
                #print("Inserisco nel calendario l'evento ", a.event_type, "del processo con id ", a.id)
                insort(self._calendar, a)
                self._busy = True
                d = event(e.id, e.event_time + e.service_time, self.DEPARTURE, e.arrival_time, e.service_time, e.interarrival_time)
                insort(self._EventList,d)

                #schedulo departure e aggiorno timer
            else:
                self._waiting_queue.append(e)
                #aggiungo alla coda e aggiorno timer

        #Gestisco Departure
        else:
            d = event(e.id, e.event_time, self.DEPARTURE, e.arrival_time, e.service_time, e.interarrival_time)
            #print("Inserisco nel calendario l'evento ", d.event_type, "del processo con id ", d.id)
            insort(self._calendar, d)

            self._update_Theta(d)

            if(not self._waiting_queue):
                self._busy = False
            else:
                self._busy = False
                e = self._waiting_queue.pop(0)
                customer = event(e.id, self._time, self.ARRIVAL, e.arrival_time, e.service_time, e.interarrival_time)
                self._EventHandler(customer)


    def _update_Theta(self, d):
        thetha_n = d.id -1
        if thetha_n == -1:
            thetha_n = 0

        self._theta.insert(thetha_n, d.event_time - d.arrival_time)

    def _update_T(self,e):
        index = len(self._waiting_queue)

        if(self._busy == True): 
            index += 1
        
        if(e.event_type == self.ARRIVAL):
            index -= 1
        else:
            index += 1

        T_time = self._time - self._last_event
        self._last_event = self._time

        if index < len(self._T):
            self._T[index] +=  T_time
        else:   
            self._T.insert(index, T_time)


    def _test_data(self):
        e = event(1, 0, self.ARRIVAL , 0, 3, 0) #1 0 0 3
        insort(self._EventList, e)
        e = event(2, 2, self.ARRIVAL , 2, 2, 2) #2 2 2 2
        insort(self._EventList, e)
        e = event(3, 6, self.ARRIVAL , 6, 3, 4) #2 2 2 2
        insort(self._EventList, e)
        e = event(4, 7, self.ARRIVAL , 7, 4, 1) #2 2 2 2
        insort(self._EventList, e)
        e = event(5, 8, self.ARRIVAL , 8, 2, 1) #2 2 2 2
        insort(self._EventList, e)    

    def _instance(self):
        self._time = 0
        self._busy = False
        self._customers = 0
        self._total_events = 0
        self._maximum_events = 0
        self._EventList = []
        self._waiting_queue = []
        self._calendar = []
        self._theta = []
        self._T = []
        self._last_event = 0


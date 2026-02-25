import sys
import csv
from copy import deepcopy

class Process:
    def __init__(self, pid, arrivalTime, burstTime):
        self.pid = int(pid)
        self.arrivalTime = int(arrivalTime)
        self.burstTime = int(burstTime)
        self.remainingTime = int(burstTime)
        self.completionTime = None

#Helper Method
#Used to format and get final values for gantt chart
def make_gantt(schedular_type, processes, gantt):
    process_list = sorted(processes, key=lambda p: p.pid)
    num_processes =len(process_list)

    waiting_times = []
    turnAround_times = []
    #calculates each processes Turn Around and Wait times and adds to list 
    for p in process_list:
        curr_TAT = p.completionTime - p.arrivalTime
        turnAround_times.append(curr_TAT)
        curr_WT = curr_TAT - p.burstTime
        waiting_times.append(curr_WT)

    avg_WT = sum(waiting_times) / num_processes
    avg_TAT = sum(turnAround_times) / num_processes
    total_Time = gantt[-1][2]
    total_ThroughPut = num_processes / total_Time

    print("Process ID", " ".join(str(p.pid) for p in process_list))
    print("Waiting Time", " ".join(str(wait)for wait in waiting_times))
    print("Turnaround Time", " ".join(str(time)for time in turnAround_times))
    print()
    print(schedular_type + " Gantt Chart")

    for i in range(0, len(gantt)):
        print(f"[{gantt[i][0]}]--{gantt[i][1]}--[{gantt[i][2]}]")
    
    print()
    if(schedular_type == "Round Robin"):
        print(f"Average Waiting Time: {avg_WT:.2f}")
        print(f"Average Turnaround Time: {avg_TAT:.2f}")
    else:
        print(f"Average Waiting Time: {float(avg_WT)}")
        print(f"Average Turnaround Time: {float(avg_TAT)}")
    print(f"Throughput: {total_ThroughPut}")
    print()

#Helper method
#Gets processes that arrive at *time* and returns sorted list by burstTime then PID
def get_arrivalTimes(time, notArrived):
    arrivalTimes = [p for p in notArrived if p.arrivalTime == time]
    arrivalTimes.sort(key=lambda p: (p.burstTime, p.pid))
    return arrivalTimes

#read data from csv and adding new Process objects to list, Processes contain: PID, ArrivalTime, BurstTime
def process_inputFile(filePath):
    processes = []
    with open(filePath, newline='') as inputFile:
        read = csv.DictReader(inputFile)

        for row in read:
            pid = int(row["ProcessID"])
            arrivalTime = int(row["Arrival Time"])
            burstTime = int(row["Burst Time"])

            processes.append(Process(pid, arrivalTime, burstTime))
        return processes
    
def FCFS(processes):
    #deepcopy() to ensure copying objects in process list, prevents altering initial objects/values
    processesFCFS = deepcopy(processes)
    #sorted list by arrivaltime -> burst -> pid in that order (takes care of equal values)
    notArrived = sorted(processesFCFS, key=lambda p: (p.arrivalTime, p.burstTime, p.pid))
    readyQ = []
    time = 0
    ganttChartFCFS = []

    while len(notArrived) > 0 or len(readyQ) > 0:
        #get newly arrived processes
        arrived = get_arrivalTimes(time, notArrived)
        for process in arrived:
            readyQ.append(process)
            notArrived.remove(process)
        #nothing is ready at current time, CPU is IDLE
        if (not readyQ):
            next_processTime = min(p.arrivalTime for p in notArrived)
            ganttChartFCFS.append((time, "IDLE", next_processTime))
            time = next_processTime
            continue
        
        #gets next process to run based on arrival time
        readyProcess = readyQ.pop(0)
        startTime = time
        runTime = readyProcess.remainingTime
        time += runTime
        readyProcess.remainingTime = 0
        readyProcess.completionTime = time
        ganttChartFCFS.append((startTime, str(readyProcess.pid), time))

        #if a process arrived during (execution of current process + 1 -> current time) add it to readyQ and remove from notArrived
        for sec in range(startTime + 1, time + 1):
            new_ArrivedProcesses = get_arrivalTimes(sec, notArrived)
            for p in new_ArrivedProcesses:
                readyQ.append(p)
                notArrived.remove(p)
    
    return processesFCFS, ganttChartFCFS

def SJF_preempt(processes):
    #deepcopy() to ensure copying objects in process list, prevents altering initial objects/values
    processesSJF = deepcopy(processes)
    #sorted list by arrivaltime -> burst -> pid in that order (takes care of equal values)
    notArrived = sorted(processesSJF, key=lambda p: (p.arrivalTime, p.burstTime, p.pid))
    readyQ = []
    time = 0
    ganttChartSJF = []
    curr_running = None
    prev_running = None
    num_processes = len(processesSJF)
    completed = 0

    #loop until all processes have completed
    while completed < num_processes:
        #get processes that arrived at *time* and add to readyQ/remove from notArrived
        arrived = get_arrivalTimes(time, notArrived)
        for p in arrived:
            readyQ.append(p)
            notArrived.remove(p)
        
        #sorts by remainingTime -> pid to ensure the process with least burstTime is in front
        readyQ.sort(key=lambda p: (p.remainingTime, p.pid))

        #if nothing is running and readyQ is NOT empty get the next process
        if curr_running == None:
            if (len(readyQ) > 0):
                curr_running = readyQ.pop(0)
        else:
            #preemption - if readyQ is NOT empty and the next process has less remainingTime than currently running process -> preempt it and re-sort readyQ
            if (len(readyQ) > 0) and (readyQ[0].remainingTime < curr_running.remainingTime):
                readyQ.append(curr_running)
                readyQ.sort(key=lambda p: (p.remainingTime, p.pid))
                curr_running = readyQ.pop(0)
        
        #if there was nothing in readyQ then add IDLE to gantt for current time to time of next process
        if curr_running == None:
            if len(notArrived) > 0:
                next_processTime = min(p.arrivalTime for p in notArrived)
                ganttChartSJF.append((time, "IDLE", next_processTime))
                time = next_processTime
                continue
            elif len(notArrived) == 0:
                break
        
        #if a new process starts, add it to gantt
        # None is a placeholder for when the process finished/gets preempted
        if prev_running != curr_running.pid:
            ganttChartSJF.append((time, str(curr_running.pid), None))
            prev_running = curr_running.pid

        #run the process
        curr_running.remainingTime -= 1
        time += 1

        #if process is done, change gantt chart value to be current time
        if curr_running.remainingTime == 0:
            curr_running.completionTime = time
            completed += 1
            ganttChartSJF[-1] = (ganttChartSJF[-1][0], ganttChartSJF[-1][1], time)
            curr_running = None
            prev_running = None
        #if process is going to continue to run change value in gantt chart
        elif not ((len(readyQ) > 0) and (readyQ[0].remainingTime < curr_running.remainingTime)):
            ganttChartSJF[-1] = (ganttChartSJF[-1][0], ganttChartSJF[-1][1], time)
        
    return processesSJF, ganttChartSJF

def RR(processes, timeQuant):
    #deepcopy() to ensure copying objects in process list, prevents altering initial objects/values
    processesRR = deepcopy(processes)
    #sorted list by arrivaltime -> burst -> pid in that order (takes care of equal values)
    notArrived = sorted(processesRR, key=lambda p: (p.arrivalTime, p.burstTime, p.pid))
    readyQ = []
    ganttChartRR = []
    time = 0

    #get first process(es) and add to readyQ/remove from notArrived
    arrived = get_arrivalTimes(time, notArrived)
    for p in arrived:
        readyQ.append(p)
        notArrived.remove(p)

    #while there is at least 1 process in notArrived/readyQ run the process
    while len(notArrived) > 0 or len(readyQ) > 0:
        #if readyQ is empty find the next process(es) and add IDLE to gantt
        if len(readyQ) == 0:
            next_processTime = min(p.arrivalTime for p in notArrived)
            ganttChartRR.append((time, "IDLE", next_processTime))
            time = next_processTime
            arrived = get_arrivalTimes(time, notArrived)
            for p in arrived:
                readyQ.append(p)
                notArrived.remove(p)
            continue

        #actually run the process for timeQuant/remaining time, whichever is less and add to gantt
        curr_process = readyQ.pop(0)
        startTime = time
        run_Time = min(timeQuant, curr_process.remainingTime)
        time += run_Time
        curr_process.remainingTime -= run_Time
        ganttChartRR.append((startTime, str(curr_process.pid), time))

        #if a process arrived during (execution of current process + 1 -> current time) add it to readyQ and remove from notArrived, before adding the current process back to readyQ
        for t in range(startTime + 1, time + 1):
            arrived_now = get_arrivalTimes(t, notArrived)
            for p in arrived_now:
                readyQ.append(p)
                notArrived.remove(p)

        #if process is NOT done, add it to the end of the readyQ
        if curr_process.remainingTime > 0:
            readyQ.append(curr_process)
        else:
            curr_process.completionTime = time
        
    return processesRR, ganttChartRR


def main():
    if (len(sys.argv) < 3):
        print("Error: program needs 4 args to complete scheduling. Format[python3 schedular.py *inputFile*.csv *timeQuantum*]")
        sys.exit(1)
    
    processFile = sys.argv[1]
    try:
        timeQuant = int(sys.argv[2])
    except ValueError:
        print("Time Quantum needs to be an integer")
        sys.exit(1)

    processes = process_inputFile(processFile)
    if len(processes) == 0:
        print("CSV file is empty/Error with CSV reader")
        sys.exit(1)

    #gets final list of processes with newly added values for completion time to calculate turnaround and wait times
    FCFS_processes, ganttFCFS = FCFS(processes)
    print("_______________FCFS_______________")
    #prints gantt and other values for wait and turnaround times (avg and /process)
    make_gantt("FCFS", FCFS_processes, ganttFCFS)

    #gets final list of processes with newly added values for completion time to calculate turnaround and wait times
    SJF_processes, ganttSJF = SJF_preempt(processes)
    print("___Shortest Job First with Preemption____")
    #prints gantt and other values for wait and turnaround times (avg and /process)
    make_gantt("Shortest Job First with Preemption", SJF_processes, ganttSJF)

    #gets final list of processes with newly added values for completion time to calculate turnaround and wait times
    RR_processes, ganttRR = RR(processes, timeQuant)
    print("___________Round Robin___________")
    #prints gantt and other values for wait and turnaround times (avg and /process)
    make_gantt("Round Robin", RR_processes, ganttRR)
    

if __name__ == "__main__":
    main()
    
# CPU Scheduling Simulator
A Python-based CPU scheduling simulator that implements and compares three classic scheduling algorithms:
* First Come First Server (FCFS)
* Shortest Job First (Preemptive)
* Round Robin (RR)
The program reads process data from a CSV file and outputs:
* Waiting Time (per process)
* Turnaround Time (per process)
* Average Waiting Time
* Average Turnaround Time
* Throughput
* Gantt Chart visualization (text-based)
# Features
* Supports multiple scheduling algorithms in one run
* Handles CPU idle periods
* Calculates detailed performance metrics
* Displays formatted Gantt Charts
* Uses deep copies to preserve original process data
# Project Structure
* schedular.py -> Main program
  - Process class -> Represents each process
  - FCFS() -> First Come First Serve algorithm
  - SJF_preempt() -> Shortest Job First (Preemptive) algorithm
  - RR() -> Round Robin scheduling algorithm
  - make_gantt() -> Calculates statistics & prints results
# Input File Format (CSV)
The program expects a CSV file with the following headers:

ProcessID,Arrival Time,Burst Time\
1,0,5\
2,1,3\
3,2,8

#Column Definitions
| Column Name | Description |
| ProcessID | Unquie process ID |
| Burst Time | Total CPU execution time required |

# How to Run
`python3 schedular.py <inputFile>.csv <timeQuantum>` 

Example: 
`python3 schedular.py processes.csv 2` 
* Processes.csv -> Input file
* 2 -> Time Quantum (used only for Round Robin)

# Implemented Algorithms
1. First Come First Serve (FCFS)
   * Non-preemptive
   * Executes processes in order of arrival
   * If CPU is idle, program records IDLE time in Gantt Chart
   Characteristics:
    * Simple implementaion
    * Can suffer from convoy effect
    * No starvation
2. Shortest Job First (Preemptive) AKA Shortest Remaining Time First (SRTF)
   * Preemptive algorithm
   * At every time unit, selects process with smallest remaining burst time
   * Preempts current process if a shorter job arrives
   Characteristics
   * Minimizes average waiting time
   * More complex than FCFS
   * Requires continuous checking for new arrivals
3. Round Robin (RR) with time Quantum
   * Preemptive
   * Each process runs for a fixed time quantum
   * If process is not finished, it is added back to the ready queue
   Characteristics:
   * Fair scheduling
   * Prevents starvation
   * Performance depends on time quantum
# Output Format
For each scheduling algorithm, the program prints: 

**Example Output Strucutre**

Process ID 1 2 3 \
Waiting Time 0 4 7 \
Turnaround Time 5 7 15

FCFS Gantt Chart \
[0]--1--[5] \
[5]--2--[8] \
[8]--3--[16]

Average Waiting Time: 3.67 \
Average Turnaround Time: 9.00 \
Throughput: 0.1875

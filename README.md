# CPU-Scheduler
Program takes an input of processes containing the Process ID, Arrival Time, and Burst Time. Outputs a Gantt Chart of when each process "executes".
# scheduler.py
Contains FCFS, SJF(preemption), RR methods for scheduling
    -Helper methods for making the gantt chart, reading from the input .csv, getting newly arrived processes
    -constructor to make Process objects


Comments in code show flow of execution with descriptions for important lines/blocks

# Expected Input:
CSV files (*.csv)

Format:
ProcessID, Arrival Time, Burst Time
1, 0, 10
2, 2, 3
3, 8, 8

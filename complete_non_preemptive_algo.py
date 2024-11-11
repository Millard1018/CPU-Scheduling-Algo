class processes:
    def __init__(self, id, at, bt, ct):
        self.id = id
        self.at = at
        self.bt = bt
        self.ct = ct
        self.tat = self.ct-self.at
        self.wt = self.tat-self.bt

    def display(self):
        print(f"{self.id}\t{self.at}\t{self.bt}\t{self.ct}\t{self.tat}\t{self.wt}")

    def turnaround(self):
        return self.tat

    def waiting(self):
        return self.wt

def user_input():
    num = int(input("Enter the Number of Processes: "))
    print("\n")
    process = []

    for i in range(num):
        print(f'Process {i + 1}')
        at = int(input("Enter the Arrival Time: "))
        bt = int(input("Enter the Burst Time: "))
        process_info = {"id": i + 1, "at": at, "bt": bt}
        process.append(process_info)
        print("\n")
    
    return num, process

def user_input_priority():
    num = int(input("Enter the Number of Processes: "))
    print("\n")
    process = []

    for i in range(num):
        print(f'Process {i + 1}')
        at = int(input("Enter the Arrival Time: "))
        bt = int(input("Enter the Burst Time: "))
        pl = int(input("Enter the Level of Priority: "))
        process_info = {"id": i + 1, "at": at, "bt": bt, "pl": pl}
        process.append(process_info)
        print("\n")
    
    return num, process

def first_come_first_serve_algo(process: list):
    # Sort processes by arrival time
    fcfs_algo = sorted(process, key=lambda x: x["at"])
    return fcfs_algo

def shortest_job_first_algo(process: list):
    # Sort processes by arrival time initially
    sjf_algo = sorted(process, key=lambda x: x["at"])
    
    completed_processes = []  # List to store completed processes with calculated completion times
    current_time = 0  # Start at time 0

    # While True continue until all processes are handled
    while sjf_algo:
        # List of processes that have arrived by current_time
        available_processes = [p for p in sjf_algo if p["at"] <= current_time]

        if available_processes:
            # The process with the smallest burst time from available ones
            shortest_process = min(available_processes, key=lambda x: x["bt"])
            sjf_algo.remove(shortest_process)  # Remove selected process from the original list

            # Calculate the current_time for the selected process
            current_time += shortest_process["bt"]
            completed_processes.append(shortest_process)
        else:
            # If no processes are available, move current_time to the next arrival time
            current_time = sjf_algo[0]["at"]

    return completed_processes
    
def priority_non_preemptive_algo(process: list):
    priority_algo = sorted(process, key=lambda x: x["at"])
    
    completed_processes = []  # List to store completed processes with calculated completion times
    current_time = 0  # Start at time 0
    
    while priority_algo:
        # List of processes that have arrived by current_time
        available_processes = [p for p in priority_algo if p["at"] <= current_time]

        if available_processes:
            # The process with the highest priority from available ones
            priority_process = min(available_processes, key=lambda x: x["pl"])
            priority_algo.remove(priority_process)  # Remove selected process from the original list

            # Calculate current_time for the selected process
            current_time += priority_process["bt"]
            completed_processes.append(priority_process)
        else:
            # If no processes are available, move current_time to the next arrival time
            current_time = priority_algo[0]["at"]

    return completed_processes

def highest_response_ratio_next_algo(process: list):
    hrrn_algo = sorted(process, key=lambda x: x["at"])
    
    completed_processes = []  # List to store completed processes with calculated completion times
    current_time = 0  # Start at time 0
    ct = 0
    
    while hrrn_algo:
        # List of processes that have arrived by current_time
        available_processes = [p for p in hrrn_algo if p["at"] <= current_time]

        if available_processes:
            #Response ratio for available process
            for p in available_processes:
                p["rr"] = ((ct - p["at"])+p["bt"])/p["bt"]
            # The process with the Highest Response Ratio from available ones
            highest_rr = max(available_processes, key=lambda x: x["rr"])
            hrrn_algo.remove(highest_rr)  # Remove selected process from the original list

            # Calculate ct and current_tme for the selected process
            ct += highest_rr["bt"]
            current_time += highest_rr["bt"]
            completed_processes.append(highest_rr)
        else:
            # If no processes are available, move current_time to the next arrival time
            current_time = hrrn_algo[0]["at"]

    return completed_processes

def default(): # No CPU Scheduling algorithm choosen
    print("CPU-Scheduling Algotithm selected is either none of the choices or nothing selected.")
    print("Closing the program.")
    quit()

def cpu_scheduling_algo_type():
    cpu_scheduling_algorithms = {
        "A": first_come_first_serve_algo,
        "B": shortest_job_first_algo,
        "C": priority_non_preemptive_algo,
        "D": highest_response_ratio_next_algo
    }
    option = input("'A' - First Come First Serve\n'B' - Shortest Job First\n'C' - Priority Pre-Emptive\n'D' - Highest Response Ratio Next\nEnter CPU-Scheduling Algorithm: ").upper()
    # User will choose what type of CPU Scheduling
    scheduling_type = cpu_scheduling_algorithms.get(option, None)
    if scheduling_type is priority_non_preemptive_algo: # for preemptive and non_preemptive priority
        num, process = user_input_priority() # process/es user input
        return num, scheduling_type(process) 
    if scheduling_type: # Other CPU Scheduling Algorithm
        num, process = user_input()
        return num, scheduling_type(process)
    else:
        default() # If user enter none or none on the list

def final_calculation(sorted_list: list): # Calculate completion time for each process
    final_process_list = []
    ct = 0
    for i, process in enumerate(sorted_list):
        if i == 0:
            ct = process["bt"] # first process of ct is equal to the burst time
        else:
            ct += process["bt"]  # Adding to the previous ct to the current bt

        # Append Process object to the final list
        final_process_list.append(processes(process["id"], process["at"], process["bt"], ct))

    # Sort the final list by process ID
    final_process_list = sorted(final_process_list, key=lambda x: x.id)
    return final_process_list

def calculate_ave(num: int, l: list):
    avg_tat = 0 # turnaround time and waiting time iniate at 0
    avg_wat = 0
    for process in l:
        avg_tat += process.turnaround()
        avg_wat += process.waiting()
    final_tat: float = (f"{avg_tat/num:.2f}") # average of tat and wat programmed with 2 decimals
    final_wt: float = (f"{avg_wat/num:.2f}")
    return final_tat, final_wt

def display(l: list, final_tat: float, final_wt: float): 
    print("PID\tAT\tBT\tCT\tTAT\tWT") # Display header
    for process in l: # display each user input and calculation
        process.display()
    print(f"Avg_turnaround:{final_tat}\nAvg_Waitingtime:{final_wt}") # display average final_tat and final_wat

def main():
    num, scheduling_type = cpu_scheduling_algo_type() 
    final_process_list = final_calculation(scheduling_type)
    final_tat, final_wt = calculate_ave(num, final_process_list)
    display(final_process_list, final_tat, final_wt)

if __name__ == '__main__':
    main()
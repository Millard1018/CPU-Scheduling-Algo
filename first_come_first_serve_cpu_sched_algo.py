class processes_non_preemptive: #for organization of processes
    def __init__(self, id, at, bt, ct): #parameters
        self.id = id
        self.at = at
        self.bt = bt
        self.ct = ct
        self.tat = self.ct-self.at #turnaround time calculation
        self.wt = self.tat-self.bt #waiting time calculation
    def display_non_preemptive(self): #display each processes for the table
        print(f"P{self.id}\t{self.at}\t{self.bt}\t{self.ct}\t{self.tat}\t{self.wt}")

    def gantt_chart_id(self): #display each unsorted process id for gantt chart
        print(f"    P{self.id}", end="  ")

    def gantt_chart_ct(self):#display each ct completion time for gantt chart
        print(f"\t{self.ct}", end="")

    # Used to get the average tat turnaround time and wt waiting time 
    def turnaround(self):
        return self.tat

    def waiting(self):
        return self.wt
    
def validateInt(validNum, range1, range2): # Error handling in-case of character input
    while True:# While the input is out of range or a charcter
        try: 
            validNum = int(validNum) 
            if validNum < range1 or validNum > range2: # Number inputted was out of range
                print(f"Must be at least {range1} and no more than {range2}.")
                validNum = input("Please enter the number again: ")
            else: # Correct user input
                return validNum
        except ValueError: # Value Error encoutered, a character was inputed
            print("Invalid entry; must be a number without characters!")
            validNum = input("Please enter the number again: ")

def user_input()->None:
    num: int = (input("Enter the Number of Processes: "))
    num = validateInt(num, 2, 100) # Error handling in-case of character input or out-of-range

    print("\n")
    process: list = []
    for i in range(1, num+1):
        print(f'Process {i}')
        at: int= (input("Enter the Arrival Time: ")) # To get Arrival Time
        at = validateInt(at, 0, 100) # Error handling in-case of character input or out-of-range
        bt: int = (input("Enter the Burst Time: ")) # To get Burst tTime
        bt = validateInt(bt, 0, 100) # Error handling in-case of character input or out-of-range
        process_info = {"id": i, "at": at, "bt": bt} # Entry to be appended to the process
        process.append(process_info)
        print("\n")

    return num, process

def first_come_first_serve_algo(process: list):
    # Sort processes by arrival time
    fcfs_algo: list = sorted(process, key=lambda x: x["at"])
    completed_process_list: list = []
    ct: int = 0
    for i, process in enumerate(fcfs_algo):
        if i == 0:
            ct = process["bt"] # first process of ct is equal to the burst time
        else:
            ct += process["bt"]  # Adding to the previous ct to the current bt
        # Append Process object to the final list
        completed_process_list.append(processes_non_preemptive(process["id"], process["at"], process["bt"], ct))

    return completed_process_list

def sorted_processes_list(final_process_list): # Sort the final list by process ID
    sorted_by_id_process = sorted(final_process_list, key=lambda x: x.id)
    return sorted_by_id_process

def calculate_ave(num: int, sorted_by_id_process: list):
    avg_tat: float = 0.0 # turnaround time and waiting time iniate at 0
    avg_wat: float = 0.0
    for process in sorted_by_id_process:
        avg_tat += process.turnaround()
        avg_wat += process.waiting()
    final_tat: float = (f"{avg_tat/num:.2f}") # average of tat and wat programmed with 2 decimals
    final_wt: float = (f"{avg_wat/num:.2f}")
    return final_tat, final_wt

def display_non_preem(l: list, fcfs_algo:list, final_tat: float, final_wt: float):
    # Gannt Chart Output
    print("\nGantt Chart")
    for process in fcfs_algo: # display of each id from the class
        process.gantt_chart_id()

    print("\n0", end="")

    for process in(fcfs_algo): # display of each ct from the class
        process.gantt_chart_ct()

    #Table Output
    print("\n\nPID\tAT\tBT\tCT\tTAT\tWT") # Display header
    for process in l: # display each user input and calculation
        process.display_non_preemptive()
    print(f"\t\t    Average    {final_tat}    {final_wt}") # display average final_tat and final_wt
    print("\nThank you for using the program!")

def main():
    # Every variable was the return of a function and being used for another function
    num, process = user_input()
    completed_process_list = first_come_first_serve_algo(process)
    sorted_by_id_process = sorted_processes_list(completed_process_list)
    final_tat, final_wt = calculate_ave(num, sorted_by_id_process)
    display_non_preem(sorted_by_id_process, completed_process_list, final_tat, final_wt)

if __name__ == "__main__":
    main()
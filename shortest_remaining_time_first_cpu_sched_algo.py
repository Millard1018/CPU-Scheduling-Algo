import copy
class processes_preemptive: # for organization of processes
    def __init__(self, id, at, bt, ct, fs): #parameters
        self.id = id #process id
        self.at = at #process arrival time
        self.bt = bt #process burst time
        self.ct = ct #process completion time
        self.fs = fs #process first seen, first seen is when the first time the process started 
        self.tat = self.ct-self.at #turnaround time calculation
        self.wt = self.tat-self.bt #waiting time calculation
        self.rt = self.fs-self.at #response time calculation

    def display_preemptive(self):
        print(f"{self.id}\t{self.at}\t{self.bt}\t{self.ct}\t{self.tat}\t{self.wt}\t{self.rt}")

    #used to get the average tat, wt and rt
    def turnaround(self):
        return self.tat

    def waiting(self):
        return self.wt
    
    def response(self):
        return self.rt
    
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
    num: int = (input("Enter the Number of Processes: ")) # how many processess
    num = validateInt(num, 0, 100)
    print("\n")
    process: list = []

    for i in range(1, num+1):
        print(f'Process {i}')
        at = (input("Enter the Arrival Time: ")) # To get the arrival time
        at = validateInt(at, 0, 100) # Error handling in-case of character input or out-of-range
        bt = (input("Enter the Burst Time: ")) # To get the burst time
        bt = validateInt(bt, 0, 100) # Error handling in-case of character input or out-of-range
        process_info = {"id": i, "at": at, "bt": bt} # All the process entry
        process.append(process_info) #Appending process entry to process
        print("\n")
    
    return num, process

def shortest_remaining_time_first_algo(process: list)->list:
    srtf_algo = sorted(process, key=lambda x: x["at"]) 
    completed_process = []
    current_time = 0
    first_response_times = {}
    gantt_chart_list = []
    copy_srtf = copy.deepcopy(process)
    copy_srtf = sorted(copy_srtf, key=lambda x: x["at"])

    while srtf_algo:
        available_process = [p for p in srtf_algo if p["at"] <= current_time and p["bt"] > 0]

        if available_process:
            shortest_time = min(available_process, key=lambda x: x["bt"])

            # Condition to get the fs first seen 
            if shortest_time["id"] not in first_response_times: #each process will be validated if it is already in first_respnse_time
                first_response_times[shortest_time["id"]] = current_time # the current time will be the basis if when it was first seen
                shortest_time["fs"] = current_time

            current_time +=1 # current time is incrimented for only 1 sec/min 
            shortest_time["bt"] -= 1 # the bt is dicremented by 1 because it had been processed by 1 only

            # For gantt chart to identify how much time each process was processed
            if not gantt_chart_list or gantt_chart_list[-1]["id"] != shortest_time["id"]:
                gantt_chart_dict = {"id": shortest_time["id"], "ct": current_time}
                gantt_chart_list.append(gantt_chart_dict)
            else:
                gantt_chart_list[-1]["ct"] = current_time

            #if the process has 0 burst time the process will be appended and it has completed its process
            if shortest_time["bt"] == 0:
                fs_id = first_response_times[shortest_time["id"]]
                # Create a new dictionary for the completed process with the original burst time
                completed_entry = {
                    "id": shortest_time["id"],
                    "at": shortest_time["at"],
                    "ct": current_time,  
                    "fs": fs_id
                    }
                completed_process.append(completed_entry) # Appending the completed process
                srtf_algo.remove(shortest_time)  # Remove the completed process from the main list
        else:
            current_time = srtf_algo[0]["at"]

    completed_process_list: list = []
    completed_process = sorted(completed_process, key=lambda x:x["at"])
    for i, p in enumerate(completed_process):
        p["bt"] = copy_srtf[i]["bt"]
        completed_process_list.append(processes_preemptive(p["id"], p["at"], p["bt"], p["ct"], p["fs"]))
                             
    return completed_process_list, gantt_chart_list

def sorted_completed_list(completed_process: list):
    sorted_completed_process = sorted(completed_process, key=lambda x: x.id)
    return sorted_completed_process

def calculate_ave(num: int, sorted_completed_process: list)->list:
    avg_tat = 0 # turnaround time and waiting time iniate at 0
    avg_wt = 0
    avg_rt = 0
    for process in sorted_completed_process:
        avg_tat += process.turnaround()
        avg_wt += process.waiting()
        avg_rt += process.response()
    final_tat: float = (f"{avg_tat/num:.2f}") # average of tat, wt, rt programmed with 2 decimals
    final_wt: float = (f"{avg_wt/num:.2f}")
    final_rt: float = (f"{avg_rt/num:.2f}")
    return final_tat, final_wt, final_rt

def display_preem(sorted_completed_process: list, gantt_chart_list: list, final_tat: float, final_wt: float, final_rt: float)->list: 
    # Gannt Chart Output
    print("\nGantt Chart")
    for i, process in enumerate(gantt_chart_list): # each id from the gantt chart list is displayed
        print(f"    P{gantt_chart_list[i]['id']}", end="  ")

    print("\n0", end="")

    for i, process in enumerate(gantt_chart_list): # each ct from the gantt chart list is displayed
        print(f"\t{gantt_chart_list[i]['ct']}", end="")

    #Table Output
    print("\n\nPID\tAT\tBT\tCT\tTAT\tWT\tRT") # Display header
    for process in sorted_completed_process: # display each user input and calculation
        process.display_preemptive()
    print(f"\t\t    Average    {final_tat}    {final_wt}    {final_rt}") # display average final_tat, final_wt and final_rt
    print("\nThank you for using the program!")

def main()->None:
    # Every variable was the return of the function and being used for another function
    num, process = user_input() 
    completed_process_list, gantt_chart_list = shortest_remaining_time_first_algo(process)
    sorted_completed_process = sorted_completed_list(completed_process_list)
    final_tat, final_wt, final_rt = calculate_ave(num, sorted_completed_process)
    display_preem(sorted_completed_process, gantt_chart_list, final_tat, final_wt, final_rt)

if __name__ == '__main__': # main guard to run only what it is in main
    main()
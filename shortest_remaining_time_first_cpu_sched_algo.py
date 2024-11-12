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

    def gantt_chart_id(self): #display each unsorted process id for gantt chart
        print(f"    P{self.id}", end="  ")

    def gantt_chart_ct(self):#display each ct completion time for gantt chart
        print(f"\t{self.ct}", end="")

    def turnaround(self):
        return self.tat

    def waiting(self):
        return self.wt
    
    def response(self):
        return self.rt
    
def user_input()->None:
    num: int = int(input("Enter the Number of Processes: "))
    print("\n")
    process: list = []

    for i in range(num):
        print(f'Process {i + 1}')
        at = int(input("Enter the Arrival Time: "))
        bt = int(input("Enter the Burst Time: "))
        process_info = {"id": i + 1, "at": at, "bt": bt}
        process.append(process_info)
        print("\n")
    
    return num, process

def shortest_remaining_time_first_algo(process: list):
    srtf_algo = sorted(process, key=lambda x: x["at"])
    completed_process = []
    current_time = 0
    first_response_times = {}
    copy_srtf = copy.deepcopy(process)
    copy_srtf = sorted(copy_srtf, key=lambda x: x["at"])

    while srtf_algo:
        available_process = [p for p in srtf_algo if p["at"] <= current_time and p["bt"] > 0]

        if available_process:
            shortest_time = min(available_process, key=lambda x: x["bt"])
            
            if shortest_time["id"] not in first_response_times:
                first_response_times[shortest_time["id"]] = current_time
                shortest_time["fs"] = current_time

            current_time +=1
            shortest_time["bt"] -= 1
            
            if shortest_time["bt"] == 0:
                fs_id = first_response_times[shortest_time["id"]]
                # Create a new dictionary for the completed process with the original burst time
                completed_entry = {
                    "id": shortest_time["id"],
                    "at": shortest_time["at"],
                    "ct": current_time,  
                    "fs": fs_id
                    }
                completed_process.append(completed_entry)
                srtf_algo.remove(shortest_time)  # Remove the completed process from the main list
        else:
            current_time = srtf_algo[0]["at"]

    completed_process = sorted(completed_process, key=lambda x:x["at"])
    for i, p in enumerate(completed_process):
        p["bt"] = copy_srtf[i]["bt"]
        completed_process.append(processes_preemptive(p["id"], p["at"], p["bt"], p["ct"], p["fs"]))
                             
    return completed_process

def sorted_completed_list(completed_process: list):
    sorted_completed_process = sorted(completed_process, key=lambda x: x.id)
    return sorted_completed_process

def calculate_ave(num: int, sorted_completed_process: list):
    avg_tat = 0 # turnaround time and waiting time iniate at 0
    avg_wt = 0
    for process in sorted_completed_process:
        avg_tat += process.turnaround()
        avg_wt += process.waiting()
        avg_rt += process.response()
    final_tat: float = (f"{avg_tat/num:.2f}") # average of tat, wt, rt programmed with 2 decimals
    final_wt: float = (f"{avg_wt/num:.2f}")
    final_rt: float = (f"{avg_wt/num:.2f}")
    return final_tat, final_wt, final_rt

def display_preem(sorted_completed_process: list, completed_process: list, final_tat: float, final_wt: float, final_rt: float): 
    # Gannt Chart Output
    print("\nGantt Chart")
    for process in completed_process: 
        process.gantt_chart_id()

    print("\n0", end="")

    for process in(completed_process):
        process.gantt_chart_ct()

    #Table Output
    print("PID\tAT\tBT\tCT\tTAT\tWT\tRT") # Display header
    for process in sorted_completed_process: # display each user input and calculation
        process.display_preemptive()
    print(f"\t\t    Average    {final_tat}    {final_wt}    {final_rt}") # display average final_tat, final_wt and final_rt
    print("\nThank you for using the program!")

def main()->None:
    num, process = user_input()
    completed_process = shortest_remaining_time_first_algo(process)
    sorted_completed_process = sorted_completed_list(completed_process)
    final_tat, final_wt, final_rt = calculate_ave(num, sorted_completed_process)
    display_preem(sorted_completed_process, completed_process, final_tat, final_wt, final_rt)

if __name__ == '__main__':
    main()
            if not gantt_chart_list or gantt_chart_list[-1]["id"] != shortest_time["id"]:
            # If the process is new or different from the last one, add a new entry
                gantt_chart_lib = {"id": shortest_time["id"], "ct": current_time}
                gantt_chart_list.append(gantt_chart_lib)
            else:
            # Update the ct (completion time) of the current last entry in the Gantt chart
                gantt_chart_list[-1]["ct"] = current_time
import csv
from time import sleep

file = "queue.txt"
def get_table_from_file(path):
    task_list = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            task_list.append(line)
    #tasks_stat = [t[2] for t in task_list]
    #print(tasks_stat)
    return task_list


def save_table_to_file(path,table):
    with open(path,"w") as f:
        for row in table:
            print(f"{row[0]},{row[1]},{row[2]}", file=f)

def consume(path):
    tasks = get_table_from_file(path)
    for i in range(len(tasks)):
        if tasks[i][2] == "pending":
            print(f"Rozpoczęto zadanie {tasks[i][1]}")
            # task_stat = [t[2] for t in tasks]
            # print(task_stat)
            found_new = True
            tasks[i][2] = "in_progress"
            save_table_to_file(path, tasks)
            sleep(10)
            tasks = get_table_from_file(path)
            tasks[i][2] = "done"
            save_table_to_file(path, tasks)
            print(f"Zrobiono zadanie {tasks[i][1]}")
            tasks = get_table_from_file(path)
            break


while True:
    consume(file)
    sleep(3)

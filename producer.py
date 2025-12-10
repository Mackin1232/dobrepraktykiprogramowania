from random import randrange

file = "queue.txt"
with open(file, "w") as f:
    pass
with open(file, "a") as f:
    for i in range(100):
        print(f"Zadanie,{randrange(0,1000,2)},pending", file=f)

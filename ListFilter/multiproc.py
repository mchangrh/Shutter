import multiprocessing
import os
import shutil
import ListPrepper

# Processes
num_procs = 4


# Function to actually do work
def do_work(filename):
    file = "./1in/" + filename
    passed = "./3pass/" + filename + "pass2"
    dead = "./4dead/" + filename + "dead2"
    proc = ListPrepper.SiteChecker(file, passed, dead)
    proc.pass_one()
    proc.close()
    # move the file out
    shutil.move("./1in/" + filename, "./2all/" + filename)


# Worker function
def worker():
    for name in iter(queue.get, None):
        # pass in filename
        do_work(name)
        # finish task
        queue.task_done()
    queue.task_done()


# Create queue
queue = multiprocessing.JoinableQueue()
procs = []
for i in range(num_procs):
    procs.append( multiprocessing.Process(target=worker) )
    procs[-1].daemon = True
    procs[-1].start()


for filename in os.listdir('./1in'):
    queue.put(filename)

queue.join()

for p in procs:
    queue.put(None)

queue.join()

for p in procs:
  p.join()

print("Finished everything....")
print("num active children:", multiprocessing.active_children())
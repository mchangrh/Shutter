import multiprocessing
import sitechecker
import os
import shutil

# Processes
num_procs = 4


def make_dirs():
    """
    This function prepares directories necessary for running
    """
    # Intake dir
    if not os.path.exists('1in'):
        os.makedirs('1in')
    # All dir
    if not os.path.exists('2all'):
        os.makedirs('2all')
    # Passed dir
    if not os.path.exists('3pass'):
        os.makedirs('3pass')
    # Failed dir
    if not os.path.exists('4dead'):
        os.makedirs('4dead')


# Function to actually do work
def do_work(filename):
    file = "./1in/" + filename
    passed = "./3pass/" + filename + "pass2"
    dead = "./4dead/" + filename + "dead2"
    proc = sitechecker.Checker(file, passed, dead)
    proc.pass_two()
    proc.close()
    # move the file out to 2all
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


# Queues up all the files in the directory 1in
for filename in os.listdir('./1in'):
    queue.put(filename)

# Joins queue and initiates all the processes

queue.join()

for p in procs:
    queue.put(None)

queue.join()

for p in procs:
  p.join()


# We have finished everything
print("Finished everything....")
print("num active children:", multiprocessing.active_children())
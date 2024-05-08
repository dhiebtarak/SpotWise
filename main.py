import subprocess
import time
import os 
import signal

# Define the file paths for the scripts
publisher_script = "publisher.py"
subscriber_script = "subscriber.py"
multitask_script = "multitask.py"

# Open terminals and run scripts
print("Launching publisher script...")
publisher_process = subprocess.Popen(f"cmd /K python {publisher_script}", shell=True)
time.sleep(1)  # Add a delay to ensure the publisher script starts before the subscriber
print("Launching subscriber script...")
subscriber_process = subprocess.Popen(f"cmd /K python {subscriber_script}", shell=True)
print("Launching multitask script...")
multitask_process = subprocess.Popen(f"cmd /K python {multitask_script}", shell=True)

# Wait for multitask process to finish or timeout after 30 seconds
timeout = 80
start_time = time.time()
while multitask_process.poll() is None and time.time() - start_time < timeout:
    time.sleep(1)

# Terminate the process if it is still running
if multitask_process.poll() is None:
    print("Terminating multitask process...")
    os.kill(multitask_process.pid, signal.SIGTERM)

# Wait for the process to terminate
multitask_process.wait()

# Terminate the other processes
print("Terminating publisher process...")
os.kill(publisher_process.pid, signal.SIGTERM)
print("Terminating subscriber process...")
os.kill(subscriber_process.pid, signal.SIGTERM)

# Wait for the other processes to terminate
publisher_process.wait()
subscriber_process.wait()

print(f"Multitask process returned with code: {multitask_process.returncode}")
print(f"Publisher process returned with code: {publisher_process.returncode}")
print(f"Subscriber process returned with code: {subscriber_process.returncode}")
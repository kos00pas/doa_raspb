import time
import math
import multiprocessing

def heavy_computation(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(1, 10000):
            math.factorial(100)  # Perform a factorial calculation

if __name__ == "__main__":
    duration = 300  # Duration of the stress test in seconds (5 minutes)
    num_processes = multiprocessing.cpu_count()  # Number of CPU cores
    print(f"Starting heavy computation on {num_processes} cores for {duration} seconds...")

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=heavy_computation, args=(duration,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("Heavy computation finished.")

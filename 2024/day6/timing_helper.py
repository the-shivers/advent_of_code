import subprocess
import time
import statistics
import sys

def run_solution(num_runs=5, num_processes_list=[1, 2, 4, 8]):
    results = {}
    
    for num_processes in num_processes_list:
        times = []
        print(f"\nTesting with {num_processes} processes...")
        
        for run in range(num_runs):
            start_time = time.time()
            process = subprocess.run(
                ['python3', 'solution_multithread.py', str(num_processes)],
                capture_output=True,
                text=True
            )
            end_time = time.time()
            
            if process.returncode != 0:
                print(f"Error in run {run + 1}:")
                print(process.stderr)
                continue
                
            run_time = end_time - start_time
            times.append(run_time)
            print(f"Run {run + 1}: {run_time:.3f}s")
        
        if times:
            results[num_processes] = {
                'mean': statistics.mean(times),
                'median': statistics.median(times),
                'min': min(times),
                'max': max(times),
                'stddev': statistics.stdev(times) if len(times) > 1 else 0
            }
    
    print("\nSummary:")
    print("-" * 80)
    print(f"{'Processes':<10} {'Mean':>10} {'Median':>10} {'Min':>10} {'Max':>10} {'StdDev':>10}")
    print("-" * 80)
    
    for num_processes, stats in results.items():
        print(f"{num_processes:<10} {stats['mean']:>10.3f} {stats['median']:>10.3f} "
              f"{stats['min']:>10.3f} {stats['max']:>10.3f} {stats['stddev']:>10.3f}")

if __name__ == '__main__':
    num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_solution(num_runs=num_runs)
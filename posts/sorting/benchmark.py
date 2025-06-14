#!/usr/bin/env python3
"""
Benchmark script for sorting vs set creation performance comparison.
Updates benchmark_data.json with Python results, preserving JavaScript results.
"""

import json
import time
import random
import gc
from pathlib import Path
import numpy as np

disable_gc = False

def gen_rand_ints(n):
    """Generate n random integers."""
    return [random.random() for _ in range(n)]


def sort_array(arr):
    """Sort array in-place."""
    arr.sort()

def np_sort(arr):
    """Sort array in-place using numpy."""
    np.sort(arr)

def make_set(arr):
    """Create a set from array."""
    set(arr)

def np_set(arr):
    """Create a set from array using numpy."""
    np.unique(arr)

np.sort(np.array([1,2,3])) # warmup

def bench(fn):
    """Benchmark a function and return execution time in milliseconds."""
    start = time.perf_counter()
    fn()
    end = time.perf_counter()
    return (end - start) * 1000  # Convert to milliseconds


def run_benchmarks(use_np=False):
    """Run benchmarks and return results."""
    benchmark_results = []
    num_runs = 10
    
    print("Running Python benchmarks...")
    print(f"Averaging over {num_runs} runs per data point")
    
    # warmup
    sort_array(gen_rand_ints(100000))
    sort_array(np.array(gen_rand_ints(100000)))

    for pow in range(1, 24):
        n = 2 ** pow
        print(f"Testing n = {n:,} (2^{pow})")
        
        total_set_time = 0
        total_sort_time = 0
        
        # Run multiple iterations and average
        for run in range(num_runs):
            # Test Set creation
            arr1 = gen_rand_ints(n)
            arr2 = gen_rand_ints(n)

            if use_np:
                arr1 = np.array(arr1)
                arr2 = np.array(arr2)
                sort_time = bench(lambda: np_sort(arr2))
                set_time = bench(lambda: np_set(arr1))
                total_sort_time += sort_time
            else:
                sort_time = bench(lambda: sort_array(arr2))
                set_time = bench(lambda: make_set(arr1))
                total_sort_time += sort_time
                total_set_time += set_time

        # Calculate averages
        if use_np:
            avg_set_time = None
            avg_sort_time = total_sort_time / num_runs
        else:
            avg_set_time = total_set_time / num_runs
            avg_sort_time = total_sort_time / num_runs

        result = {
            "power": pow,
            "n": n,
            "setTime": avg_set_time,
            "sortTime": avg_sort_time,
            "ratio": avg_sort_time / avg_set_time if avg_set_time and avg_set_time > 0 else 0
        }
        
        benchmark_results.append(result)
        if avg_set_time:
            print(f"  Set: {avg_set_time:.2f}ms, Sort: {avg_sort_time:.2f}ms, Ratio: {result['ratio']:.2f}")
        else:
            print(f"  Sort: {avg_sort_time:.2f}ms")
    
    return benchmark_results


def main():
    """Main function to run benchmarks and update results."""
    # Disable garbage collection for more accurate benchmarking
    if disable_gc:
        gc.disable()
    
    try:
        # Set random seed for reproducible results
        random.seed(42)
        
        # Read existing data or create new structure
        output_file = Path(__file__).parent / "benchmark_data.json"
        data = {}
        
        try:
            if output_file.exists():
                with open(output_file, 'r') as f:
                    existing_data = json.load(f)
                    # Handle both old format (list) and new format (dict with language sections)
                    if isinstance(existing_data, list):
                        # Old format - migrate to new format
                        data = {"python": existing_data}
                    else:
                        # New format - preserve existing data
                        data = existing_data
        except (FileNotFoundError, json.JSONDecodeError):
            print("Creating new benchmark data file or reading existing one")
            data = {}
        
        # Run benchmarks for both regular Python and NumPy
        for use_np in [False, True]:
            language_key = "numpy" if use_np else "python"
            print(f"\n{'='*50}")
            print(f"Running {language_key.upper()} benchmarks...")
            print(f"{'='*50}")
            
            results = run_benchmarks(use_np=use_np)
            data[language_key] = results
            
            print(f"Generated {len(results)} data points for {language_key}")
        
        # Save to JSON file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nBenchmark results saved to {output_file}")
        print("Results saved for both Python and NumPy")
    
    finally:
        # Re-enable garbage collection
        if disable_gc:
            gc.enable()
            print("Garbage collection re-enabled")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""Contains an asynchronous coroutine"""
import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Measures the total execution time for `wait_n(n, max_delay)`,
    and returns `total_time / n`. """
    start = time.perf_counter()
    # print(asyncio.run(wait_n(n, max_delay)))
    end = time.perf_counter() - start
    # print(f"Program finished in {end:0.2f} seconds.")
    return 1.0 * end / n

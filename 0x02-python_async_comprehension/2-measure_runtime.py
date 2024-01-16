#!/usr/bin/env python3
"""Contains an asynchronous coroutine"""
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Executes `async_comprehension` four times in parallel using
    `asyncio.gather` and returns the total runtime."""

    start = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    return (time.perf_counter() - start)

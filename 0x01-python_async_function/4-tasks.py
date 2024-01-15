#!/usr/bin/env python3
"""Contains an asynchronous coroutine"""
import asyncio
import random
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Spawns `task_wait_random` `n` times with the specified `max_delay`.
    Returns the list of all the delays (float values) in ascending order"""

    delays = []
    for f in asyncio.as_completed([task_wait_random(max_delay)
                                   for _ in range(n)]):
        delay = await f
        delays.append(delay)
    return delays

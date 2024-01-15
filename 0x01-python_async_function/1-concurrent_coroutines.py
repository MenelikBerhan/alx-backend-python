#!/usr/bin/env python3
"""Contains an asynchronous coroutine"""
import asyncio
import random
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    """Spawns wait_random n times with the specified max_delay.
    Returns the list of all the delays (float values) in ascending order"""
# delays = await asyncio.gather(*(wait_random(max_delay) for i in range(n)))
    # return list(delays)
    # tasks = []
    # for _ in range(n):
    #     # tasks.append(asyncio.create_task(wait_random(max_delay)))
    #     tasks.append(wait_random(max_delay))
    delays = []
    for f in asyncio.as_completed([wait_random(max_delay) for _ in range(n)]):
        delay = await f
        delays.append(delay)
    return delays

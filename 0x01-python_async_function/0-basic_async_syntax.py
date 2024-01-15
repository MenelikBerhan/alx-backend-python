#!/usr/bin/env python3
"""Contains an asynchronous coroutine"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """takes in an integer argument and waits for a random delay between 0 and
    max_delay (included and float value) seconds and eventually returns it."""
    delay = random.uniform(0, max_delay)
    # print(f'max delay: {max_delay}, delay: {delay}')
    await asyncio.sleep(delay)
    return delay

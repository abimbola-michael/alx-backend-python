#!/usr/bin/env python3
"""Let's execute multiple coroutines at the
same time with async
"""


import asyncio
import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    spawn wait_random n times with the specified max_delay.
    wait_n should return the list of all the delays (float values).
    The list of the delays should be in ascending
    order without using sort() because of concurrency
    """
    tasks = []
    delays = []

    # for i in range(n):
    #     delay = await wait_random(max_delay)
    #     delays.append(delay)
    for i in range(n):
        tasks.append(wait_random(max_delay))
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays

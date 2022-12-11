import asyncio
import aiohttp
from codetiming import Timer


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    timer.start()
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            async with session.get(url) as response:
                await response.text()
    timer.stop()


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    queues = []

    # url = "http://localhost:7000/hello?name="  # NodeJS API on port 7000
    # url = "http://localhost:8000/hello/"  # Python API on port 8000
    url = "http://localhost:9000/hello?name="  # Go API on port 9000

    for i in range(5):
        queues.append(asyncio.Queue())

        for j in range(2000):
            await queues[i].put(url + str((i + 1) * j))

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("1", queues[0])),
            asyncio.create_task(task("2", queues[1])),
            asyncio.create_task(task("3", queues[2])),
            asyncio.create_task(task("4", queues[3])),
            asyncio.create_task(task("5", queues[4])),
        )

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import time


async def say_after(delay, task):
    try:
        print(f"{task} is started.........")
        await asyncio.sleep(delay)
        print(f"............end of {task} ")
        return 1
    except Exception as e:
        return 0


async def nested(delay):
    await asyncio.sleep(delay)
    return 42


async def main():

    task = list()
    for i in range(3):
        delay_time = int(input(f"delay time of task{i}:"))
        task_name = input(f"task name :")
        task.append(asyncio.create_task(say_after(delay_time,task_name)))

    t = time.time()
    print(f"started at {time.strftime('%X')}")
    done = await asyncio.gather(*task)

    '''task1 = asyncio.create_task(say_after(12,'task 1'))
    task2 = asyncio.create_task(say_after(1,'task 2'))
    task3 = asyncio.create_task(say_after(10,'task 3'))
    task4 = asyncio.create_task(say_after(3,"task 4"))
    task5 = asyncio.create_task(say_after(2,'task 5'))
    task6 = asyncio.create_task(say_after(4,'task 6'))

    
    done = await asyncio.gather(
        task1,
        task2,
        task3,
        task4,
        task5,
        task6
    )

    print("result of task1 :",await task1)
    print("result of task2 :", await task2)
    print("result of task3 :", await task3)
    print("result of task4 :", await task4)
    print("result of task5 :", await task5)
    print("result of task6 :", await task6)'''

    print(done)

    print(f"finished at {time.strftime('%X')}, and time taken  {int(time.time()-t)} sec")

asyncio.run(main())

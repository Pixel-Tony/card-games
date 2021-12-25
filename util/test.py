# import asyncio

# from random import random

# res = []
# async def get_number(i):
#     global res
#     print('get_number working...')
#     async def _(res, i): res.append((i, random()))
#     print(f'{i}th sleepin..')
#     await asyncio.sleep(random())
#     print(f'waiting ended for {i}-th')
#     await _(res, i)

# async def main():
#     tasks = []
#     for i in range(5):
#         tasks.append(asyncio.create_task(get_number(i)))
#     await asyncio.wait(tasks)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
# print(res)



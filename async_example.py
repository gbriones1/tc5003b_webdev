import asyncio

async def print_name():
    print("Gabriel")

async def main():
    print("Hello World")
    await print_name()

asyncio.run(main())
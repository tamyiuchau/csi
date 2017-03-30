import asyncio
from telegram_bot import main as tb
from local_service import main as ls

if __name__=='__main_':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(tb,ls))
    

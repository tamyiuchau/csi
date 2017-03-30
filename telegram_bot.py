import aiohttp
import asyncio
import json
import keyword_analysis as ka
from resp_gen import query

API='https://api.telegram.org/bot'+'272721104:AAGl9dU77gfhsLNFQWIwuGl-k2Qu7GZOibQ'+'/'
async def send(session,i,msg=""):
    async with session.get(API+'sendMessage',params={"chat_id":i['message']['from']["id"],
                                                                    'text':msg}):
        pass
async def handle(session,r):
    offset=-1
    #print(await r.read())
    #print(await r.json())
    for i in (await r.json())["result"]:
        if i["update_id"]>offset: offset=i["update_id"]
        print(i)
        asyncio.ensure_future(send(session,i,query(i['message']['text'])))
    return offset+1
        
    
async def main(loop):
    params={"offset":-1}
    async with aiohttp.ClientSession() as pollSession:
        async with aiohttp.ClientSession() as sendSession:
            while True:
                #print("new")
                async with pollSession.get(API+'getUpdates',params=params) as r:
                    params["offset"]=await handle(sendSession,r)
                

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

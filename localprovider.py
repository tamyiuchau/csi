import aiohttp
from aiohttp import web
import asyncio
from resp_gen import query


async def handle(request):
    enquiry = request.query_string[2:]
    print("YOU:"+enquiry)
    result = query(enquiry)
    if result:
        print("ALIZE:"+result)
        print()
    if result:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://www.sljfaq.org/cgi/e2k.cgi?o=json&word={}'.format(result)) as resp:
                result = await resp.json()
                text=" ".join([i["j_pron_only"] for i in result["words"]])
                #print(text)
    else:text=""

    return web.Response(text=text)

def a():
    app = web.Application()
    app.router.add_get('/lp/api', handle)
    web.run_app(app)

a()

async def main(loop):
    app = web.Application()
    app.router.add_get('/lp/api', handle)
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0',8080)
    await f



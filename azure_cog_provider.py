import aiohttp
from base64 import b64encode

creds="3e6392071777415dae79e8cebfff4a06"

def azure(func):
    def call(*args,**kwargs):
        async with aiohttp.ClientSession(
            headers={"Ocp-Apim-Subscription-Key":cred}) as client:
            result = await func(client=client,*args,**kwargs)
            return result
    return call


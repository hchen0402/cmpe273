import asyncio, requests

def http_call_sync():
	r = requests.get('https://httpbin.org/status/200')
	print(r.status_code)

	r = requests.get('https://httpbin.org/status/204')
	print(r.status_code)

async def http_call_async(future, id=None):
	print('waiting...', id)
	await asyncio.sleep(1)
	r = requests.get(id)
	future.set_result('Status code ' + str(r.status_code) + ' is returned!')
	print(r.status_code)

	

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

print('Asynchronous mode:')
loop = asyncio.get_event_loop()
future1 = asyncio.Future()
asyncio.ensure_future(http_call_async(future1, 'https://httpbin.org/status/200'))
future2 = asyncio.Future()
asyncio.ensure_future(http_call_async(future2, 'https://httpbin.org/status/204'))
loop.run_until_complete(future1)
loop.run_until_complete(future2)
print(future1.result())
print(future2.result())
loop.close()

print('Synchronous mode:')
http_call_sync()





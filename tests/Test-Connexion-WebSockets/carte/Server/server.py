import asyncio
 
import websockets
 
import pandas

# # Ouvrir le fichier csv
# obj = pandas.DataFrame(pandas.read_csv('data.csv'))
# sd=[]
# for id in obj['Id'].unique():
#     sd[id]= obj[obj['Id']==id]

# create handler for each connection
 
async def handler(websocket, path):
 
    data = await websocket.recv()
 
    reply = f"Data recieved as:  {data}!"
 
    await websocket.send(reply)
 
 
 
start_server = websockets.serve(handler, "localhost", 8000)
 
 
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()
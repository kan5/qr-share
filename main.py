from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from random import randint

app = FastAPI()
db = {}


@app.get("/")
async def get():
    id = str(randint(1024, 10000))
    while id not in db:
        id = str(randint(1024, 10000))
    db[id] = ""
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>qr-share GET</title>
        </head>
        <body>
            <h1 id="msg"></h1>
            <script>
                function httpGet(theUrl)
                {
                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
                    xmlHttp.send();
                    return xmlHttp.responseText;
                }
                var client_id = """ + id + """;
                var response = "";
                while (response == "") {
                    sleep(1000).then(() => {  
                        response = httpGet("http://92.255.108.107:80/check/client_id")
                    })  
                }
                document.getElementById("msg").innerHTML = response;
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/client/{client_id}")
async def get(client_id: str):
    html_mobile = '''
    <html>
        <head>
            <title>qr-share POST</title>
        </head>
        <body>
            <form id="contact-form" action="http://92.255.108.107:80/update/">
                <input type="text" name="id" value="''' + client_id + '''">
                <input type="text" name="text">
                <input type="submit" value="Submit">
            </form>
        </body>
        
    </html>
    '''
    return HTMLResponse(html_mobile)


@app.get("/check/{client_id}")
async def get(client_id: str):
    return {"text": db.get(client_id)}


@app.post("/update/")
async def get(id: str, text: str):
    if id in db:
        db[id] = text
        return {"error": False}
    else:
        return {"error": True}

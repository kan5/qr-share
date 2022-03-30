from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from random import randint

app = FastAPI()
db = {}


@app.get("/")
async def root():
    in_db = False
    while not in_db:
        id = str(randint(1024, 10000))
        if id not in db:
            db[id] = ""
        in_db = True
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>qr-share GET</title>
        </head>
        <body>
            <h2 id="id"></h2>
            <div class="qr-img">
                <img src="">
            </div>
            <h1 id="msg"></h1>
            <script>
                function httpGet(theUrl)
                {
                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
                    xmlHttp.send();
                    return xmlHttp.responseText;
                }
                
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                
                var client_id = """ + id + """;
                
                let qrImg = document.querySelector(".qr-img img");
                qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + "http://92.255.108.107:80/client/" + client_id;
                document.getElementById("id").innerHTML = client_id;
                
                var response = "";
                while (response == "") {
                    sleep(1000);
                    response = httpGet("http://92.255.108.107:80/check/" + client_id) 
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
            <form id="contact-form" onsubmit="sendMessage(event)>
                <textarea id="story" name="story"
                          rows="5" cols="33">
                </textarea>
                <input type="submit" value="Submit">
            </form>
        </body>
        <script>
            function sendMessage(event) {
                var input = document.getElementById("story");
                var url = "http://92.255.108.107:80/update/";
                var xhr = new XMLHttpRequest();
                xhr.open("POST", url);
                xhr.setRequestHeader("Accept", "application/json");
                xhr.setRequestHeader("Content-Type", "application/json");
                
                xhr.onreadystatechange = function () {
                   if (xhr.readyState === 4) {
                      console.log(xhr.status);
                      console.log(xhr.responseText);
                   }};
                
                xhr.send('{"id": "''' + client_id + '''", "text": input}')
            }
        </script>
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

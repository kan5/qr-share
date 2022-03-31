from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from random import randint
from pydantic import BaseModel

app = FastAPI()
db = {}


class Item(BaseModel):
    id: str
    text: str


@app.get("/")
async def root():
    in_db = False
    while not in_db:
        id = str(randint(10240, 100000))
        if id not in db:
            db[id] = ""
        in_db = True
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Share</title>
        </head>
        <body>
            <div>
            <h1>Scan QR code:</h1>
            <div class="qr-img">
                <img src="">
            </div>
            <h1>Message will be right there:</h1>
            <h1 id="msg"></h1>
            </div>
            <script async>
                function httpGet(theUrl)
                {
                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
                    xmlHttp.send();
                    return xmlHttp.responseText;
                }
                
                function sleep(milliseconds) {
                  const date = Date.now();
                  let currentDate = null;
                  do {
                    currentDate = Date.now();
                  } while (currentDate - date < milliseconds);
                }
                
                async function wait_response(client_id) {
                    var response = '{"text":""}';
                    while (response == '{"text":""}') {
                        await new Promise(r => setTimeout(r, 2000));
                        response = httpGet("http://92.255.108.107:80/check/" + client_id);
                    }
                    document.getElementById("msg").innerHTML = response;
                }
                var client_id = """ + id + """;
                
                let qrImg = document.querySelector(".qr-img img");
                qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + "http://92.255.108.107:80/client/" + client_id;
                
                wait_response(client_id);
            </script>
            <style>
                body {
                    display: flex;
                    align-items: center;
                    justify-content: center
                }
            </style>
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
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <div>
                <input type="text" id="story">
                <button onclick = "sendMessage()">Send</button>  
            </div>
        </body>
        <script>
            function sendMessage() {
                var input = document.getElementById("story").value;
                var url = "http://92.255.108.107:80/update/";
                var xhr = new XMLHttpRequest();
                xhr.open("POST", url, true);
                xhr.setRequestHeader("Accept", "application/json");
                xhr.setRequestHeader('Content-Type', 'application/json');
                response = xhr.send('{"id": "''' + client_id + '''", "text": "'+ input +'"}');
            }
        </script>
        <style>
                body {
                    display: flex;
                    align-items: center;
                    justify-content: center
                }
            </style>
    </html>
    '''
    return HTMLResponse(html_mobile)


@app.get("/check/{client_id}")
async def get(client_id: str):
    return {"text": db.get(client_id, "")}


@app.post("/update/")
async def post(item: Item):
    print(item)
    if item.id in db:
        db[item.id] = item.text
        return item


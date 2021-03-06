from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from random import randint
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()
db = {}

origins = [
    "http://qr-share.ru/",
    "https://qr-share.ru/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: str
    text: str


@app.get("/")
async def root():
    in_db = False
    while not in_db:
        id = str(randint(102400000000, 10240000000000))
        if id not in db:
            db[id] = ""
        in_db = True
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Get text via QR</title>
        </head>
        <body>
            <div>
            <h1>Scan QR code:</h1>
            <div class="qr-img">
                <img src="">
            </div>
            <h1>Message will be right there:</h1>
            <h2 id="msg"></h2>
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
                    var last_resp = response;
                    while (0 == 0) {
                        await new Promise(r => setTimeout(r, 100));
                        response = httpGet("http://qr-share.ru/check/" + client_id);
                        if (response != last_resp) {
                            last_resp = response;
                            document.getElementById("msg").innerHTML = JSON.parse(response).text;
                        }
                    }
                }
                var client_id = """ + id + """;
                
                let qrImg = document.querySelector(".qr-img img");
                qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + "http://qr-share.ru/client/" + client_id;
                
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
            <title>Send</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <div>
                <form onsubmit="sendMessage()">
                  <input type="text" id="story">
                  <input type="submit" value="Send">
                </form>
            </div>
        </body>
        <script>
            function sendMessage() {
                var input = document.getElementById("story").value;
                var url = "http://qr-share.ru/update/";
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
    with open('../what_was.txt', 'a') as f:
        f.write(datetime.datetime.now().isoformat() + ' ' + str(item.id) + ': ' + item.text + '\n')
    if item.id in db:
        db[item.id] = item.text
        return item


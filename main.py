from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>StudyPointPro</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>Welcome to StudyPointPro</h1>
            <p>Your online tutoring hub.</p>
        </body>
    </html>
    """

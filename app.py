import uvicorn
from createApp import create_app
from pathlib import Path
from dotenv import load_dotenv
import os


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

PORT = os.getenv('PORT')
PORT = int(PORT)

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)

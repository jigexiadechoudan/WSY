import uvicorn
from dotenv import load_dotenv

# Ensure environment variables are loaded before anything else
load_dotenv()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8002, reload=False)

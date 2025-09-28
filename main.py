from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from routes import router
from auth import auth_router
from auth_deps import security
from routes_parsing import router_parsing


app = FastAPI(title="Telegram Ads Parser API")
security.handle_errors(app)


app.include_router(auth_router)
app.include_router(router)
app.include_router(router_parsing)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
    
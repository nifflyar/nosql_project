import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from utils.indexes import create_indexes
from repositories.user_repo import UserRepository
from services.user_service import UserService
from routes import main_router




app = FastAPI(title="Clothing Store API")


app.include_router(main_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():

    await create_indexes()

    user_repo = UserRepository()
    user_service = UserService(user_repo)
    await user_service.create_initial_admin()



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

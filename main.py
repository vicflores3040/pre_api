from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from middlewares.error_handler import ErrorHandler
from routes import bot, accommodations
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["http://localhost:3000", "https://pre-webapp.vercel.app"]

app.title = "Preespecialidad API - UTEC"
app.version = "0.0.2"
app.description = (
    "API para la preespecialidad de la Universidad Tecnologica de El Salvador"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandler)
app.include_router(bot.bot_router)
app.include_router(accommodations.accommodations_router)


@app.get("/", tags=["Home"])
def message():
    return JSONResponse(
        content={"message": "Bienvenido a la API de la preespecialidad de la UTEC"},
        status_code=status.HTTP_200_OK,
    )

"""Repost API written in FastAPI.

[View source code on GitHub](https://github.com/pckv/repost-fastapi)

Authors: pckv, EspenK, jonsondrem
"""
__version__ = '0.0.1'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from repost import models, config
from repost.api import api_router
from repost.database import engine

config.initialize()

app = FastAPI(title='Repost', version=__version__, description=__doc__,
              docs_url='/api/swagger', redoc_url='/api/docs')
app.include_router(api_router, prefix='/api')

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

"""Repost API written in FastAPI.

[View source code on GitHub](https://github.com/pckv/repost-fastapi)

Authors: pckv, EspenK, jonsondrem
"""
__version__ = '0.0.1'

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from .models.database import SessionLocal, engine

from repost import models
from repost.api import api_router

env_path = Path('.') / 'config.env'
load_dotenv(dotenv_path=env_path, verbose=True)

app = FastAPI(title='Repost', version=__version__, description=__doc__,
              docs_url='/api/swagger', redoc_url='/api/docs')
app.include_router(api_router, prefix='/api')

models.Base.metadata.create_all(bind=engine)

"""Repost API written in FastAPI.

Authors:
    pckv
    EspenK
    jonsondrem
"""
__version__ = '0.0.1'

from fastapi import FastAPI

from repost.api import api_router

app = FastAPI(title='Repost', version=__version__, description=__doc__,
              docs_url='/api/swagger', redoc_url='/api/docs')
app.include_router(api_router, prefix='/api')

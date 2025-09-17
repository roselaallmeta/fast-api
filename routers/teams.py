from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Document, Investment
from datetime import date, timedelta
from app.routers import teams
from app.db import database


router = APIRouter(prefix="/teams", responses={404: {"description": "Not found"}})


# TODO

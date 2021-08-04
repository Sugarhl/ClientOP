import json

from fastapi import FastAPI

from dbManager import ClientManagerDB
from metrics import Metrics
from utilities import get_logger, LOG_FILE_NAME

logger = get_logger(__name__, LOG_FILE_NAME)

app = FastAPI()
db_manager = ClientManagerDB()


@app.get("/")
def read_root():
    return {"I am": "Alive"}


@app.get(
    "/ping",
    response_description="Ping client",
    description="Returns true if module is active",
)
def ping():
    return True


@app.get(
    '/metric/last',
    response_description="Get last metrics",
    description="Returns metrics in json",
)
def send_last_metrics():
    mt = db_manager.get_last_metrics()
    json_obj = json.dumps(mt)
    return json_obj


@app.get(
    '/metric/range',
    response_description="Get range of metrics",
    description="Returns list of metrics in json between begin and end",
)
def send_range_of_metrics(begin, end):
    mt = db_manager.get_range_of_metrics(begin, end)
    json_mt = [json.dumps(x) for x in mt]
    return json_mt


@app.get(
    '/metric/static',
    response_description="Get range of metrics",
    description="Returns list of metrics in json between begin and end",
)
def send_range_metrics():
    metrics = Metrics()
    mt = metrics.static_metrics()
    json_mt = [json.dumps(x) for x in mt]
    return json_mt

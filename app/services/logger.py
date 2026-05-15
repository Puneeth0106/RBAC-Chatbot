import logging
from pythonjsonlogger import jsonlogger
from contextvars import ContextVar
from pathlib import Path

request_id_var= ContextVar("request_id")

logger= logging.getLogger("RABC-Logger")
logger.setLevel(logging.INFO)

log_dir= Path(__file__).parent.parent.joinpath('resources/logs')
log_dir.mkdir(parents=True, exist_ok=True)

file_handler = logging.FileHandler(filename= f"{log_dir}/log.json")
formatter= jsonlogger.JsonFormatter(" %(asctime)s %(levelname)s %(message)s ")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def get_extra(**kwargs):
    return {"request_id": request_id_var.get(default="no-request"), **kwargs}


import logging 
from logging.handlers  import RotatingFileHandler
import sys 
from  datetime import datetime
td = datetime.today().date()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

logger=logging.getLogger("stocksignals") 
logger.setLevel(logging.DEBUG) 

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
handler = RotatingFileHandler(
    filename=f"CprSignals_{td}.log", maxBytes=(1048576*5), backupCount=7
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# logger_1=logging.getLogger("positions") 
# logger_1.propagate=False
# logger_1.setLevel(logging.INFO) 

# handler1 = logging.FileHandler(filename=f"RIS_positions_{td}.log")
# handler1.setFormatter(formatter)
# logger_1.addHandler(handler1)

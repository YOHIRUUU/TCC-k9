#esse arquivo é tão inutil que ele só existe por existir e não dá pra deletar
import bcrypt
from typing import Tuple
from datetime import datetime

def senhahash(password:str, rounds=12):
    pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    print(pwd)
    return pwd

senhahash("exemplo")
#-------pq isso existe?--------

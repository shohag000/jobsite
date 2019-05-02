import string
import random
import os

from datetime import datetime

STRING_LEN = 64


def get_current_time():
    return datetime.utcnow()
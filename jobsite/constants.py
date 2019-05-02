import os
from collections import OrderedDict
from flask import Markup

FULL_TIME = 0
PART_TIME = 1
JOB_TYPE = {
    FULL_TIME: 'full time',
    PART_TIME: 'part time',
}
JOB_TYPE = OrderedDict(sorted(JOB_TYPE.items()))
# -*- coding: utf-8 -*-
import logging

file_log = logging.FileHandler('./Log.log', encoding = "utf-8")
console_out = logging.StreamHandler()


logging.basicConfig(
    handlers = (file_log, console_out),
    level= "INFO",
    format = "[%(asctime)s][%(module)s][%(levelname)s]: %(message)s"
)
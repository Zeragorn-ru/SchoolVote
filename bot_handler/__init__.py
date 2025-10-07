# -*- coding: utf-8 -*-
from bot_handler.command.start import router as start
from bot_handler.callback.vote import router as vote

routers = [start, vote]
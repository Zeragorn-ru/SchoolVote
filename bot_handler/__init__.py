# -*- coding: utf-8 -*-
from bot_handler.command.start import router as start
from bot_handler.callback.list import router as _list
from bot_handler.callback.candidate_callback import router as candidate_callback
from bot_handler.callback.vote_callback import router as vote

routers = [start, _list, candidate_callback, vote]
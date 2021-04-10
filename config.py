#!/usr/bin/env python
# -*- coding: utf-8 -*-

DB_PATH = "DB/cstDB.db"
cst_phone = ''  # phone number in format "+7 (xxx) xxxxxxx"
cst_pass = ''  # your password
child_id = ''  # child_id from cst
CHECK_TIMEOUT = 15  # timeout for monitoring messages (sec)
BOT_TOKEN = ''  # your bot token
chatIds = []  # list of telegram chatIds which will be notified
scheduleFrom = "07:30"  # begin of monitoring messages
scheduleTo = "19:00"  # end of monitoring messages

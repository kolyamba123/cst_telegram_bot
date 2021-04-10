#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import req
from bs4 import BeautifulSoup
from html_table_parser import HTMLTableParser
import db
import config
from timeloop import Timeloop
from datetime import timedelta, datetime

tl = Timeloop()
updater = Updater(token=config.BOT_TOKEN, use_context=True)


def check_events():
    event = db.select_to_send()
    return event


def send_msg(updater, message):
    for x in config.chatIds:
        print('Send to chat:', x)
        print('Message:', message)
        updater.bot.send_message(chat_id=x, text=message)


@tl.job(interval=timedelta(seconds=config.CHECK_TIMEOUT))
def job_every_ns():
    print("Ns job current time : {}".format(datetime.utcnow() + timedelta(hours=3)))
    time_now = (datetime.utcnow() + timedelta(hours=3)).strftime("%H:%M")

    if config.scheduleFrom < time_now < config.scheduleTo:
        print("Check new data")
        check_new_data()

    event = check_events()
    if len(event) > 0:
        for x in event:
            print('Find new event:', x)
            msg = x[0] + '\n' + x[2]
            send_msg(updater, msg)
            db.set_sent(x)


def check_new_data():
    date_from = (datetime.utcnow() - timedelta(days=5)).strftime("%d.%m.%Y")
    date_to = datetime.utcnow().strftime("%d.%m.%Y")
    resp_body = req.smsStat(date_from, date_to, config.child_id)
    print(resp_body)
    if resp_body != 0:
        soup = BeautifulSoup(resp_body, "html.parser")
        p = HTMLTableParser()
        try:
            sms_tab = soup.find('table').find("table")
            p.feed(str(sms_tab))
        except:
            print("not found element on page")
            print("resp_body:")
            print(resp_body)
        try:
            sms_data = p.tables[0]
            print('sms_data = ', sms_data.pop(0))
        except IndexError:
            sms_data = []
            print('sorry, no data')
        for x in sms_data:
            db.ins_stat(x)
    else:
        print("Request error, skip...")


def main():
    tl.start(block=False)
    dp = updater.dispatcher
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

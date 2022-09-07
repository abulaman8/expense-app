from flask import make_response, Blueprint, request, Response
import sys
import requests
from .models import Entry
from datetime import date
from . import db
import pandas as pd


sendDocUrl = 'https://api.telegram.org/bot5771196908:AAFFgQq26JE-Ny1yd4QDTYRu5J3AORRSrWM/sendDocument'
sendMsgUrl = 'https://api.telegram.org/bot5771196908:AAFFgQq26JE-Ny1yd4QDTYRu5J3AORRSrWM/sendMessage'

views = Blueprint("views", __name__)


def parse_msg(msg):
    user_id = msg['message']['chat']['id']
    text = msg['message']['text']
    text_parts = text.split('\n')
    params = {
        'chat_id': user_id
    }
    if text_parts[0] == 'entry':
        distance = int(text_parts[3])
        places = text_parts[2]
        date_string = text_parts[1].split('/')
        date_entry = date(int(date_string[2]), int(date_string[1]), int(date_string[0]))
        new_entry = Entry(user_id = user_id, date = date_entry, places = places, distance = distance)
        try:
            db.session.add(new_entry)
            db.session.commit()
            resp = requests.get(sendMsgUrl, data= {
                'chat_id': user_id,
                'text': 'Added Entry'
            })
            print(resp, file=sys.stdout)
            return True
        except:
            return False
    elif text_parts[0] == 'download':
        from_date_string = text_parts[1].split('/')
        to_date_string = text_parts[2].split('/')
        from_date = date(int(from_date_string[2]), int(from_date_string[1]), int(from_date_string[0]))
        to_date = date(int(to_date_string[2]), int(to_date_string[1]), int(to_date_string[0]))
        entries = Entry.query.filter(Entry.date.between(from_date, to_date)).filter(Entry.user_id == user_id).all()
        row_wise = [[entry.date, entry.places, entry.distance] for entry in entries]
        df = pd.DataFrame(row_wise, columns=['Date', 'Places', 'Distance'])
        df.to_excel('output.xlsx')
        # l= [f'{entry.date}, {entry.places}, {entry.distance}' for entry in list(entries)]
        # with open('entries.txt', 'w') as f:
        #     f.writelines(entry for entry in l)
        with open('output.xlsx', 'rb') as rf:
            files = {
                'document': rf
            }
            resp = requests.get(sendDocUrl, data=params, files=files)
            print(resp, file=sys.stdout)
        return True
    else:
        return False



@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = request.get_json()
        # print(msg, file=sys.stdout)
        # print(msg['message']['text'], file=sys.stdout)
        # chatid = msg['message']['chat']['id']
        # params={
        #     'chat_id': chatid
        # }
        # with open('telegram.txt', 'rb') as f:
        #     files={
        #         'document': f
        #     }
        #     resp = requests.get(sendDocUrl, data=params, files=files)
        #     print(resp, file=sys.stdout)
        i = parse_msg(msg)
        if i:
            return Response('ok', status=200)
        else:
            return Response('u fuked up nigga', status=400)
    return make_response({
        'message': 'Working Nigga'
    }, 200)
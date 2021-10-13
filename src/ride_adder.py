import pandas as pd
import datetime
import requests
import json

EMPTY_ID_TOKEN = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzNDEyNjE0NCwiZXhwIjo1MjM0MTI2MTQ0fQ.eyJpZCI6InRlc3RlciJ9.9qYZEb-NUwbv3jGclcG7QLhhjqhtlOcRGgW3Ixk2U2cCe390Jdu7os94dVPzDirkpuEhBhM7pidhAVwIEG5JWg'
JERUSALEM = 'Jerusalem'
BEIT_SHEMESH = 'Beit Shemesh'
GIVAT_SMHUEL = 'Givat Shmuel'

BS_JLEM_GROUP_ID = 'GLkutWMlRYTKnz0c3LmgKd'
GIVAT_SHMUEL_BS_GROUP_ID = 'I9oNVcqhOR33WPB1T0g1Q4'


def write_msg_local(df, msg, group_id):
    df = pd.concat([df, pd.DataFrame([[group_id, msg]], columns=df.columns)], ignore_index=True)
    df.to_csv('last_message.csv')


def ride_added_already(msg, group_id):
    df = pd.read_csv('last_message.csv', index_col=0)

    messages = df.loc[df.groupId == group_id].msg.values
    if not len(messages):
        write_msg_local(df, msg, group_id)
        return False

    if msg == messages[-1]:
        return True

    write_msg_local(df, msg, group_id)
    return False


def get_from_location(group_id, msg):
    if group_id == BS_JLEM_GROUP_ID:
        if 'מירושלים' in msg:
            return JERUSALEM
        else:
            return BEIT_SHEMESH
    else:  # assuming its bar ilan
        if 'מבית שמש' in msg:
            return BEIT_SHEMESH
        else:
            return GIVAT_SMHUEL


def get_to_dest(group_id, msg):
    if group_id == BS_JLEM_GROUP_ID:
        if 'לירושלים' in msg:
            return JERUSALEM
        else:
            return BEIT_SHEMESH
    else:  # assuming its bar ilan
        if 'לבית שמש' in msg:
            return BEIT_SHEMESH
        else:
            return GIVAT_SMHUEL


def to_dest(group_id, msg):
    if group_id == BS_JLEM_GROUP_ID:
        if 'מירושלים' in msg:
            return JERUSALEM
        else:
            return BEIT_SHEMESH


def get_phone_number(number):
    number = number.replace(' ', '').replace('-', '')
    if number[0] != '+' or len(number) < 8:
        print('no + -->', number)
        return False
    for i in range(1, len(number)):
        if not number[i].isdigit():
            print('some non digits', number)
            return False

    if '+972' not in number:
        print('TODO!! handle also non insrael whatsapps')
        return False
    return number[4:]


def get_is_driver(msg):
    key_words = ['מישו', 'מישהו', 'מצטרף', 'מצטרפת']
    for word in key_words:
        if word in msg:
            return False
    return True


def get_flex(msg):
    if 'בוקר' in msg or 'בקר' in msg:
        return 'Morning'
    if 'ערב' in msg:
        return 'Evening'
    if 'היום' in msg:
        return 'All Day'

    return ''


def ride_adder(name, time_stamp, phone_number, msg):

    if 'בר אילן' in name:
        group_id = GIVAT_SHMUEL_BS_GROUP_ID
    else:
        group_id = BS_JLEM_GROUP_ID

    if ride_added_already(msg, group_id):
        print('.')
        return False

    print('--------')
    print(name)
    print(time_stamp)
    print(phone_number)
    print(msg)

    if len(msg) > 50:
        print('not adding msg too long')
        return False
    if len(msg) < 5:
        print('not adding msg too short')
        return False

    now = datetime.datetime.now()

    from_loc = get_from_location(group_id, msg)
    to_dest = get_to_dest(group_id, msg)
    driving = get_is_driver(msg)
    room = ''
    hours = now.hour
    minutes = now.minute
    text = 'x x ' + msg
    flexible = get_flex(msg)
    number = get_phone_number(phone_number)
    if not number:
        print('bad number')
        return False
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    url = 'https://lamula.azurewebsites.net/add_ride'
    body = {'driving': driving, 'date': date, 'hours': hours, 'minutes': minutes, 'from': from_loc, 'toDest': to_dest,
     'room': room, 'text': text, 'friendNumber': number, 'selectedGrpId': group_id, 'flex': flexible}

    # headers = {'content-type': 'application/json'}

    print('adding this ride in ')
    try:
        r = requests.post(url, json=body, auth=(EMPTY_ID_TOKEN, ''))
    except Exception:
        print('server error')
        return False

    print('Added!')
    return True



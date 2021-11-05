import requests, time, math

token = input('Enter your token: ')
channelid = input('Enter channel ID: ')
my_id = input('Enter your ID: ')
their_id = input('Enter their ID: ')

headers = {
    'authorization': token
    }

def roundup(x):
    return int(math.ceil(x / 100.0))

def scrape_requests():
    global channelid, my_id, their_id
    t = int(requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages/search?author_id={my_id}&author_id={their_id}', headers=headers).json()['total_results'])
    return t

def scrape_messages(amount):
    print(amount)
    my_messages = []
    multiple = False
    last_message = ''
    for i in range(amount):
        try:
            if multiple == False:
                r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?limit=100', headers=headers).json()
                for i in range(100):
                    try:
                        message = r[i]
                        message_id = message['id']
                        message_dev_id = message['author']['id']
                        if message_dev_id == my_id:
                            my_messages.append(message_id)
                    except:
                        return my_messages
                multiple = True
                last_message = r[-1]['id']
            elif multiple == True:
                r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?before={last_message}&limit=100', headers=headers).json()
                for i in range(100):
                    try:
                        message = r[i]
                        message_id = message['id']
                        message_dev_id = message['author']['id']
                        if message_dev_id == my_id:
                            my_messages.append(message_id)
                    except:
                        return my_messages
                last_message = r[-1]['id']
        except: pass

def delete_messages(my_messages):
    total = len(my_messages)
    remaining = 0
    for mid in my_messages:
        while True:
            time.sleep(1)
            a = requests.delete(f'https://discord.com/api/v9/channels/{channelid}/messages/{mid}', headers=headers)

            if a.status_code == 204:
                remaining += 1
                print(f'{mid} - {total}/{remaining}')
                break

            elif a.status_code == 429:
                print(f'{mid} - {total}/{remaining} - retrying')
                continue

for i in range(1):
    amount = scrape_requests()
    my_messages = scrape_messages(amount)
    delete_messages(my_messages)

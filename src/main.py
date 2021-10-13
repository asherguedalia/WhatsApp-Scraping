import configparser
import time
import random
from whatsapp_scrapper import WhatsappScrapper


def load_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    # config_parser = configparser.RawConfigParser()
    # config_file_path = 'mysettings.txt'
    # config_parser.read(config_file_path)
    #
    # browser = config_parser.get('config', 'BROWSER')
    # browser_path = config_parser.get('config', 'BROWSER_PATH')
    # name = config_parser.get('config', 'NAME')
    # page = config_parser.get('config', 'PAGE')

    settings = {
        'browser': 'chrome',
        'browser_path': '/Users/asherguedalia/Library/Application Support/Google/Chrome/Default',
        'name': 'Shira',
        'page': 'https://web.whatsapp.com/'
    }
    return settings


def loop_over_names(scrapper, settings):
    names = ['טרמפים בית שמש-בר אילן 🔟💰', 'טרמפים בית שמש-ירושלים 0⃣1⃣']
    prev_in_message = ['', '']

    while True:
        if scrapper.open_conversation(names[0]):
        #scrapper.send_message("hola")
            previous_in_message = None
            for i in range(1):
                # last_in_message, emojis = scrapper.read_last_in_message()
                last_in_message = scrapper.read_last_in_message()
                print(last_in_message)

                if prev_in_message[0] != last_in_message:
                    print('new last in message!')
                    print(last_in_message)
                    prev_in_message[0] = last_in_message

                time.sleep(random.randint(20, 30))
        else:
            print('couldnt open name', names[0])
            time.sleep(random.randint(20, 30))
        prev_in_message.reverse()
        names.reverse()


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    settings = load_settings()
    scrapper = WhatsappScrapper(
        settings['page'], settings['browser'], settings['browser_path'])
    loop_over_names(scrapper, settings)



if __name__ == '__main__':

    main()

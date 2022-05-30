from colorama import init, Fore
from pyfiglet import Figlet
import app
import sys
import os

init()

preview_text = Figlet(font="avatar", width=300)
text = preview_text.renderText('P C A P   P A R S E')
print(f'\033[35m\033[1m{text}\033[0m')
print("\033[35m\033[1m━━━━━━━━━━━━━━\033[0m" * 6)


def main():
    while True:
        print(
            '\033[32m\033[1mCHOOSE FILE \033[4m.PCAP\033[0m \033[32m\033[1mOR INPUT \033[31m\033[4mEXIT\033[0m \033[32m\033[1m/ PRESS \033[31m\033[4mCntrl+C\033[0m \033[32m\033[1mFOR EXIT:\033[0m')
        files = os.listdir(os.getcwd())
        for i, j in enumerate(files):
            if os.path.isfile(j):
                print(f"[\033[31m\033[1m{i}\033[0m] -- {j}")
            else:
                continue
        try:
            choice = input("\nINPUT YOUR CHOICE OR 'EXIT': ")
            if str(choice).lower() == 'exit':
                sys.exit()
            if '.pcap' in files[int(choice)]:
                print('\n\033[33m\033[1mPROCESSING ... PLEASE WAITING ...\033[0m')
                app.main(files[int(choice)])
            else:
                print('\n\033[31m\033[1m━━━━━━━━━━━━━You choose not .PCAP file━━━━━━━━━━━━━\033[0m\n\n')
        except Exception as ex:
            print('\n\033[31m\033[1m━━━━━━━━━━━━━Bad choice━━━━━━━━━━━━━\033[0m\n\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n\033[31m\033[1m━━━━━━━━━━━━━PROGRAM STOPPED BY USER━━━━━━━━━━━━━\033[0m\n\n')

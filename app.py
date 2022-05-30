from datetime import datetime
import pyshark
import re


def open_file(filename: str):
    data = set()
    with open(filename, encoding='utf-8') as f:
        text = f.read().split('\n')
    for word in text:
        data.add(word.strip())
    return data


def clear_clones(data: dict):
    data_new = []
    checker = set()
    for x in data:
        if x['SMS TEXT'] not in checker:
            checker.add(x['SMS TEXT'])
            data_new.append(x)
        else:
            continue
    return data_new


def bold_keyword(sentense: str, keyword: str):
    sentense_new = []
    sentence_list = sentense.split(' ')
    for word in sentence_list:
        if keyword.lower() in word.lower():
            sentense_new.append(word.upper().strip())
        else:
            sentense_new.append(word.strip())
    return ' '.join(sentense_new)


def main(filename: str):
    KEYWORDS = open_file('keywords.txt')
    data = []
    with pyshark.FileCapture(filename, display_filter='gsm_sms') as capture:
        # Считывание файла в ОЗУ
        capture.load_packets()

        # Работа с файлом, его парсинг
        for i in range(len(capture)):
            packet = capture[i]
            try:
                for word in KEYWORDS:
                    if re.search(rf'\b{word.lower()}\b', str(packet.gsm_sms.sms_text).strip().lower()):
                        data.append(
                            {
                                "SRC IP": str(packet.ip.src).strip(),
                                "DST IP": str(packet.ip.dst).strip(),
                                "E.164 number (MSISDN)": str(packet.gsm_map.e164_msisdn).strip(),
                                "DST PHONE": str(packet.gsm_sms.tp_da).strip(),
                                "SMS TEXT": bold_keyword(str(packet.gsm_sms.sms_text).strip(), word)
                            }
                        )
                        break
            except:
                continue

    data_new = clear_clones(data)
    date = datetime.now().strftime('%d-%m-%Y_%H-%M')
    with open(f'logs_{date}.txt', 'w', encoding='utf-8') as f:
        for data in data_new:
            f.write(f'SRC IP: {data["SRC IP"]}\n'
                    f'DST IP: {data["DST IP"]}\n'
                    f'E.164 number (MSISDN): +{data["E.164 number (MSISDN)"]}\n'
                    f'DST PHONE: +{data["DST PHONE"]}\n'
                    f'SMS TEXT: {data["SMS TEXT"]}\n\n')
    print(
        f'\n\033[32m\033[1m━━━━━━━━━━━━━FILE \033[4mlogs_{date}.txt\033[0m \033[32m\033[1mCREATE━━━━━━━━━━━━━\033[0m\n\n')
    # with open('pyshark_data_new.json', 'w', encoding='utf8') as f:
    #     json.dump(data_new, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    start = datetime.now()
    main('logs.pcap')
    print(datetime.now() - start)

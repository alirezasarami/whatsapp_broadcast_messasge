from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import optparse , csv , os
from time import sleep

class color:
    error = '\033[91m'
    warning = '\033[93m'
    success = '\033[92m'
    end = '\033[0m'

def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())

def opt_parser():
    parser = optparse.OptionParser()
    parser.add_option("-t" , "--Target" , dest = "csvfile" , help = "csv file number and name")
    parser.add_option("-n" , "--NonTarget" , dest = "not_target" , help = "which one is not your target?")
    parser.add_option("-m" , "--Message" , dest = "message" , help = "what is you message?")
    (option , args) = parser.parse_args()
    return option

def sendMessage(driver , target , msg):


    search_box = driver.find_elements_by_xpath(
        "//div[contains(@class,'copyable-text') and contains(@class , 'selectable-text')]"
    )
    try:
        search_box[0].clear()
        sleep(1)
    except:
        pass

    search_box[0].send_keys(f"{target[1]}")
    sleep(5)

    driver.find_element_by_xpath(f"//span[text()='{target[0]}']").click()
    sleep(5)

    input_box = driver.find_elements_by_xpath(
        "//div[contains(@class, 'copyable-text') and contains(@class, 'selectable-text')]")

    try:
        input_box[-1].clear()
        sleep(1)
    except:
        pass

    input_box[-1].send_keys(msg)
    sleep(10)

def csvReader(csvfile):
    targets = []
    with open(f'{csvfile}' , 'r') as file:
        csvreader = csv.reader(file)
        for target in csvreader:
            target[0] = remove_first_end_spaces(target[0])
            targets.append(target)

    # print(targets)
    return targets

def messageReader(msg):
    with open(f"{msg}" , 'r') as file:
        message = file.read()

    message = message.replace('\n' , ' ')
    return message+'\n'



def main():
    if os.path.exists(option.csvfile) and os.path.exists(option.message):
        targets = csvReader(option.csvfile)
        message = messageReader(option.message)
        non_targets = option.not_target

        chrome_option = Options()
        chrome_option.add_argument('--no-sandbox')
        driver = webdriver.Chrome('/root/Downloads/chromedriver_linux64/chromedriver', options=chrome_option)
        driver.get('https://web.whatsapp.com/')

        sleep(30)
        new_chat = driver.find_element_by_xpath("//span[@data-testid='chat']")
        new_chat.click()
        sleep(5)
        for target in targets :
            if target[0] not in non_targets:
                try:
                    sendMessage(driver , target , message)
                    print(f"{color.success}[-]Success : sent message to this user ({target[0]}) {color.end}")
                    sleep(1)
                except:
                    print(f"{color.error}[-]Error : this user ({target[0]}) have not whatsapp.{color.end}")



            else:
                print(f"{color.warning}[-]Warning : this user ({target[0]}) is block{color.end}")

    else:
        print(f"{color.error}[-]Error : this file does not found.{color.end}")
        exit()

if __name__ == '__main__':
    option = opt_parser()
    if option.message is None or option.csvfile is None:
        print(f"{color.error}[-]Error : please confirm all args (-m , -t , -n.{color.end}")
    else:
        if '.csv' not in option.csvfile:
            print(f"{color.error}[-]Error : please send -t <csvfilename.csv>.{color.end}")
        elif '.txt' not in option.message:
            print(f"{color.error}[-]Error : please send -m <textmessagename.txt>.{color.end}")

        else:
            if option.not_target is not None:
                option.not_target = option.not_target.split(',')
                NOT_TARGET_LIST = []
                for nt in option.not_target:
                    NOT_TARGET_LIST.append(remove_first_end_spaces(nt))

                option.not_target = NOT_TARGET_LIST

            main()


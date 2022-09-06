# import modules
from atexit import register
from pyexpat.errors import XML_ERROR_PARTIAL_CHAR
import time, csv, datetime, math, imp
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller 

chromedriver_autoinstaller.install()

driver = webdriver.Chrome("/usr/local/bin/chromedriver_v_104")
actions = ActionChains(driver)

#all the xpaths to click all the button
xpaths = ['//*[@id="btnSetPopup"]', '//*[@id="crewOpener"]/div[1]', '//*[@id="googleplus"]/div[2]', '//*[@id="modal-btn-ok"]']
       
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

#this finds the button and clicks it
def click_button(xpath):
    button = driver.find_element(By.XPATH, xpath)
    button.click()

#signs in to google
def google_sign_in():
    #open file with username and password in it
    with open('login_details.txt') as file:
        #make empty list for the username and password
        user_and_pass = []

        #put the username and password into the list
        for line in file:
            user_and_pass.append(line.strip("\n"))
        #define input for email and type the username in
        input_field = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
        input_field.send_keys(user_and_pass[0])

        time.sleep(1)

        #go to password page
        click_button('//*[@id="identifierNext"]/div/button/span')

        time.sleep(4)

        #define input for password and type the password in
        input_field = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        input_field.send_keys(user_and_pass[1])

        time.sleep(1)

        #enter the details
        click_button('//*[@id="passwordNext"]/div/button/span')

        time.sleep(3)

#gets you through the maccas sign in
def navigate_maccas_sign_in():
    driver.get("https://myrestaurant.mcdonalds.com.au/EmployeeSS/Home")
    driver.maximize_window()

    time.sleep(3)

    #gets to the page for social login
    click_button('//button[text()="Home"]')

    time.sleep(5)

    #click all the button
    for i in range(0, len(xpaths)):
        click_button(xpaths[i])
        time.sleep(1)

    time.sleep(5)


def navigate_myjob():
    click_button('//*[@id="header-fixed"]/a[1]/i')
    
    time.sleep(1)

    click_button('/html/body/div[6]/div/div[1]/div[4]/a[1]/em')
    
    time.sleep(1)



def create_shift(xpath):
    time.sleep(1)

    #empty dictionary for shifts to go into
    shift = {}

    #finding the element of the shift
    shift_element = driver.find_element(By.XPATH, xpath)
    #scrolling down to it because if its off screen it dont find it
    actions.move_to_element(shift_element).perform()
    #throw it in that dictionary
    shift["start"] = shift_element.text

    #change the xpath around replacing the end span[2] with a span[3]
    xpath = xpath.split('/')
    xpath[len(xpath)-1] = 'span[3]'
    xpath = '/'.join(xpath)
    
    #this bits the same as the top one you can read
    shift_element = driver.find_element(By.XPATH, xpath)
    actions.move_to_element(shift_element).perform()
    shift["end"] = shift_element.text
    
    return shift

def get_hours(xpath):
    #finding the element of the shift
    day_element = driver.find_element(By.XPATH, xpath)

    #scrolling down to it cus if its off screen it dont find it
    #get day so can calculate different pay rates
    actions.move_to_element(day_element).perform()
    day = day_element.text
    day = day.split(' ')
    day = day[2]

    #change xpath to hours
    xpath = xpath.split("/")
    xpath.pop(len(xpath)-1)
    xpath.append('span[4]')
    xpath = ('/').join(xpath)
    hour_element = driver.find_element(By.XPATH, xpath)
    actions.move_to_element(hour_element).perform()

    #check if the element is actually a break and not the hours of the shift because of the silly maccas xpaths
    if hour_element.text.__contains__("-"):
        print("element is break, now moving to next element")
        xpath = xpath.split("/")
        xpath.pop(len(xpath)-1)
        xpath.append('span[5]')
        xpath = ('/').join(xpath)

    hour_element = driver.find_element(By.XPATH, xpath)
    actions.move_to_element(hour_element).perform()
    hours = hour_element.text

    #taking raw hours from string of how many hours
    hours = hours.split('h')
    hours = hours.pop(0)
    hours = hours.split(':')
    hours[1] = int(hours[1])/60
    hours = float(hours[0]) + float(hours[1])

    day_and_hours = [day, hours]
    return day_and_hours

def get_shifts():
    #this is like the base xpath itll get changed around and stuff
    shift_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[2]'
    #shift length xpath:
    #/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[4]
    #normal shift xpath
    #/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[2]
    #to get to the next week you just add a div[3] onto the end
                #/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]/span[2]
                #/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]/span[2]

    #empty dictionary for shifts and hours
    shifts = {}
    hours = {}

    #do this max 10 times cus cant do more than 5 shifts in a week and like it can be 2 weeks 
    for i in range(1, 11):
        #check if that shit exists cus if it dont we fucked        
        element_exists = check_exists_by_xpath(shift_xpath)
        if element_exists == True:
            #make the shift
            shifts[f"shift{i}"] = create_shift(shift_xpath)
            #get the hours
            hours[f"shift{i}"] = get_hours(shift_xpath)

            #change the xpath around, basically just adding another div[2]
            shift_xpath = shift_xpath.split("/")
            shift_xpath.insert(len(shift_xpath)-1, 'div[2]')
            shift_xpath = '/'.join(shift_xpath)
        else:
            shift_xpath = shift_xpath.split("/")
            shift_xpath.insert(len(shift_xpath)-1, 'div[3]')
            shift_xpath = '/'.join(shift_xpath)
            element_exists = check_exists_by_xpath(shift_xpath)

            if element_exists == True:
                continue
            else:
                break

    return shifts, hours

#puts date right 
def format_date(date):
    date_time_obj = datetime.datetime.strptime(date, '%I:%M %p %A %d/%b/%Y')
    date = date_time_obj.strftime('%m/%d/%y %H:%M')
    date = date.split(' ')
    return date

def get_ready_for_csv(shift):
    csv_line = ['Miles Work']
    shift_start = format_date(shift['start'])
    shift_end = format_date(shift['end'])
    csv_line = csv_line + shift_start + shift_end
    with open('roster.csv', 'a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_line)

def write_to_roster_csv(shifts):
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time']

    #clears it
    open('roster.csv', 'w').close()
    #opens to write to the file
    with open('roster.csv', 'a', encoding="UTF8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    #do it until no more shifts
    for i in range(1, 6):
        if f"shift{i}" in shifts:
            shift = shifts[f'shift{i}']
            get_ready_for_csv(shift)
        else:
            break

def import_to_calendar():
    driver.get("https://calendar.google.com/calendar/u/0/r")
    time.sleep(5)
    click_button("/html/body/div[2]/div[1]/div[1]/header/div[2]/div[2]/div[3]/div/div/div[4]/div")
    time.sleep(1)
    click_button("/html/body/div[21]/div/div/span[1]")
    time.sleep(1)
    click_button("/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[5]")
    time.sleep(1)
    # file_upload = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/form/label")
    # file_upload.send_keys("roster.csv")

def format_hours(hours):
    # create empty lists to append into
    shift_lengths = []
    day = []
    pay_types = []
    pay_amt = []
    shifts = []
    
    # add each shift as header
    for i in range(1, len(hours) + 1):
        shifts.append(f"shift{i}")

    #append hours and what day to appropriate lists
    for i in range(1, len(hours) + 1):
        day.append(hours[f"shift{i}"][0])
        shift_lengths.append(hours[f"shift{i}"][1])

    # sum the hours foe a total and put it at the end of the list
    total_hours = math.fsum(shift_lengths)
    shift_lengths.append(total_hours)

    # classify pay rate and add to list
    for i in range(0, len(day)):
        if day[i] == "Saturday" or day[i] == "Sunday":
            pay_types.append("weekend")
        else:
            pay_types.append("regular")

    # calculate pay using pay rates and hours and add t list
    for i in range(0, len(pay_types)):
        if pay_types[i] == "regular":
            pay_amt.append(round(14.03 * shift_lengths[i], 2))
        else:
            pay_amt.append(round(17.5375 * shift_lengths[i], 2))
    
    #sum pay and add to end of list
    total_pay = sum(pay_amt)
    pay_amt.append(total_pay)

    # some extra formatting
    shifts.append("total")
    shift_lengths.insert(0, "hours")
    pay_amt.insert(0, "pay")
    pay_types.insert(0, "pay type")
    shifts.insert(0, "shifts")
    day.insert(0, "day")

    # put it all into a dictionary to unpack in seperate funtion
    data = {
        "day": day,
        "shift_lengths": shift_lengths,
        "pay_types": pay_types,
        "pay_amt": pay_amt,
        "shifts": shifts
        }
    return data

def write_to_data_csv(data):
    # unpack dictionary into seperate cariables
    day = data["day"]
    shift_lengths = data["shift_lengths"]
    pay_types = data["pay_types"]
    pay_amt = data["pay_amt"]
    shifts = data["shifts"]

    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    # write it all to the csv
    with open(f'data/week_of_{last_monday}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(shifts)
        writer.writerow(day)
        writer.writerow(shift_lengths)
        writer.writerow(pay_types)
        writer.writerow(pay_amt)



#for the stupid maccas website to work you gotta sign in to google through them then do it all again so this is why im doing this
navigate_maccas_sign_in()

google_sign_in()

#remove this it dont ask you the second time
xpaths.remove('//*[@id="btnSetPopup"]')

navigate_maccas_sign_in()

time.sleep(15)

navigate_myjob()

shifts_and_hours = get_shifts()

shifts = shifts_and_hours[0]

hours = shifts_and_hours[1]

write_to_roster_csv(shifts)

import_to_calendar()

data = format_hours(hours)

write_to_data_csv(data)

##last span, number 2 is the start number 3 is end
##to get to next shift just add another div[2]/ before span
#first shift start
#/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[2]
#first shift end
#/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[3]
#second shift start
#/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/span[2]
#second shift end
#/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/span[3]

# import modules
import time
import csv
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
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

        time.sleep(3)

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
    # driver.execute_script("document.body.style.zoom='25%'")
    time.sleep(1)



def create_shift(xpath):
    time.sleep(1)
    #empty dictionary for shifts to go into
    shift = {}

    #finding the element of the shift
    shift_element = driver.find_element(By.XPATH, xpath)
    #scrolling down to it cus if its off screen it dont find it
    actions.move_to_element(shift_element).perform()
    #throw it in that dictionary YEAH BABY
    shift["start"] = shift_element.text
    print(shift_element.text)

    #change the xpath around replacing the end span[2] with a span[3]
    xpath = xpath.split('/')
    xpath[len(xpath)-1] = 'span[3]'
    xpath = '/'.join(xpath)
    
    #this bits the same as the top one you can read
    shift_element = driver.find_element(By.XPATH, xpath)
    actions.move_to_element(shift_element).perform()
    shift["end"] = shift_element.text
    print(shift_element.text)

    
    return shift
    





    
#where we up to:
#   using the long ass xcode address to get a shift start or end
#   the if function checks if that element exists then if it does runs create_shift
#   then splits the shift_xpath for modification before the next shift is generated
def get_shifts():
    #this is like the base xpath itll get changed around and stuff
    shift_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[2]'
                # /html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[2]
    #how fun the next week you just add a div[3] onto the end
                #/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]/span[2]
                #/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]/span[2]
    #empty dictionary for shifts
    shifts = {}

    #do this max 10 times cus cant do more than 5 shifts in a week and like it can be 2 weeks yk 
    for i in range(1, 11):
        #check if that shit exists cus if it dont we fucked        
        element_exists = check_exists_by_xpath(shift_xpath)
        if element_exists == True:
            print(shift_xpath)
            #make tha shift
            shifts[f"shift{i}"] = create_shift(shift_xpath)
            print(shifts)
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

    return shifts

#puts date right 
def format_date(date):
    date_time_obj = datetime.datetime.strptime(date, '%I:%M %p %A %d/%b/%Y')
    date = date_time_obj.strftime('%m/%d/%y %H:%M')
    date = date.split(' ')
    return date



#this is spitting out nested lists idk why anyway im going to bed
def get_ready_for_csv(shift):
    csv_line = ['Miles Work']
    shift_start = format_date(shift['start'])
    shift_end = format_date(shift['end'])
    csv_line = csv_line + shift_start + shift_end
    with open('roster.csv', 'a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_line)

def write_to_csv(shifts):
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time']

    open('roster.csv', 'w').close()
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
    #this is not right xpath for the thing or idk its not working
    file_upload = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/form/label")
    file_upload.send_keys("roster.csv")



#for the stupid maccas website to work you gotta sign in to google through them then do it all again so this is why im doing this
navigate_maccas_sign_in()

google_sign_in()

#remove this it dont ask you the second time
xpaths.remove('//*[@id="btnSetPopup"]')

navigate_maccas_sign_in()

time.sleep(15)

navigate_myjob()

shifts = get_shifts()

write_to_csv(shifts)

import_to_calendar()


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
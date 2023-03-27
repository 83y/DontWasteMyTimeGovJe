from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime, date
from discord_webhook import DiscordWebhook, DiscordEmbed
import calendar
import time

dateToFind = str(input("Enter a date you are looking to find a test before (format must be eg.(25/1/2023)): "))
dateToFind = datetime.strptime(dateToFind, '%d/%m/%Y')
waitTime = int(input("Enter the amount of time you want to be searching before the date you just inputted (eg. 12 months): "))
hook = str(input("Enter your discord webhook (this is what will message you): "))
last = str(input("Last name: "))
driverno = str(input("Driver no: "))
postcode = str(input("Postcode: "))
today = date.today()

d1 = today.strftime("%m")
d2 = int(d1)
d3 = calendar.month_name[d2]
d3 = str(d3)
y1 = today.strftime("%Y")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def main(dateToFind, waitTime, hook):
    webhook = DiscordWebhook(url=hook)
    availableDates = []
    datesFound = []
    driver.get("https://www.gov.je/dvs/pages/bookyourtestonline.aspx")

    time.sleep(10)

    lastName = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$txtSurname")
    lastName.send_keys(last)
    Licence = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$txtLicenceNo")
    Licence.send_keys(driverno)
    Postcode = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$txtPostcode")
    Postcode.send_keys(postcode)
    checkBox = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$chbLoginAgree")
    checkBox.click()
    checkBox.send_keys(Keys.RETURN)

    time.sleep(3)

    changeTest = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$rptSummaryExistingBookingsPractical$ctl01$btnSummaryBookingChange")
    changeTest.click()

    time.sleep(2)

    amendDate = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$bacAmend$btnAmendChange")
    amendDate.click()
    found = False
    counter = 0
    while found == False:
        if counter == waitTime:
            found == True
            break
        available = driver.find_elements(By.XPATH, "//div[@class='available']")
        for span in available:
            getDate = driver.find_element("id", "ctl00_PlaceHolderMain_Booking1_bacAmend_cmucAmendCalendar_lblMonthName").get_attribute("innerHTML")
            holder = span.text
            newHolder = holder.split("\n")
            newerHolder = newHolder[0] # Lol this code is so dumb and I know it
            newDate = newerHolder+" "+getDate
            splitDate = newDate.split(" ")
            datetime_object = datetime.strptime(splitDate[1], "%B")
            month_number = datetime_object.month
            month_number = str(month_number)
            newDate = str(splitDate[0]+"/"+month_number+"/"+splitDate[2])
            availableDates.append(newDate)
        prev = driver.find_element("name", "ctl00$PlaceHolderMain$Booking1$bacAmend$cmucAmendCalendar$btnPrevious")
        prev.click()
        counter += 1
        time.sleep(2)
    for date in range(len(availableDates)):
        newDate = datetime.strptime(availableDates[date], '%d/%m/%Y')
        newDate = str(newDate)
        dateToFind = str(dateToFind)
        if newDate < dateToFind:
            foundDate = False
            for i in datesFound:
                newDate = str(newDate)
                if i == newDate:
                    foundDate = True
                    break
            if foundDate == False:
                datesFound.append(str(newDate))
                embed = DiscordEmbed(title="Found Test @83y")
                embed.set_author(name="83y")
                embed.set_footer(text=str(newDate))
                webhook.add_embed(embed)
    try:
        webhook.execute()
    except:
        pass
    webhook = ""
    main(dateToFind, waitTime, hook)

main(dateToFind, waitTime, hook)

from calendar import calendar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime


login_info = {}
login_info["abdullah"] = ("abdullah.shah@qalamseminary.com", "Qalam#2024")
login_info["saqib"] = ("mian.saqib@qalamseminary.com", "Zehra1029!")
login_info["shaji"] = ("shaji.ul-islam@qalamseminary.com", "tyctej-jynhu9-mlbjez")

# user = 'saqib'
#TODO: pass in user as cmd arg?

def log(string):
  print(string, datetime.datetime.now().time())

def login(driver, user):
  log('Starting Login Operation')
  driver.get("https://qalam.seats.cloud/")

  # Wait for username field to be present
  username_field = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "UserName"))
  )

  username = login_info[user][0]

  username_field.send_keys(username)

  log(f'Logging in for user {username}')


  # Wait for password field to be present
  password_field = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "Password"))
  )
  password_field.send_keys(login_info[user][1])

  # Submit the login form
  submit_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
  submit_button.click()
  log('Finished Login Operation')

def click_calendar_button(driver):
  log('Starting Calendar Button Click Operation')
  # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "mdc-tab.mat-mdc-tab-link.mat-mdc-focus-indicator"))).click()
  driver.find_elements(By.CLASS_NAME, "mdc-tab.mat-mdc-tab-link.mat-mdc-focus-indicator")[1].click()
  log('Finished Calendar Button Click Operation')


def click_month_then_week(driver):
  log('clcking month then week')
  driver.find_elements(By.CLASS_NAME, "fc-dayGridMonth-button.fc-button.fc-button-primary")[0].click()
  time.sleep(1)
  driver.find_elements(By.CLASS_NAME, "fc-timeGridWeek-button.fc-button.fc-button-primary")[0].click()
  log('finished clcking month then week')
  
 
def find_todays_classes(driver):
  log("finding today's classes")
  # print(datetime.date.today().strftime('%A')[:3].lower())
  day = datetime.date.today().strftime('%A')[:3].lower()
  # day = "mon"

  today_object = driver.find_element(By.CLASS_NAME, f"fc-day.fc-day-{day}.fc-day-today.fc-timegrid-col")
  # today_object = driver.find_element(By.TAG_NAME, datetime.date.today().strftime('%Y-%m-%d'))

  # classes_objects = today_object.find_elements(By.CLASS_NAME, "fc-event-card.flex-container.success-event")

  classes_objects = today_object.find_elements(By.CLASS_NAME, "fc-event-card.flex-container")

  time.sleep(1)

  print("num of classes:", len(classes_objects))
  for qalam_class in classes_objects:
    title = qalam_class.get_attribute("title")

    # print("color:", qalam_class.value_of_css_property("background-color"))
    # if 'Absent' in title:
    # if 'Marked as Attended' in title:
    if title.startswith('Scheduled'):
      print(title)
    
      # get pop-up for last class
      # classes_objects[-1].click()
      qalam_class.click()
      time.sleep(2)

      # click on link
      # class_info is just "Class Link" and "Marked"
      class_link_object = driver.find_elements(By.CLASS_NAME, "div-row.ng-star-inserted")[0]

      join_link = class_link_object.find_element(By.CLASS_NAME, "font-title")
      join_link.click()

      # buffer time to see second tab opening - can delete
      time.sleep(1)

      # Closes second tab
      driver.switch_to.window(driver.window_handles[0])

      time.sleep(1)
      break

    # driver.close()
    # driver.switch_to.window(first_tab)

  log("finished today's classes")


for user in login_info.keys():
  if user == 'shaji':
    print('skipping shaji')
    break
  driver = webdriver.Chrome()
  login(driver, user)
  time.sleep(3)
  click_calendar_button(driver)
  time.sleep(3)
  # If sunday then click month button then week button cuz the website is retarded (it doesn't populate sun classes unless month button is clicked first)
  if datetime.date.today().strftime('%A')[:3].lower() == "sun":
    click_month_then_week(driver)
  time.sleep(2)
  find_todays_classes(driver)
  time.sleep(3)
  driver.close()
  print('-------------------------')
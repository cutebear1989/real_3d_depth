import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import cv2
from selenium.webdriver.support.ui import Select

key_names = ["text", "checkbox", "radio", "href", "select"]
resize_ratio = 2
def simulate_typing(driver, element, text, delay=0.1):
    x = 7
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.click(element)
    actions.pause(delay)
    for letter in text:
        actions.send_keys(letter)
        actions.pause(delay)
    actions.perform()
def simulate_typing_1(driver, element, text, delay=0.1):
    x = 7
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.click(element)
    actions.pause(delay)
    for letter in text:
        actions.send_keys(letter)
        actions.pause(delay)
    actions.perform()

def draw_rectangle(image, rect, index, type):
    x, y, height, width = int(rect['x']), int(rect['y']), int(rect['height']), int(rect['width'])
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
    cv2.putText(image, type + " " + index, (x, y + height), 0, 0.8, (255, 0, 0), thickness=2, lineType=cv2.FILLED)
def draw_rectangle_1(image, rect, index, type):
    x, y, height, width = int(rect['x']), int(rect['y']), int(rect['height']), int(rect['width'])
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
    cv2.putText(image, type + " " + index, (x, y + height), 0, 0.8, (255, 0, 0), thickness=2, lineType=cv2.FILLED)


def remove_elements(elements):
    displayed_elements = []
    for element in elements:
        if element.is_displayed():
            # Get the location of the element
            location = element.location
            x, y = location['x'], location['y']
            if x == 0 and y == 0:
                continue
            displayed_elements.append(element)
    return displayed_elements

def order_elements(elements):
    for i in range(len(elements) - 1):
        for j in range(i + 1, len(elements)):
            location1 = elements[i].location
            x1, y1 = location1['x'], location1['y']
            location2 = elements[j].location
            x2, y2 = location2['x'], location2['y']
            if y1 > y2:
                temp = elements[j]
                elements[j] = elements[i]
                elements[i] = temp
                continue
            if y1 == y2 and x1 > x2:
                temp = elements[j]
                elements[j] = elements[i]
                elements[i] = temp
    return elements

def find_all_elements(driver):
    elements = {}
    text_elements = driver.find_elements(By.XPATH, "//input[@type='text']")
    text_elements = remove_elements(text_elements)
    text_elements = order_elements(text_elements)

    textarea_elements = driver.find_elements(By.TAG_NAME, "textarea")
    textarea_elements = remove_elements(textarea_elements)
    textarea_elements = order_elements(textarea_elements)
    elements["text"] = text_elements + textarea_elements

    checkbox_elements = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    checkbox_elements = remove_elements(checkbox_elements)
    checkbox_elements = order_elements(checkbox_elements)
    elements["checkbox"] = checkbox_elements

    radio_elements = driver.find_elements(By.XPATH, "//input[@type='radio']")
    radio_elements = remove_elements(radio_elements)
    radio_elements = order_elements(radio_elements)
    elements["radio"] = radio_elements

    href_elements = driver.find_elements(By.XPATH, "//a[@href]")
    href_elements = remove_elements(href_elements)
    # href_elements = order_elements(href_elements)
    elements["href"] = href_elements

    select_elements = driver.find_elements(By.XPATH, "//select")
    select_elements = remove_elements(select_elements)
    select_elements = order_elements(select_elements)
    elements["select"] = select_elements
    return elements

def draw_elements(img, elements):
    for key in key_names:
        rows = elements[key]
        count = 0
        for row in rows:
            count += 1
            draw_rectangle(img, row.rect, str(count), key)

if __name__ == '__main__':
    chromeoption = Options()
    # chromeoption.add_argument('--headless')
    driver = webdriver.Chrome(options=chromeoption)
    driver.maximize_window()

    website_url = 'https://www.w3schools.com/howto/howto_css_custom_checkbox.asp'
    website_url = "https://www.w3schools.com/howto/howto_css_checkout_form.asp"
    website_url = "https://www.w3schools.com/howto/howto_css_fixed_menu.asp#gsc.tab=0"
    website_url = "https://www.w3schools.com/howto/howto_css_dropdown.asp"
    website_url = "https://www.w3schools.com/bootstrap5/bootstrap_form_select.php"
    website_url = "https://speech.microsoft.com/portal/pronunciationassessmenttool"
    website_url = "https://demoqa.com/automation-practice-form"
    website_url = "https://www.ebay.com/"
    #website_url = "https://flickr.com/"
    #website_url = "https://www.slideshare.net/"
    driver.get(website_url)
    time.sleep(1)
    driver.save_screenshot("web.png")
    img = cv2.imread("web.png")
    h, w, c = img.shape
    elements = find_all_elements(driver)
    show_img = img.copy()
    draw_elements(show_img, elements)
    show_img = cv2.resize(show_img, (int(w / resize_ratio), int(w / resize_ratio)))
    cv2.imshow("locations", show_img)
    cv2.waitKey(1)
    while(True):
        inputs = input("Enter the input type and index: ")
        try:
            args = inputs.split(" ")
            type = args[0]
            if type == "quit":
                break
            element_num = int(args[1]) - 1
            displayed_elements = elements[type]

            if type == "checkbox" or type == "radio" or type == "href":
                if 0 <= element_num < len(displayed_elements):
                    displayed_elements[element_num].click()
                    print(f"{type} {element_num + 1} clicked successfully!")
                else:
                    print(f"Invalid {type} index provided!")
            if type == "select":
                if 0 <= element_num < len(displayed_elements):
                    # selected_option_list = displayed_elements[element_num].getAllSelectedOptions()
                    index = int(args[2])
                    displayed_elements[element_num].click()
                    time.sleep(2)
                    dropdown = Select(displayed_elements[element_num])

                    # dropdown.click()
                    # time.sleep(2)
                    # Get the list of options
                    options = dropdown.options
                    # Get the number of options

                    if 0 <= index - 1 < len(options):
                        dropdown.select_by_index(index - 1)
                        displayed_elements[element_num].click()
                        print(f"{type} {index} clicked successfully!")
                    else:
                        print(f"Invalid index provided!")
            if type == "text":
                desired_string = "Hello, World!"
                text_to_enter = ""
                for i in range(2, len(args)):
                    text_to_enter = text_to_enter + " " + args[i]
                text_to_enter = text_to_enter.strip()
                print("text", text_to_enter)
                if 0 <= element_num < len(displayed_elements):
                    simulate_typing(driver, displayed_elements[element_num], text_to_enter)

                    # displayed_elements[element_num].send_keys(str_val)
                    print(f"Text {element_num + 1} entered successfully!")
                else:
                    print("Invalid text index provided!")
        except:
            print("Invalid command!")
            continue
        # driver.save_screenshot("web.png")
        # img = cv2.imread("web.png")
        # show_img = img.copy()
        # draw_elements(show_img, elements)
        # cv2.imshow("locations", show_img)
        # cv2.waitKey(0)

    # Close the browser
    driver.quit()

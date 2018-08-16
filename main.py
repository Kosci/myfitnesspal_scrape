from selenium import webdriver
from datetime import date, timedelta
import db_manager


def login(browser, usr_val, pwd_val):
    login_btn = browser.find_element_by_class_name('fancylink')
    login_btn.click()

    usr_fld = browser.find_element_by_name('username')
    pwd_fld = browser.find_element_by_name('password')
    usr_fld.send_keys(usr_val)
    pwd_fld.send_keys(pwd_val)
    pwd_fld.submit()


def strip_table(browser, cur_list):
    try:
        next_page_btn = browser.find_element_by_class_name('next_page')
        tbl = browser.find_elements_by_class_name('col-num')
        for each in tbl:
            if _num_there(each.text):
                cur_list.append(each.text)
        next_page_btn.click()
        strip_table(browser, cur_list)
    except:
        tbl = browser.find_elements_by_class_name('col-num')
        for each in tbl:
            if _num_there(each.text):
                cur_list.append(each.text)

    return cur_list


def _num_there(s):
    return any(i.isdigit() for i in s)


def load_printable_diary(browser, start_date, end_date, category):
    link = 'https://www.myfitnesspal.com/reports/printable_diary'
    browser.get(link)

    if category == 'food':
        browser.find_element_by_id('show_exercise_diary').click()
    else:
        browser.find_element_by_id('show_food_diary').click()

    browser.find_element_by_id('show_food_notes').click()
    browser.find_element_by_id('show_exercise_notes').click()

    from_fld = browser.find_element_by_id('from')
    from_fld.clear()
    from_fld.send_keys(start_date)

    to_fld = browser.find_element_by_id('to')
    to_fld.clear()
    to_fld.send_keys(end_date)
    to_fld.submit()

    strip_printable_diary(browser)


def strip_printable_diary(browser):
    test = browser.find_elements_by_tag_name('tfoot')
    d1 = date(2018, 7, 15)
    d2 = date(2018, 8, 15)
    t = all_days(d1, d2)
    for each, day in zip(test, t):
        db_manager.create_entry(day, '', '', each.text)



def all_days(start_date, end_date):
    days = []

    delta = end_date - start_date
    for i in range(delta.days + 1):
        days.append(start_date + timedelta(i))

    return days


def main():
    browser = webdriver.Chrome(
        executable_path='C:/Users/bkosciolek/Desktop/chromedriver.exe'
    )
    browser.get('https://myfitnesspal.com/')
    login(browser, 'email_temp_filler', 'password_temp_filler')
    #
    # browser.get('https://www.myfitnesspal.com/measurements/edit')
    # weight_date = strip_table(browser, [])
    # dropdown = browser.find_element_by_class_name('select')
    # dropdown.send_keys('Waist')
    # dropdown.submit()
    # waist_date = strip_table(browser, [])
    # print(weight_date)
    # print(waist_date)

    d1 = date(2018, 7, 15)
    d2 = date(2018, 8, 15)
    load_printable_diary(browser, str(d1), str(d2), 'food')




if __name__ == "__main__":
    main()
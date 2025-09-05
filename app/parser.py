import time

import fake_useragent
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode

targets = {
    '2025-09-06': {
        ('Брест', 'Минск'): {
            '728Б': [1],
            '734Б': [1, 2]
        },
        ('Минск', 'Москва'): {
            '028Б': [3, 4, 5],
            '148Ч': [6, 7],
            '002Б': [8, 9]
        }
    },
    '2025-09-07': {
        ('Брест', 'Минск'): {
            '738Б': [10, 11],
            '702Б': [12, 13],
            '738Ф': [14, 15]
        },
        ('Минск', 'Москва'): {
            '718Б': [16, 17],
            '722Б': [18, 19, 20]
        }
    }
}

current_free_seats = {}

def get_free_seats_in_train(page, trains) -> dict[str, list]:
    res = {}
    for train, user_ids in trains.items():
        time.sleep(3)
        page.go_back()

    return res

def reject_cookies(page):
    time.sleep(2)
    if page.locator("button.btn.btn-index.mc-decline-all").count() > 0:
        page.click(".btn.btn-index.mc-decline-all")

def get_free_seats_in_day(date, dicts) -> dict[(str, str), dict[str, list]]:
    res = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        user_agent = fake_useragent.UserAgent().random
        context = browser.new_context(user_agent=user_agent)

        for (cityA, cityB), trains in dicts.items():
            page = context.new_page()

            base_url = 'https://pass.rw.by/ru/route/'
            params = {
                'from': cityA,
                'to': cityB,
                'date': date
            }
            full_url = f"{base_url}?{urlencode(params)}"
            page.goto(full_url)

            reject_cookies(page)

            res[(cityA, cityB)] = get_free_seats_in_train(page, trains)

    return res

def precalc():
    for date, dicts in targets.items():
        current_free_seats[date] = get_free_seats_in_day(date, dicts)

if __name__ == '__main__':
    precalc()

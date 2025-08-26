from scrapling.fetchers import StealthyFetcher
from playwright.sync_api import Page, expect
from colorama import Fore, Back, Style
import logging
import json
logging.getLogger("scrapling").setLevel(logging.ERROR)


def scroll_login(page: Page):
    def handle_response(response):
        if("endpoint-intercept/" in response.url):
            print(response.json())
    page.on("response", handle_response)


    try:
        page.get_by_role("textbox", name="email").click()
        page.get_by_role("textbox", name="email").fill("correo@target.test")
        page.get_by_role("textbox", name="password").click()
        page.get_by_role("textbox", name="password").fill("Password123!$")
        page.get_by_role("button", name="Ingresar").click()
        #page.wait_for_timeout(1000)

    except Exception:
        pass

    try:
        expect(page.get_by_text("Texto a esperar")).to_be_visible()
        return page

    except Exception:
        return page


page = StealthyFetcher.fetch('https://target.com.test/login',
    page_action=scroll_login,
    headless=False,
    humanize=True,
    os_randomize=True
)

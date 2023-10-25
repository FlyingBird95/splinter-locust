import logging
from http import HTTPStatus
from typing import Optional, TYPE_CHECKING

from locust.clients import HttpSession, LocustResponse
from requests.exceptions import RequestException
from requests.models import Request
from splinter import Browser
from splinter.element_list import ElementList
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from urllib3 import PoolManager

if TYPE_CHECKING:
    from .user import SplinterLocustUser  # prevent circular import


logger = logging.getLogger()


class SplinterLocustClient(HttpSession):
    def __init__(
        self,
        base_url: str,
        request_event,
        user: "SplinterLocustUser",
        pool_manager: Optional[PoolManager] = None,
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            request_event=request_event,
            user=user,
            pool_manager=pool_manager,
            **kwargs,
        )
        
        options = webdriver.ChromeOptions()
        if not self.user.show_browser:
            options.add_argument('headless')
        options.add_argument(f'window-size={self.user.screen_width}x{self.user.screen_height}')
        options.add_argument('disable-gpu')
        
        self.browser = Browser("chrome", options=options)
        self.wait = WebDriverWait(self.browser.driver, self.user.wait_timeout)
    
    def wait_until_xpath_present(self, xpath: str):
        return self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    
    def _send_request_safe_mode(self, method, url, **kwargs):
        """Override HttpSession._send_request_safe_mode, since the request is redirected to Splinter."""
        assert method == "GET", "Method is not supported."
        response = LocustResponse()
        response.request = Request(method, url).prepare()
        
        try:
            self.browser.visit(url)
        except RequestException as e:
            logger.exception(e)
            response.error = e
            response.status_code = 0  # with this status_code, content returns None
        else:
            # Selenium does not return any status codes.
            # If the visit() doesn't throw an error, assume it was successful.
            response.status_code = HTTPStatus.OK
        return response
    
    def click_element(self, element: ElementList):
        response = LocustResponse()
        
        try:
            element.click()
        except Exception as e:
            logger.exception(e)
            response.error = e
            response.status_code = 0  # with this status_code, content returns None
        else:
            response.request = Request(self.browser.driver.method, self.browser.driver.current_url).prepare()
            response.status_code = 200
        
        return response
    
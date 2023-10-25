"""This is an example locust file, and is intended to demonstrate the package.

Run using the following command:
    locust --host https://locust.io --run-time 5s --headless
"""

from locust import TaskSet, task

from splinter_locust import SplinterLocustUser


class VisitLocustWebsite(TaskSet):
    
    @task
    def visit_locust_website(self):
        """Visit the homepage of locust.io"""
        self.client.get("/")
        assert self.client.wait_until_xpath_present("//h1[text()='An open source load testing tool.']")
    
    @task
    def click_documentation_button(self):
        """Click the documentation link and verify that we're on the documentation page."""
        element = self.client.browser.find_by_xpath("//a[text()='Documentation']")
        
        self.client.click_element(element)
        
        assert self.client.wait_until_xpath_present("//h1[contains(text(), 'Locust Documentation')]")


class MyUser(SplinterLocustUser):
    show_browser = False  # Don't show browser. It means something else than --headless.
    
    tasks = [VisitLocustWebsite]

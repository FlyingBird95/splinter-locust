from locust import HttpUser

from .client import SplinterLocustClient


class SplinterLocustUser(HttpUser):
    abstract = True
    
    wait_timeout = 10  # in seconds
    screen_width = 1400  # in pixels
    screen_height = 800  # in pixels
    show_browser = True
    
    def __init__(self, environment):
        super().__init__(environment=environment)
        
        self.client = SplinterLocustClient(
            base_url=self.host,
            request_event=self.environment.events.request,
            user=self,
            pool_manager=self.pool_manager,
        )
    
    def on_stop(self):
        self.client.browser.quit()

# Splinter Locust
Make [Locust](https://locust.io/) work with UI interactions using [Splinter](http://splinter.readthedocs.org/en/latest/index.html).

## Why Splinter Locust?
[Locust](https://locust.io/) is an open source load testing tool. It is an easy to use, 
scriptable and scalable performance testing tool. 
According to their [documentation](https://docs.locust.io/en/stable/what-is-locust.html), the behaviour of your users
should be defined in Python code, instead of being stuck in a UI or restrictive domain specific language.

This works great for [REST APIs](https://en.wikipedia.org/wiki/REST), which are often used for the backend of a 
web application. However, it is not enough to test only the backend, since _the behaviour of users_ also involves 
interacting with the frontend. 
This is where [Splinter](http://splinter.readthedocs.org/en/latest/index.html) is designed for. 
It is easy to use, powerful and flexible at the same time.

It is not easy to combine both frameworks, since they have different purposes. That's where Splinter Locust comes in. 
It aims to define a connection between Splinter and Locust (it's in the name). Without any configuration, 
a browser is created by Locust, which can be accessed using conventional methods offered by Splinter.
Time for an example:

## Example
The following `locustfile.py` shows how easy it is to interact with the response. 
More examples can be found in the [/examples](/examples)-folder.

```python
from locust import SequentialTaskSet, task

from splinter_locust import SplinterLocustUser


class VisitLocustWebsite(SequentialTaskSet):
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
    show_browser = False

    tasks = [VisitLocustWebsite]
```

This example can be executed in Locust using the following command:

```shell
locust --host https://locust.io --run-time 5s  --headless
```

## Installation
Installation is easy via `pip`:

```shell
pip install splinter-locust
```
*Note: this doesn't work yet, since this package is still under active development.* 

## Development
Contributions to this package are much appreciated. In order to get started, execute the following commands:
1. Clone the repository:
   ```shell
   git clone git@github.com:FlyingBird95/splinter-locust.git
   ```
2. Move into the directory:
   ```shell
   cd splinter-locust
   ```
3. Install dependencies (virtualenv, python dependencies and pre-commit hooks) via a simple make command:
   ```shell
   make develop
   ```

## Future developments
In order to make this package even more useful, the following developments are on the roadmap:
- Support different browsers.
- Add more functionality to `SplinterLocustClient`.
- Add unit tests using `pytest`.
- Configure CI using Github Actions.
- Also let me know what functionality you would like to have by creating [an issue](/issues/new).
🚀 Python + Playwright + MCP + AI: End‑to‑End Guide for Automatic Test Script Generation
This guide explains how to upgrade an existing Python + Pytest + Playwright project (such as sloth-python) to support AI‑driven test script generation using:
- Python
- Playwright
- MCP (Model Context Protocol)
- AI (OpenAI / Anthropic / Azure)
We will use Tangerine’s Homepage, Sign‑In Page, and Sign‑Up Page as the demo targets.

🧭 Overview
The goal is to enable the following workflow:
- Playwright launches a browser
- MCP exposes the browser context (DOM, screenshot, network logs)
- AI reads the real page context
- AI generates Playwright test scripts automatically
- (Optional) AI self‑heals selectors when tests fail
This is currently one of the most practical and modern approaches to AI‑assisted test automation.

🧱 Step 1 — Add MCP Client to Your Project
Install the MCP Python SDK:
pip install mcp


Create a file such as:
sloth/mcp_server.py


Example structure:
from mcp import MCPServer

class SlothMCPServer(MCPServer):
    def __init__(self, page):
        super().__init__()
        self.page = page

    async def get_dom(self):
        return await self.page.content()

    async def get_element_tree(self):
        return await self.page.evaluate("() => document.body.innerHTML")

    async def get_screenshot(self):
        return await self.page.screenshot()

    async def get_network_logs(self):
        return self.page.context.request


This exposes the browser context to AI through MCP.

🧱 Step 2 — Attach MCP to Playwright Browser Session
Modify your pytest fixture (e.g., conftest.py) to start MCP when Playwright launches:
import pytest
from playwright.sync_api import sync_playwright
from sloth.mcp_server import SlothMCPServer

@pytest.fixture(scope="session")
def mcp_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        mcp = SlothMCPServer(page)
        mcp.start()

        yield page, mcp

        browser.close()


Now AI can access:
- DOM
- Element tree
- Screenshot
- Network logs
This is the foundation for AI‑generated scripts.

🧱 Step 3 — Build an AI Agent to Generate Playwright Scripts
Create a file:
sloth/ai_agent.py


Example:
from openai import OpenAI

class SlothAIAgent:
    def __init__(self, mcp):
        self.mcp = mcp
        self.client = OpenAI()

    def generate_script(self, goal: str):
        dom = self.mcp.get_dom()
        screenshot = self.mcp.get_screenshot()

        prompt = f"""
You are an automation engineer.
Here is the DOM of the current page:
{dom}

Goal: {goal}

Generate a Python Playwright script that accomplishes this goal.
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message["content"]


This agent:
- Reads the real DOM
- Understands the page
- Generates Playwright code

🧱 Step 4 — Run Experiments on Tangerine Pages
Below are ready‑to‑run examples.

🟧 Experiment 1 — Generate Script for Tangerine Homepage
def test_generate_homepage_script(mcp_context):
    page, mcp = mcp_context

    page.goto("https://www.tangerine.ca/en")

    agent = SlothAIAgent(mcp)
    script = agent.generate_script(
        "Verify the homepage loads and the Sign In button is visible."
    )

    print(script)


Expected AI output:
def test_homepage(page):
    page.goto("https://www.tangerine.ca/en")
    assert page.locator("text=Sign In").is_visible()



🟧 Experiment 2 — Generate Script for Sign‑In Page
def test_generate_signin_script(mcp_context):
    page, mcp = mcp_context

    page.goto("https://www.tangerine.ca/app/#/login")

    agent = SlothAIAgent(mcp)
    script = agent.generate_script(
        "Fill username and password fields and click Sign In."
    )

    print(script)


Expected AI output:
def test_signin(page):
    page.goto("https://www.tangerine.ca/app/#/login")
    page.fill("#username", "test_user")
    page.fill("#password", "secret")
    page.click("button[type=submit]")



🟧 Experiment 3 — Generate Script for Sign‑Up Page
def test_generate_signup_script(mcp_context):
    page, mcp = mcp_context

    page.goto("https://www.tangerine.ca/app/#/signup")

    agent = SlothAIAgent(mcp)
    script = agent.generate_script(
        "Fill the signup form with fake data."
    )

    print(script)


Expected AI output:
def test_signup(page):
    page.goto("https://www.tangerine.ca/app/#/signup")
    page.fill("#firstName", "John")
    page.fill("#lastName", "Doe")
    page.fill("#email", "john@example.com")
    page.click("button[type=submit]")



🎯 Final Result
After following these steps, your project will support:
- AI‑generated Playwright test scripts
- AI understanding of real browser context via MCP
- AI‑selected stable locators
- AI‑assisted self‑healing (you already have this in sloth-python)
- A modern, AI‑driven automation workflow
This turns sloth-python into a cutting‑edge AI automation framework.

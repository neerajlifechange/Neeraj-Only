import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
import nest_asyncio
import getindianname as name  # Assuming you have a function to generate Indian names in this module

import random
nest_asyncio.apply()

# Flag to indicate whether the script is running
running = True

async def start(thread_name, user, wait_time, meetingcode, passcode):
    print(f"{thread_name} started!")

    async with async_playwright() as p:
        # Use Brave browser with specified executable path
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/brave-browser"
        )
        browser_type = p.chromium
        print(f"{thread_name} is using browser: {browser_type.name}")  # Print browser type
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'http://www.zoom.us/wc/join/{meetingcode}', timeout=200000)

        # ... rest of the code ...

        try:
            await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.click('//button[@id="wc_agree1"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.wait_for_selector('input[type="text"]', timeout=200000)
            await page.fill('input[type="text"]', user)
            await page.fill('input[type="password"]', passcode)
            join_button = await page.wait_for_selector('button.preview-join-button', timeout=200000)
            await join_button.click()
        except Exception as e:
            pass

        try:
            query = '//button[text()="Join Audio by Computer"]'
            await asyncio.sleep(13)
            mic_button_locator = await page.wait_for_selector(query, timeout=350000)
            await asyncio.sleep(10)
            await mic_button_locator.evaluate_handle('node => node.click()')
            print(f"{thread_name} microphone: Mic aayenge.")
        except Exception as e:
            print(f"{thread_name} microphone: Mic nahe aayenge. ", e)

        print(f"{thread_name} sleep for {wait_time} seconds ...")
        while running and wait_time > 0:
            await asyncio.sleep(1)
            wait_time -= 1
        print(f"{thread_name} ended!")

        await browser.close()

async def main():
    global running
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    with ThreadPoolExecutor(max_workers=number) as executor:
        loop = asyncio.get_running_loop()
        tasks = []
        for i in range(number):
            try:
                # Replace name.randname() with your getindianname function
                user = name.randndame()
            except IndexError:
                break
            task = loop.create_task(start(f'[Thread{i}]', user, wait_time, meetingcode, passcode))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            running = False
            # Wait for tasks to complete
            await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

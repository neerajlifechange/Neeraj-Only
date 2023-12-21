import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from faker import Faker
from playwright.async_api import async_playwright
import nest_asyncio

nest_asyncio.apply()

fake = Faker('en_IN')
MUTEX = threading.Lock()

def sync_print(text):
    with MUTEX:
        print(text)

async def grant_permissions(page):
    try:
        # Grant microphone permissions directly
        await page.context().override_permissions("https://zoom.us", ["microphone"])
        # Wait for the browser to prompt for microphone access
        await page.wait_for_selector('button[data-testid="preJoinTestButton"]', timeout=30000)
        # Increase the sleep duration to ensure all elements are loaded
        await asyncio.sleep(5)
        # Directly grant microphone permissions
        await page.context().override_permissions("https://zoom.us", ["microphone"])
        sync_print("Microphone permission granted pre-join.")
    except Exception as e:
        sync_print(f"Error granting microphone permission: {e}")

async def start(thread_name, wait_time, meetingcode, passcode):
    user = fake.name()
    sync_print(f"{thread_name} started! User: {user}")

    async with async_playwright() as p:
        # Modified lines
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/brave-browser"
        )
        browser_type = p.chromium
        print(f"{thread_name} is using browser: {browser_type.name}")

        context = await browser.new_context(permissions=['microphone'])
        page = await context.new_page()

        await grant_permissions(page)

        await page.goto(f'https://zoom.us/wc/join/{meetingcode}', timeout=200000)

        try:
            await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
        except:
            pass
        try:
            await page.click('//button[@id="wc_agree1"]', timeout=50000)
        except:
            pass

        await page.wait_for_selector('input[type="text"]', timeout=200000)
        await page.fill('input[type="text"]', user)
        await page.fill('input[type="password"]', passcode)
        join_button = await page.wait_for_selector('button.preview-join-button')
        await join_button.click()

        try:
            # Increase timeout if still mic missing on some users
            query = '//button[text()="Join Audio by Computer"]'
            mic_button_locator = await page.wait_for_selector(query, timeout=200000)
            await mic_button_locator.wait_for_element_state('stable', timeout=200000)
            await mic_button_locator.evaluate_handle('node => node.click()')
            sync_print(f"{thread_name} mic aayenge.")

            # Take a screenshot after clicking "Join Audio by Computer" button
            await page.screenshot(path=f"{thread_name}_after_join_audio.png")

        except Exception as e:
            print(e)
            sync_print(f"{thread_name} mic nhi aayenge.")

        # ... (remaining code)

        # Wait for 30 seconds
        await asyncio.sleep(30)

        # Take a screenshot after 30 seconds
        await page.screenshot(path=f"{thread_name}_after_30_seconds.png")

        sync_print(f"{thread_name} sleep for {wait_time} seconds ...")
        await asyncio.sleep(wait_time)
        sync_print(f"{thread_name} ended!")

        await browser.close()

async def main():
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 60
    wait_time = sec * 60

    with ThreadPoolExecutor(max_workers=number) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for i in range(number):
            task = loop.create_task(start(f'[Thread{i}]', wait_time, meetingcode, passcode))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

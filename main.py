import time

import vision
from vimbot import Vimbot

def main():
    print("Initializing the Vimbot driver...")
    driver = Vimbot() # playwrightの準備

    print("Navigating to Google...")
    driver.navigate("https://www.google.com") # ページ遷移

    objective = input("Please enter your objective: ")

    while True:
        input("Please enter and continue process.")
        print("Capturing the screen...")
        screenshot = driver.capture() # ページのスクリーンショットを撮る

        print("Getting actions for the given objective...")
        action = vision.get_actions(screenshot, objective) # 次のアクションを得る
        print(f"JSON Response: {action}")
        if driver.perform_action(action):  # returns True if done
            break

def main_entry():
    main()

if __name__ == "__main__":
    try:
        main_entry()
    except KeyboardInterrupt:
        print("Exiting...")

from smart_courier_app import SmartCourierApp
from config import DEFAULT_MAP_PATH

def main():
    print("Smart Courier Application")
    print(f"Mencari peta default: {DEFAULT_MAP_PATH}")
    app = SmartCourierApp()
    app.run()

if __name__ == "__main__":
    main()

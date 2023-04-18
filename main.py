import asyncio
import traceback
import data
import tests
from datetime import datetime


def printWithTime(text: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: {text}")


def askUserWhichApiToTest():
    while 1:
        print("On which API do you want to test the performance?")
        print("1 = GoAPI")
        print("2 = NodeJsAPI")
        print("3 = PythonAPI")
        inp = input()

        if inp == "1":
            print("Performance Test for GoAPI...")
            return 10000
        elif inp == "2":
            print("Performance Test for NodeJsAPI...")
            return 10000
        elif inp == "3":
            print("Performance Test for PythonAPI...")
            return 10000


if __name__ == "__main__":
    try:
        portToTest = askUserWhichApiToTest()
        streets = data.getStreetsFromCSV("STRASSE.csv", 100)
        asyncio.run(tests.runInsertTest(portToTest, streets, 5))
    except Exception:
        traceback.print_exc()

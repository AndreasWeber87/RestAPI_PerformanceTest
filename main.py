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
            return 7000
        elif inp == "2":
            print("Performance Test for NodeJsAPI...")
            return 8000
        elif inp == "3":
            print("Performance Test for PythonAPI...")
            return 9000


def askUserHowManyRecords():
    while 1:
        print("How many records do you want to use for the test?")
        inp = input()

        try:
            val = int(inp)
            if val < 1:
                continue
            return val
        except:
            pass


def askUserHowManyTasks():
    while 1:
        print("How many tasks do you want to use for the test?")
        inp = input()

        try:
            val = int(inp)
            if val < 1:
                continue
            return val
        except:
            pass


if __name__ == "__main__":
    try:
        #portToTest = askUserWhichApiToTest()
        #recordsCnt = askUserHowManyRecords()
        #tasksCnt = askUserHowManyTasks()
        portToTest = 10000
        recordsCnt = 100
        tasksCnt = 5

        streets = data.getStreetsFromCSV("STRASSE.csv", recordsCnt)
        asyncio.run(tests.runTest(tests.Testcategory.AddTest, portToTest, streets, tasksCnt))
    except Exception:
        traceback.print_exc()

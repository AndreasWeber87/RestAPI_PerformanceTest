import os


class Street:
    def __init__(self, skz: int, streetname: str):
        self.skz = skz
        self.streetname = streetname


def getStreetsFromCSV(filename: str, lines: int):
    if not os.path.exists(filename):
        raise Exception(f'File "{filename}" not exists!')

    streets = []

    with open(filename, "r", encoding="utf-8") as file:
        file.readline()
        for i in range(lines):
            line = file.readline()
            columns = line.split(";")

            skz = int(columns[0].replace('"', ''))
            streetname = columns[1].replace('"', '')
            streets.append(Street(skz, streetname))

    return streets

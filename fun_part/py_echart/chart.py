import json

from record import Record


# Read data from file and analize, then display in chart
class FileReader:
    def readData(self) -> list[Record]:
        pass


class TxtFileReader(FileReader):
    def __init__(self, filename: str):
        self.filename = filename

    def readData(self) -> list[Record]:
        file = open(self.filename, encoding="utf-8")
        record_list: list[Record] = []
        for line in file.readlines():
            line = line.strip()
            data_list = line.split(",")
            record = Record(data_list[0], data_list[1], data_list[2], data_list[3])
            record_list.append(record)
        file.close()
        return record_list


class jsonFileReader(FileReader):
    def __init__(self, filename: str):
        self.filename = filename

    def readData(self) -> list[Record]:
        file = open(self.filename, encoding="utf-8")
        record_list: list[Record] = []
        data_list = json.load(file)
        for data_dict in data_list:
            record = Record(
                data_dict["name"], data_dict["age"], data_dict["gender"], data_dict["occupation"]
            )
            record_list.append(record)
        file.close()
        return record_list

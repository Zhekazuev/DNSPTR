"""
Подготовка выгрузки FTTx GOV с PTR
http://jira/browse/PSSER-2588
"""
import pydig
import csv


def file(csv_file):
    """
     Read a CSV file using csv.DictReader
    """
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    return csv_reader


def main():
    with open('ptr_examples.csv', encoding="utf8") as csv_file:
        csv_reader = file(csv_file)
        for row in csv_reader:
            print(row)


if __name__ == '__main__':
    main()

"""
Подготовка выгрузки FTTx GOV с PTR
http://jira/browse/PSSER-2588
"""
from dns import exception as dnsexception
from dns import reversename
from dns import resolver
import pyexcel
import csv


def readfile(file_name, delimiter=","):
    """
     Read a CSV file using csv.DictReader
    """
    csv_reader = csv.DictReader(file_name, delimiter=delimiter)
    return csv_reader


def create_xlsx_copy(file_name, delimiter=";"):
    sheet = pyexcel.get_sheet(file_name=f"{file_name}.csv", delimiter=delimiter)
    return sheet.save_as(f"{file_name}.xlsx")


def main():
    output_file_name = "ptr_output"
    file = open(f"{output_file_name}.csv", "w",  encoding="utf8")
    file.write("NAME;MSISDN;IP;ARPA;DOMAIN;NEW_IP;ARPA_NEW;NEW_DOMAIN\n")

    with open('ptr_examples.csv', encoding="utf8") as csv_read:
        csv_reader = readfile(csv_read)
        for row in csv_reader:
            try:
                rev_addr = reversename.from_address(row["FRAMED-IP-ADDRESS"])
            except dnsexception.SyntaxError:
                rev_addr = "Null"
            try:
                new_rev_addr = reversename.from_address(row["FRAMED-IP-ADDRESS NEW"])
            except dnsexception.SyntaxError:
                new_rev_addr = "Null"

            try:
                domain = resolver.query(rev_addr, "PTR")[0]
            except resolver.NXDOMAIN:
                domain = "NXDOMAIN"
            try:
                new_domain = resolver.query(rev_addr, "PTR")[0]
            except resolver.NXDOMAIN:
                new_domain = "NXDOMAIN"
            file.write(f"{row['NAME']};{row['MSISDN']};{row['FRAMED-IP-ADDRESS']};"
                       f"{rev_addr};{domain};{row['FRAMED-IP-ADDRESS NEW']};{new_rev_addr};{new_domain}\n")
    file.close()
    create_xlsx_copy(output_file_name)


if __name__ == '__main__':
    main()

import pandas as pd


# class HumBotLog:
#
#     def __init__(self, time: str,
#                  date: str,
#                  operation: str,
#                  base: str,
#                  value_base: float,
#                  quote: str,
#                  value_quote: float):
#         self.time = time
#         self.date = date
#         self.operation = operation
#         self.value_base = value_base
#         self.value_quote = value_quote
#         self.base = base
#         self.quote = quote
#
#     def __str__(self):
#         return f"{self.date} {self.time} {self.operation} {self.base}-{self.quote} {self.value_base} {self.value_quote}"


#  TODO for now this WAY to split data in log record is OK, but in future need to write regex maybe
def parse_one_line(line: str):
    spl_line = line.split(' ')
    time = spl_line[23:25][0][7:] + ' ' + spl_line[23:25][1][:-1]
    operation = spl_line[11]
    value_base = float(spl_line[14][1:])
    base, quote = spl_line[9][1:-1].split('-')
    value_quote = float(spl_line[17])
    return [time, operation, value_base, base, quote, value_quote]
    # return HumBotLog(
    #     time=time,
    #     date=date,
    #     operation=operation,
    #     base=base,
    #     value_base=value_base,
    #     quote=quote,
    #     value_quote=value_quote
    # )


def filter_log(data: list, filter_type: str):
    if filter_type == 'pure_market_making':
        return list(filter(lambda x: 'Maker' in x and 'has been completely filled' in x, data))
    return None


def convert_log_to_csv(parsed_log: list):
    return pd.DataFrame(parsed_log, columns=['time', 'operation', 'base', 'value_base', 'quote', 'value_quote'], )


def log_parser(path_to_log_file: str):
    with open(path_to_log_file, 'r') as log_file:
        data = log_file.read()

    data = filter_log(data.split('\n'), 'pure_market_making')
    parsed_data = [parse_one_line(line) for line in data]

    print(parsed_data)
    return convert_log_to_csv(parsed_data)


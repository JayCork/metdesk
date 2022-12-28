import argparse
import csv
from datetime import datetime
from prettytable import PrettyTable
from statistics import median, stdev, mean


def main():
    try:
        args = get_args()

        parse_data(args)

    except Exception as e:
        print(e)


def parse_data(args):
    try:
        temperatures = []
        dates = []

        with open(f"{args.data_location}.csv", "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                temperature = float(row["awg_areacalc_val"])
                date = datetime.strptime(
                    row["awg_areacalc_forecast_dtg"], "%Y-%m-%d %H:%M:%S"
                )
                temperatures.append(temperature)
                dates.append(date)

        outliers = get_outliers(temperatures, args.sensitivity)
        if args.verbose:
            print(f"{len(outliers)} outlier value(s) found: {outliers}")
        for outlier in outliers:
            temperatures.remove(outlier)

        min_temp = min(temperatures)
        max_temp = max(temperatures)
        min_temp_index = temperatures.index(min_temp)
        max_temp_index = temperatures.index(max_temp)
        min_temp_date = dates[min_temp_index]
        max_temp_date = dates[max_temp_index]

        mean_temp = sum(temperatures) / len(temperatures)
        median_temp = median(temperatures)

        max_temp_selected_day = 0
        warmest_days = []
        for temperature, date in zip(temperatures, dates):
            if (
                date.strftime("%A") == args.selected_day.capitalize()
                and temperature > max_temp_selected_day
            ):
                if args.verbose:
                    print(f"A new warmest day found: {temperature} {args.unit}")
                max_temp_selected_day = temperature
                warmest_days = [date.strftime("%Y-%m-%d")]
            elif (
                date.strftime("%A") == args.selected_day.capitalize()
                and temperature == max_temp_selected_day
            ):
                warmest_days.append(date.strftime("%Y-%m-%d"))

        table = PrettyTable()
        table.field_names = ["Statistic", f"Value ({args.unit})"]
        table.add_row(
            [
                "Minimum temperature",
                f"{round(convert_temperature(min_temp, args.unit), args.dp)} on {min_temp_date.strftime('%Y-%m-%d')}",
            ]
        )
        table.add_row(
            [
                "Maximum temperature",
                f"{round(convert_temperature(max_temp, args.unit), args.dp)} on {max_temp_date.strftime('%Y-%m-%d')}",
            ]
        )
        table.add_row(
            [
                "Mean temperature",
                round(convert_temperature(mean_temp, args.unit), args.dp),
            ]
        )
        table.add_row(
            [
                "Median temperature",
                round(convert_temperature(median_temp, args.unit), args.dp),
            ]
        )
        table.add_row(
            [f"Warmest {args.selected_day.capitalize()}(s)", [*set(warmest_days)]]
        )
        print(table)
    except FileNotFoundError:
        print("ERROR: Unable to find CSV file with declared name")


def get_args():
    try:
        parser = argparse.ArgumentParser(prog="metdesk_jc", description="Testing")

        parser.add_argument(
            "--csv",
            metavar="<name>",
            dest="data_location",
            default="data",
            help="The location of the CSV file that contains the data",
        )

        parser.add_argument(
            "--sensitivity",
            "-s",
            metavar="<name>",
            type=int,
            dest="sensitivity",
            help="How much to multipy the standard deviation by to remove outliers",
            default=3,
            choices=range(1, 6),
        )

        parser.add_argument(
            "--day",
            metavar="<name>",
            dest="selected_day",
            required=False,
            default="monday",
            choices=[
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ],
            help="Changes which day the is the warmest day",
        )

        parser.add_argument(
            "--unit",
            "-u",
            metavar="<name>",
            dest="unit",
            required=False,
            default="celsius",
            choices=["celsius", "c", "fahrenheit", "f", "kelvin", "k"],
            help="Selects the outputed tempture in the selected unit",
        )

        parser.add_argument(
            "--dp", metavar="<name>", dest="dp", type=int, default=2, required=False
        )

        parser.add_argument(
            "--verbose", "-v", action="store_true", help="increase output verbosity"
        )

        args = parser.parse_args()
        return args
    except TypeError as t_error:
        raise t_error


def get_outliers(data, multiplier):
    try:
        threshold = stdev(data) * multiplier
        mean_value = mean(data)
        outliers = []
        for value in data:
            if value < mean_value - threshold or value > mean_value + threshold:
                outliers.append(value)
        return outliers
    except TypeError as t_error:
        raise t_error


def convert_temperature(value, unit):
    try:
        if unit == "celsius" or unit == "c":
            return value
        elif unit == "fahrenheit" or unit == "f":
            return (value - 32) * 5 / 9
        elif unit == "kelvin" or unit == "k":
            return value + 273.15
        else:
            raise ValueError("Invalid measurement")
    except ValueError as v_error:
        raise v_error

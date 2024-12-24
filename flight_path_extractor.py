import pandas as pd
from datetime import datetime
from pprint import pp
from dateutil import tz
from suntime import Sun, SunTimeException

class FlightPath:
    def __init__(self, path, date):
        self.path = path
        self.date = date
        self.read_excel_to_dataframe()

        # create a list of flight path data points from the dataframe
        # first column should be time, second column should be tuple of lat and long
        self.flight_path = []
        for index, row in self.excel_data.iterrows():
            time_string = row['Time (EST)']
            # Append the specific date to the time string
            datetime_string = f"{self.date} {time_string.split(' ')[1]}"
            am_pm_string = time_string.split(' ')[2]
            datetime_string = f"{datetime_string} {am_pm_string}"
            time = datetime.strptime(datetime_string, '%Y-%m-%d %I:%M:%S %p').timestamp()
            lat = row['Latitude']
            long = row['Longitude']
            self.flight_path.append((time, lat, long))

    def get_flight_path(self):
        return self.flight_path

    def read_excel_to_dataframe(self, sheet_name=0):
        """
        Reads an Excel sheet into a pandas DataFrame.
        
        :param sheet_name: Name or index of the sheet to read. Default is the first sheet.
        :return: pandas DataFrame containing the data from the Excel sheet.
        """
        self.excel_data = pd.read_excel(self.path, sheet_name=sheet_name)

if __name__ == "__main__":
    path = "flight_path.xlsx"
    date = "2023-12-19"  # Example date

    flight = FlightPath(path, date)
    # pretty print flight path
    pp(flight.get_flight_path())
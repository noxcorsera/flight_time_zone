import pandas as pd
from datetime import datetime
from pprint import pp
from dateutil import tz
from suntime import Sun, SunTimeException
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DEBUG = True

class FlightPath:
    def __init__(self, path, date):
        if DEBUG:
            print("Initialize")
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
            time = datetime.strptime(datetime_string, '%Y-%m-%d %I:%M:%S %p')
            lat = row['Latitude']
            long = row['Longitude']
            self.flight_path.append((time, lat, long))
    
    def calculate_sunset(self):
        """
        Calculates the sunset time at a given latitude and longitude.
        
        :param lat: Latitude of the location.
        :param long: Longitude of the location.
        :return: Sunset time at the given location.
        """
        if DEBUG:
            print("Calculating Sunset")
        self.sunset_time = []
        for time, lat, long in self.flight_path:
            sun = Sun(lat, long)
            try:
                sunset_time = sun.get_sunset_time()
                self.sunset_time.append((time, sunset_time))
            except SunTimeException as e:
                print("Sun does not set at this location")
            

    # plot sunset times
    def plot_sunset_times(self):
        if DEBUG:
            print("Plotting Sunset Times")
        
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        time = [x[0] for x in self.sunset_time]
        sunset = [x[1] for x in self.sunset_time]
        plt.plot(time, sunset)
        plt.xlabel('Time')
        plt.ylabel('Sunset Time')
        plt.title('Sunset Time vs Time')
        plt.show()


    def calculate_time_to_sunset(self, time, lat, long):
        """
        Calculates the time until sunset at a given latitude and longitude.
        
        :param time: Current time.
        :param lat: Latitude of the location.
        :param long: Longitude of the location.
        :return: Time until sunset at the given location.
        """
        sunset = self.calculate_sunset(lat, long)
        return sunset - time

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
    flight.calculate_sunset()
    # pretty print flight path
    # pp(flight.sunset_time)
    flight.plot_sunset_times()
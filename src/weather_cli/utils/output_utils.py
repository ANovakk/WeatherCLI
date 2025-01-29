from prettytable import PrettyTable
from .get_emoji_util import get_emoji

param_names = {
    "relative_humidity_2m": "Humidity",
    "wind_speed_10m": "Wind",
    "precipitation_probability": "Precipitation",
    "pressure_msl": "Pressure",
    "cloud_cover": "Cloud_cover",
    "wind_gusts_10m": "Wind_gusts"
}

param_units = {
    "relative_humidity_2m": "%",
    "wind_speed_10m": "m/s",
    "precipitation_probability": "%",
    "pressure_msl": "hPa",
    "cloud_cover": "%",
    "wind_gusts_10m": "m/s"
}

def output_result(data, hourly_params):
    print(data)

    for i in range(len(data['hourly']['time'])):
        weather_time = data['hourly']['time'][i]
        weather_temp = data['hourly']['temperature_2m'][i]
        print(i + 1, weather_time, weather_temp)

        table = PrettyTable()
        table.field_names = [f"Weather for {weather_time}", "Values"]

        table.add_row(["Temperature", f"{weather_temp} °C {get_emoji('temperature_2m', weather_temp)}"])

        for param in hourly_params:
            if param:
                param_name = param_names.get(param, param)
                value = data['hourly'].get(param, [None])[i]
                emoji = get_emoji(param, value)
                unit = param_units.get(param, param)
                table.add_row([param_name, f"{value} {unit} {emoji}" if value is not None else "N/A"])

        print(table)

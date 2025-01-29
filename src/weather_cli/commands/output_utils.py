from prettytable import PrettyTable

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

def get_emoji(param, value):
    if param == "temperature_2m":
        if value > 30:
            return "🔥"
        elif value > 20:
            return "😊"
        elif value > 0:
            return "❄️"
        else:
            return "☃️"
    elif param == "precipitation_probability":
        if value > 80:
            return "🌧️"
        elif value > 50:
            return "🌦️"
        elif value > 20:
            return "🌤️"
        else:
            return "☀️"
    elif param == "wind_speed_10m":
        if value > 15:
            return "🌬️"
        elif value > 5:
            return "💨"
        else:
            return "🍃"
    elif param == "pressure_msl":
        if value > 1020:
            return "⬆️"
        elif value < 1010:
            return "⬇️"
        else:
            return "⚖️"
    elif param == "cloud_cover":
        if value > 80:
            return "☁️"
        elif value > 50:
            return "🌥️"
        else:
            return "🌤️"
    elif param == "wind_gusts_10m":
        if value > 30:
            return "🌪️"
        elif value > 15:
            return "🌬️"
        else:
            return "💨"
    else:
        return "✅"

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

data = {
    'hourly': {
        'time': ['2025-01-21 12:00', '2025-01-21 13:00'],
        'temperature_2m': [22, 24],
        'precipitation_probability': [10, 20],
        'wind_speed_10m': [5, 12],
        'pressure_msl': [1018, 1023],
        'cloud_cover': [50, 30],
        'wind_gusts_10m': [10, 15]
    }
}

hourly_params = ["temperature_2m", "precipitation_probability", "wind_speed_10m", "pressure_msl", "cloud_cover", "wind_gusts_10m"]
output_result(data, hourly_params)

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
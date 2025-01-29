from wsgiref import headers

import click
import requests

API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search"
API_URL_OPEN_METEO="https://api.open-meteo.com/v1/forecast"


def find_coordinates(city, district):
    """
    Returns dictionary with coordinates or error info.
    Structure: {
        'success': bool,
        'lat': float|None,
        'lon': float|None,
        'display_name': str|None,
        'error': str|None
    }
    """
    result = {
        'success': False,
        'lat': None,
        'lon': None,
        'display_name': None,
        'error': None
    }

    try:
        headers = {'User-Agent': 'GeoCLI/1.0 (contact@example.com)'}
        search_query = f"{district}, {city}" if district else city

        params = {
            'q': search_query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }

        response = requests.get(API_URL_NOMINATIM, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        if not data:
            result['error'] = f"Location not found: {search_query}"
            return result

        location = data[0]
        result.update({
            'success': True,
            'lat': float(location['lat']),
            'lon': float(location['lon']),
            'display_name': location.get('display_name', 'N/A')
        })

    except requests.exceptions.HTTPError as e:
        result['error'] = f"HTTP error: {str(e)}"
    except requests.exceptions.RequestException as e:
        result['error'] = f"Connection error: {str(e)}"
    except (KeyError, IndexError) as e:
        result['error'] = "Data processing error"
    except Exception as e:
        result['error'] = f"Unexpected error: {str(e)}"

    return result


@click.command(name="now")
@click.option("--city", prompt="Enter city name", help="City name to search")
@click.option("--district", default=None, help="District/area name (optional)")
@click.option( '--days', '-d', '--number', '-n', default=[1], show_default=True,
              help="Number of days to show [1-7]")
@click.option('--wind', '-w', is_flag=True, help="Include wind speed (optional)")
@click.option('--precipitation', '-p', is_flag=True, help="Include precipitation (optional)")
@click.option('--humidity', '-h', is_flag=True, help="Include humidity (optional)")
@click.option('--pressure', is_flag=True, help="Include pressure (optional)")
@click.option('--cloud', '-c', is_flag=True, help="Include cloud cover (optional)")
@click.option('--gust', '-g', is_flag=True, help="Include maximum wind speed and gusts (optional)")
def now(city, district, days, wind,
        precipitation, humidity, pressure, cloud, gust, uv):
    """Get coordinates by city name and/or district"""
    data = find_coordinates(city, district)

    if not data['success']:
        click.echo(f"Error: {data['error']}")
        return

    output = [
        f"Search results for: {city}" + (f" ({district})" if district else ""),
        f"- Coordinates: {data['lat']}, {data['lon']}",
        f"- Full name: {data['display_name']}"
    ]
    click.echo("\n".join(output))

    try:
        get_wind_value = "wind_speed_10m" if wind else None
        get_precipitation = "precipitation_probability" if precipitation else None
        get_humidity = "relative_humidity_2m" if humidity else None
        get_pressure = "pressure_msl" if pressure else None
        get_cloud_cover = "cloud_cover" if cloud else None
        get_wind_gusts = "wind_gusts_10m" if gust else None
        params = {
            "latitude": data['lat'],
            "longitude": data['lon'],
            "hourly": ["temperature_2m",
                       get_wind_value,
                       get_precipitation,
                       get_humidity,
                       get_pressure,
                       get_cloud_cover,
                       get_wind_gusts],
            "forecast_days": max(1, min(7, days)),
        }
        response = requests.get(API_URL_OPEN_METEO, params=params)
        response.raise_for_status()

        weather_data = response.json()
        print(weather_data)

        for i in range(len(weather_data['hourly']['time'])):
            weather_time = weather_data['hourly']['time'][i]
            weather_temp = weather_data['hourly']['temperature_2m'][i]
            print(i + 1, weather_time, weather_temp)

    except requests.exceptions.HTTPError as e:
        click.echo(f"HTTP error: {str(e)}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Connection error: {str(e)}")
    except (KeyError, IndexError) as e:
        click.echo("Data processing error")
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    now()
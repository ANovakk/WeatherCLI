import click
import requests

API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search"


@click.command(name="now")
@click.option("--city", prompt="Enter city name", help="City name to display weather for")
def now(city):
    """
    Get current weather forecast with city coordinates
    """
    try:
        headers = {
            'User-Agent': 'WeatherCLI/1.0 (contact@example.com)'
        }

        params = {
            'q': city,
            'format': 'json',
            'limit': 1
        }

        response = requests.get(API_URL_NOMINATIM, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        if not data:
            click.echo(f"City '{city}' not found")
            return

        location = data[0]
        lat = location['lat']
        lon = location['lon']
        click.echo(f"Coordinates for {city}: Latitude {lat}, Longitude {lon}")

    except requests.exceptions.HTTPError as e:
        click.echo(f"HTTP error: {str(e)}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Connection error: {str(e)}")
    except (KeyError, IndexError) as e:
        click.echo("Response data processing error")


if __name__ == "__main__":
    now()
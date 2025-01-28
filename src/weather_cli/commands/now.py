import click
import requests

API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search"

@click.command(name="now")
@click.option("--city", prompt="Enter city name", help="City name to search")
@click.option("--district", default=None, help="District/area name (optional)")
def now(city, district):
    """
    Get coordinates by city name and/or district
    """
    try:
        headers = {
            'User-Agent': 'GeoCLI/1.0 (contact@example.com)'
        }

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
            click.echo(f"Location not found: {search_query}")
            return

        location = data[0]
        lat = location['lat']
        lon = location['lon']
        display_name = location.get('display_name', 'N/A')

        output = [
            f"Search results for: {search_query}",
            f"- Coordinates: {lat}, {lon}",
            f"- Full name: {display_name}"
        ]

        click.echo("\n".join(output))

    except requests.exceptions.HTTPError as e:
        click.echo(f"HTTP error: {str(e)}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Connection error: {str(e)}")
    except (KeyError, IndexError) as e:
        click.echo("Data processing error")

if __name__ == "__main__":
    now()
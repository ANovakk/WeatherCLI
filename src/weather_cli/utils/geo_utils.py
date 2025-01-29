import requests

API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search"

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

---
name: weather
description: Retrieve current weather, today's summary, and forecasts using Open-Meteo. Automatically resolves locations via Nominatim or IP geolocation.
---

# Weather Skill

This skill allows you to retrieve accurate weather data for any location or the host machine's current IP address. It interacts with the Open-Meteo API for weather data, Nominatim for geocoding specific locations, and IPify/IP-API for IP-based geolocation.

## Usage

When you need to retrieve weather data, use the exec tool to run the Python script:

```bash
python3 [skill path (parent directory of SKILL.md)]/scripts/weather.py <COMMAND> <PARAMETERS>
```

> **Note on Geolocation:** If the `--location` parameter is omitted, the script automatically attempts to geolocate the host machine's IP address.

### Commands and Parameters

#### 1. Show Today's Weather (today)

Retrieves the daily weather summary for the current day.

* Syntax: today <optional parameters>
* Optional Parameters:
* `--location "<string>"`: Target location (e.g., "Seoul", "Paris, France").
* `--customparam "<string>"`: Comma-separated Open-Meteo daily parameters. Defaults to: *weather_code, temperature_2m_max, temperature_2m_min, precipitation_probability_max, precipitation_sum, wind_speed_10m_max*.
* `--imperial`: Flag. Changes units to Fahrenheit, mph, and inches (default is metric).

#### 2. Show Current Weather (now)

Retrieves the immediate current weather conditions.

* Syntax: now <optional parameters>
* Optional Parameters:
* `--location "<string>"`: Target location.
* `--customparam "<string>"`: Comma-separated Open-Meteo current parameters. Defaults to: *temperature_2m, relative_humidity_2m, precipitation, weather_code, wind_speed_10m*.
* `--imperial`: Flag. Uses Imperial units.

#### 3. Show Forecast (forecast)

Retrieves future weather predictions at various time intervals.

* Syntax: forecast <optional parameters>
* Optional Parameters:
* `--location "<string>"`: Target location.
* `--type <type>`: The interval of the forecast. Options: `minutely15`, `hourly`, `daily`. (Default: `hourly`).
* `--count <number>`: Number of forecast units to retrieve. (Default: 4).
* `--customparam "<string>"`: Comma-separated Open-Meteo parameters specific to the forecast type.
* `--imperial`: Flag. Uses Imperial units.

**Forecast Type Default Parameters**

| Type | Default Custom Parameters |
| --- | --- |
| **minutely15** | `temperature_2m, precipitation, wind_speed_10m, relative_humidity_2m, wind_direction_10m` |
| **hourly** | `temperature_2m, relative_humidity_2m, precipitation_probability, precipitation, weather_code, wind_speed_10m` |
| **daily** | `weather_code, temperature_2m_max, temperature_2m_min, precipitation_probability_max, precipitation_sum, wind_speed_10m_max` |

*For custom parameters, refer to: https://open-meteo.com/en/docs*

---

## Example Usage

**Getting current weather based on IP address (Metric):**

```bash
python3 [skill path]/scripts/weather.py now
```

**Getting today's weather in Tokyo (Imperial):**

```bash
python3 [skill path]/scripts/weather.py today --location "Tokyo, Japan" --imperial
```

**Getting an hourly forecast for the next 12 hours in London:**

```bash
python3 [skill path]/scripts/weather.py forecast --location "London, UK" --type hourly --count 12
```

**Getting current weather with specific custom parameters:**

```bash
python3 [skill path]/scripts/weather.py now --location "Seoul, Korea" --customparam "temperature_2m,cloud_cover"
```

## Output Format

* **Success:** The script outputs raw, formatted JSON directly from the Open-Meteo API. The `weather_code` integer values are automatically translated into human-readable strings (e.g., `61` becomes `"Rain: Slight intensity"`) for easier interpretation.
* **Error:** If an API fails, rate limits are hit, or a location cannot be found, the script exits safely and outputs a standard JSON error object: `{"error": "Description of the error"}`.

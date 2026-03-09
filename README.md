# Alternative Weather Skill for Nanobot

A custom skill for your nanobot workspace that retrieves current weather, today's summary, and forecasts. It leverages the Open-Meteo API for accurate weather data, Nominatim for specific location geocoding, and IPify/IP-API for automatic host IP geolocation. 

### Automatic Skill Override

Because this skill is named `weather`, the nanobot will automatically prioritize and load it in place of the built-in `weather` skill. If you want to revert to built-in skill, you can simply remove `weather` directory under `skills`

## Installation

Follow these steps to install the skill automatically into your nanobot workspace.

1. **Navigate to your workspace:** Open your terminal and ensure your current directory is the root of your nanobot workspace (the folder containing your `skills` directory).

```bash
cd /path/to/your/nanobot/workspace
```

2. **Download the installer:** Use `wget` to fetch the installation script directly from the repository.

```bash
wget "https://raw.githubusercontent.com/SJK-py/nanobot-weather/main/install_weather.sh"
```

3. **Execute the script:** Make the script executable and run it to set up the directories and download the necessary files.

```bash
chmod +x install_weather.sh
./install_weather.sh
```

Once installed, your nanobot will automatically detect and load this `weather` skill.

## How the Nanobot Uses It

When weather data is required, the nanobot uses the `exec` tool to run the helper Python script.

The nanobot will construct commands using the following syntax:

```bash
python3 [skill path]/scripts/weather.py <COMMAND> <PARAMETERS>
```

> **Note on Geolocation:** If the `--location` parameter is omitted by the nanobot, the script automatically attempts to geolocate the host machine's IP address to provide local weather.

### Available Commands

* **`today`**: Retrieves the daily weather summary for the current day.
* **`now`**: Retrieves the immediate current weather conditions.
* **`forecast`**: Retrieves future weather predictions at various time intervals.

### Optional Parameters

* `--location "<string>"`: Target location (e.g., "Seoul", "Paris, France").
* `--imperial`: Flag that changes units to Fahrenheit, mph, and inches (default is metric).
* `--customparam "<string>"`: Comma-separated Open-Meteo parameters to fetch specific data points.
* `--type <type>`: **(Forecast only)** The interval of the forecast (`minutely15`, `hourly`, `daily`). Defaults to `hourly`.
* `--count <number>`: **(Forecast only)** Number of forecast units to retrieve. Defaults to `4`.

### Skill Output

* **Success:** The script outputs raw, formatted JSON directly from the Open-Meteo API. For easier interpretation by the LLM, standard `weather_code` integer values are automatically translated into human-readable strings (e.g., `61` becomes `"Rain: Slight intensity"`).
* **Error:** If an API fails or a location cannot be found, the script safely exits and outputs a standard JSON error object (e.g., `{"error": "Description of the error"}`) so the nanobot doesn't crash trying to parse stdout.

## Manual Usage (Optional)

Though designed for autonomous nanobot use, the helper script can be executed independently from the command line:

**Get current weather based on your IP (Metric):**

```bash
python3 [skill path]/scripts/weather.py now
```

**Get an hourly forecast for the next 12 hours in London:**

```bash
python3 [skill path]/scripts/weather.py forecast --location "London, UK" --type hourly --count 12
```

**Get today's weather in Tokyo (Imperial unit of measure):**

```bash
python3 [skill path]/scripts/weather.py today --location "Tokyo, Japan" --imperial
```

## License

MIT

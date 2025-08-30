# Ennatuurlijk-WarmteCheck
This project is an Azure Function App for calculating the heating index (an index for how much energy is needed for heating when the temperature reaches below 20 degrees celcius) for various locations in the Netherlands using weather data from the OpenMeteo API. It retrieves temperature forecasts for configured locations, calculates how much heating is needed per hour, and stores the results. The app includes:

- **HTTP Trigger**: Accepts POST requests with a list of locations and returns the heating index forecast for each.
- **Timer Trigger**: Runs on a schedule at 7:00 UTC daily, processes configured locations, and stores the results automatically.
- **Local Storage**: By default, results are saved to local files for easy development and testing.
- **Configurable Locations**: Locations can be set via environment variables or HTTP requests.

## Prerequisites

- **Python 3.8+** (recommended: 3.10 or newer)
- **Node.js** (for Azure Functions Core Tools)
- **Azure Functions Core Tools** ([Install guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2))
- **Azurite** (local Azure Storage emulator)
- **Docker** (optional, for running Azurite)
- **VS Code** (recommended, with Python and Azure Functions extensions)

## Setup Instructions

1. **Clone the repository**
	```sh
	git clone https://github.com/BluRRayS/Ennatuurlijk-WarmteCheck.git
	cd Ennatuurlijk-WarmteCheck/app
	```

2. **Create and activate a Python virtual environment**
	```sh
	python -m venv .venv
	# Windows:
	.venv\Scripts\activate
	# macOS/Linux:
	source .venv/bin/activate
	```

3. **Install Python dependencies**
	```sh
	pip install -r requirements.txt
	```

4. **Install Azure Functions Core Tools**
	```sh
	npm install -g azure-functions-core-tools@4 --unsafe-perm true
	```

5. **Start Azurite (local storage emulator)**
	- **With Docker:**
	  ```sh
	  docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite
	  ```
	- **With npm:**
	  ```sh
	  npm install -g azurite
	  azurite
	  ```
	- Or use the VS Code Azurite extension.

6. **Run the Azure Function app locally**
	```sh
	func start
	```

7. **Test the HTTP trigger**
	- Send a POST request to:
	  ```
	  http://localhost:7071/api/http_trigger
	  ```
	- Example body:
	  ```json
	  [
		 {"name": "Eindhoven", "lat": 51.44, "lon": 5.47},
		 {"name": "Amsterdam", "lat": 52.37, "lon": 4.89}
	  ]
	  ```

## Debugging in VS Code

1. Set breakpoints in your Python code.
2. Start the function app with `func start`.
3. Use the provided `.vscode/launch.json` and select "Attach to Azure Functions Python" to debug.
4. If you want to debug startup, add `debugpy` to `requirements.txt` and insert:
	```python
	import debugpy
	debugpy.listen(("localhost", 5678))
	print("Waiting for debugger attach...")
	debugpy.wait_for_client()
	```
	at the top of your function entry file.

## Notes

- The timer trigger requires Azurite to be running for local development.
- All configuration is in `local.settings.json`.
- Shared logic is in the `src` folder.

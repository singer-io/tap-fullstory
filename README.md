# tap-close-io

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls raw data from Close.io's [REST API](https://developer.close.io/)
- Extracts the following resources from Close.io:
  - [Activities](https://developer.close.io/#activities)
  - [Leads](https://developer.close.io/#leads)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Quick start

1. Install

    ```bash
    > pip install tap-closeio
    ```

2. Get your Close.io API Key

    Login to your Close.io account, navigate to your account settings and "Your API Keys". Generate a New API Key, you'll need it for the next step.

3. Create the config file

    Create a JSON file called `config.json` containing the api key you just generated.

    ```json
    {"api_key": "your-api-token"}
    ```

4. [Optional] Create the initial state file

    You can provide JSON file that contains a date for the API endpoints
    to force the application to only fetch data newer than those dates.
    If you omit the file it will fetch all Close.io data

    ```json
    {"activities": "2017-01-17T20:32:05Z",
     "leads": "2017-01-17T20:32:05Z"}
    ```

5. Run the application

    `tap-closeio` can be run with:

    ```bash
    tap-closeio --config config.json [--state state.json]
    ```

---

Copyright &copy; 2017 Stitch

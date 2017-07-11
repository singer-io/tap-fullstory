# tap-fullstory

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls data export packs from FullStory's [Data Export REST API](http://help.fullstory.com/develop-rest/data-export-api). Note: The Data Export is a paid add-on to FullStory's normal service. Contact their support team for pricing details.
- Extracts [Events](http://help.fullstory.com/technical-questions/data-export) from the data export packs.
- Outputs the schema.
- Incrementally pulls data based on the input state.


## Quick start

1. Install

    ```bash
    > pip install tap-fullstory
    ```

2. Get your FullStory API Key

    Login to your FullStory account, navigate to your account settings and "Integrations & API Keys". Copy your API key, you'll need it for the next step.

3. Create the config file

    Create a JSON file called `config.json` containing the api key you
    just generated, and the timestamp of the date that you want the
    tap to start replicating from.

    ```json
    {
      "api_key": "your-api-token",
      "start_date": "2017-01-01T00:00:00Z"
    }
    ```

4. Run the application

    `tap-fullstory` can be run with:

    ```bash
    tap-fullstory --config config.json [--state state.json]
    ```

---

Copyright &copy; 2017 Stitch

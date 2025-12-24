# tap-fullstory

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

This tap:

- Pulls raw data from the [fullstory API].
- Extracts the following resources:
    - [Users](https://developer.fullstory.com/server/users/list-users/)

    - [User](https://developer.fullstory.com/server/users/get-user/)

    - [BlockRules](https://developer.fullstory.com/server/v1/settings/get-recording-block-rules/)

    - [BlockRulesHistory](https://developer.fullstory.com/server/v1/settings/get-recording-block-rules-history/)

    - [DomainSettingsHistory](https://developer.fullstory.com/server/v1/settings/get-domain-settings-history/)

    - [DomainSettings](https://developer.fullstory.com/server/v1/settings/get-domain-settings/)

    - [GeoSettingsHistory](https://developer.fullstory.com/server/v1/settings/get-geo-settings-history/)

    - [PrivacySettings](https://developer.fullstory.com/server/v1/settings/get-privacy-settings/)

    - [PrivacySettingsHistory](https://developer.fullstory.com/server/v1/settings/get-privacy-settings/)

    - [RecordingFeatures](https://developer.fullstory.com/server/v1/settings/get-recording-features/)

    - [RecordingFeaturesHistory](https://developer.fullstory.com/server/v1/settings/get-recording-features-history/)

    - [TargetRuleHistory](https://developer.fullstory.com/server/v1/settings/get-targeting-settings-history/)

    - [Segments](https://developer.fullstory.com/server/v1/segments/list-segments/)

- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Streams


**[users](https://developer.fullstory.com/server/users/list-users/)**
- Data Key = results
- Primary keys: id
- Replication strategy: FULL_TABLE

**[user](https://developer.fullstory.com/server/users/get-user/)**
- Primary keys: id
- Replication strategy: FULL_TABLE

**[block_rules](https://developer.fullstory.com/server/v1/settings/get-recording-block-rules/)**
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[block_rules_history](https://developer.fullstory.com/server/v1/settings/get-recording-block-rules-history/)**
- Data Key = versions
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[domain_settings_history](https://developer.fullstory.com/server/v1/settings/get-domain-settings-history/)**
- Data Key = versions
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[domain_settings](https://developer.fullstory.com/server/v1/settings/get-domain-settings/)**
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[geo_settings_history](https://developer.fullstory.com/server/v1/settings/get-geo-settings-history/)**
- Data Key = versions
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[privacy_settings](https://developer.fullstory.com/server/v1/settings/get-privacy-settings/)**
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[privacy_settings_history](https://developer.fullstory.com/server/v1/settings/get-privacy-settings/)**
- Data Key = versions
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[recording_features](https://developer.fullstory.com/server/v1/settings/get-recording-features/)**
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[recording_features_history](https://developer.fullstory.com/server/v1/settings/get-recording-features-history/)**
- Data Key = versions
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[target_rule_history](https://developer.fullstory.com/server/v1/settings/get-targeting-settings-history/)**
- Data Key = versions
- Primary keys: ['created', 'createdBy', 'lastUpdated']
- Replication strategy: INCREMENTAL

**[segments](https://developer.fullstory.com/server/v1/segments/list-segments/)**
- Data Key = segments
- Primary keys: ['id']
- Replication strategy: FULL_TABLE



## Authentication

## Quick Start

1. Install

    Clone this repository, and then install using setup.py. We recommend using a virtualenv:

    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    > python setup.py install
    OR
    > cd .../tap-fullstory
    > pip install -e .
    ```
2. Dependent libraries. The following dependent libraries were installed.
    ```bash
    > pip install singer-python
    > pip install target-stitch
    > pip install target-json

    ```
    - [singer-tools](https://github.com/singer-io/singer-tools)
    - [target-stitch](https://github.com/singer-io/target-stitch)

3. Create your tap's `config.json` file.  The tap config file for this tap should include these entries:
   - `start_date` - the default value to use if no bookmark exists for an endpoint (rfc3339 date string)
   - `user_agent` (string, optional): Process and email for API logging purposes. Example: `tap-fullstory <api_user_email@your_company.com>`
   - `request_timeout` (integer, `300`): Max time for which request should wait to get a response. Default request_timeout is 300 seconds.

    ```json
    {
        "start_date": "2019-01-01T00:00:00Z",
        "user_agent": "tap-fullstory <api_user_email@your_company.com>",
        "request_timeout": 300
    }

    ```
    Optionally, also create a `state.json` file. `currently_syncing` is an optional attribute used for identifying the last object to be synced in case the job is interrupted mid-stream. The next run would begin where the last job left off.

    ```json
    {
        "currently_syncing": "dummy_stream1",
        "bookmarks": {
            "dummy_stream1": "2019-09-27T22:34:39.000000Z",
            "dummy_stream2": "2019-09-28T15:30:26.000000Z",
            "dummy_stream3": "2019-09-28T18:23:53Z"
        }
    }
    ```

4. Run the Tap in Discovery Mode
    This creates a catalog.json for selecting objects/fields to integrate:
    ```bash
    tap-fullstory --config config.json --discover > catalog.json
    ```
   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).

5. Run the Tap in Sync Mode (with catalog) and [write out to state file](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target)

    For Sync mode:
    ```bash
    > tap-fullstory --config tap_config.json --catalog catalog.json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To load to json files to verify outputs:
    ```bash
    > tap-fullstory --config tap_config.json --catalog catalog.json | target-json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To pseudo-load to [Stitch Import API](https://github.com/singer-io/target-stitch) with dry run:
    ```bash
    > tap-fullstory --config tap_config.json --catalog catalog.json | target-stitch --config target_config.json --dry-run > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

6. Test the Tap
    While developing the fullstory tap, the following utilities were run in accordance with Singer.io best practices:
    Pylint to improve [code quality](https://github.com/singer-io/getting-started/blob/master/docs/BEST_PRACTICES.md#code-quality):
    ```bash
    > pylint tap_fullstory -d missing-docstring -d logging-format-interpolation -d too-many-locals -d too-many-arguments
    ```
    Pylint test resulted in the following score:
    ```bash
    Your code has been rated at 9.67/10
    ```

    To [check the tap](https://github.com/singer-io/singer-tools#singer-check-tap) and verify working:
    ```bash
    > tap_fullstory --config tap_config.json --catalog catalog.json | singer-check-tap > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

    #### Unit Tests

    Unit tests may be run with the following.

    ```
    python -m pytest --verbose
    ```

    Note, you may need to install test dependencies.

    ```
    pip install -e .'[dev]'
    ```
---

Copyright &copy; 2019 Stitch

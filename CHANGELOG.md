# Changelog

## 1.0.5
  * Bump dependency versions for twistlock compliance
  * Update circleci config to fix failing build
  * [#13](https://github.com/singer-io/tap-fullstory/pull/13)

## 1.0.4
  * Update version of `singer-python` to `1.9.1` to allow JSON serialisation of `Decimal` types

## 1.0.3
  * Update version of `requests` to `2.20.0` in response to CVE 2018-18074

## 1.0.2
  * Updated JSON parsing to iterate over the response [#4](https://github.com/singer-io/tap-fullstory/pull/4)

## 1.0.1
  * Update endpoint to latest supported URL (export.fullstory.api), no functionality change [#3](https://github.com/singer-io/tap-fullstory/pull/3)
  * Migrated CircleCI config to 2.0

## 1.0.0
  * Major version bump for full release (no changes)

## 0.1.2
  * Use 'utf-8' encoding for `unzip_to_json` [#1](https://github.com/singer-io/tap-fullstory/pull/1)

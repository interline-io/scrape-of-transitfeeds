# Scrape of TransitFeeds.com API

Metadata about GTFS and GTFS Realtime feeds scraped from the [TransitFeeds/OpenMobilityData API](https://openmobilitydata.org/).

## Collected data

- [all feed metadata in a single JSON file](json-scrape/getFeeds.json)
- [all feed version metadata in a single JSON file](json-scrape/getFeedVersions.json)
- [list of URLs to download archived feed versions from S3](json-scrape/feedVersionS3Urls.csv)
## Instructions for running the scraping scripts

1. Get an API key from https://transitfeeds.com/api/ and provide it in an environment variable called `TRANSITFEEDS_API_KEY`
2. `pipenv install`
3. Download all pages of `getFeeds` and `getFeedVersions` endpoints: `python scrape-transitfeeds.py get`
4. Merge together JSON files for each page: `python scrape-transitfeeds.py merge`
5. Get direct S3 download URLs for feed versions `python scrape-transitfeeds.py s3urls`

## License

> All of OpenMobilityData's metadata, including the API and site contents, are made available under Creative Commons CC0 (CC0).

according to https://transitfeeds.com/about accessed on 27 August 2021.

## See also

- [Transitland](https://www.transit.land) platform to browse most of these feeds and query their contents using APIs
- [Mobility Database](http://mobilitydatabase.org) under development by MobilityData
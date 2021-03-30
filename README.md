0. `pipenv install`
1. Download all pages of `getFeeds` and `getFeedVersions` endpoints: `python scrape-transitfeeds.py get`
2. Merge together JSON files for each page: `python scrape-transitfeeds.py merge`
3. Get direct S3 download URLs for feed versions `python scrape-transitfeeds.py s3urls`

import requests
import hashlib
import pathlib
import json
import os
import sys
import glob
from urllib.parse import urlparse


def loopThroughRequests(endpoint):
    apikey = os.environ['TRANSITFEEDS_API_KEY']
    base_url = f"https://api.transitfeeds.com/v1/{endpoint}?key={apikey}&limit=100"
    first_page = requests.get(base_url).json()
    total_page_num = first_page["results"]["numPages"]
    current_page_num = first_page["results"]["page"]

    while current_page_num <= total_page_num:
        page = requests.get(f"{base_url}&page={current_page_num}").json()
        with open(f"json-scrape/{endpoint}-p{current_page_num}.json", "w") as f:
            pretty_json = json.dumps(page, indent=2, sort_keys=True, ensure_ascii=False)
            f.write(pretty_json)
        current_page_num += 1


def mergeJsonFiles(endpoint, array_key):
    collected_values = []
    files = glob.glob(f"json-scrape/{endpoint}-p*.json")
    for file_path in files:
        with open(file_path, "r") as f:
            page = json.loads(f.read())
            collected_values.extend(page["results"][array_key])
    with open(f"json-scrape/{endpoint}.json", "w") as f:
        pretty_json = json.dumps(
            collected_values, indent=2, sort_keys=True, ensure_ascii=False
        )
        f.write(pretty_json)


def getS3Urls():
    with open("json-scrape/getFeedVersions.json", "r") as fr:
        feed_versions = json.loads(fr.read())
        with open("json-scrape/feedVersionS3Urls.csv", "w") as fw:
            for fv in feed_versions:
                tf_url = fv["url"]
                r = requests.get(tf_url, allow_redirects=False)
                if "Location" in r.headers:
                    fw.write(r.headers["Location"])
                    fw.write("\n")

def downloadAllFeedVersions():
    with open("json-scrape/feedVersionS3Urls.csv", "r") as f:
        for raw_url in f:
            parsed_url = urlparse(raw_url)
            # provider and feed subdirectories
            provider_feed_subpath = os.path.join('feed-versions', *parsed_url.path.split('/')[3:-2])
            pathlib.Path(provider_feed_subpath).mkdir(parents=True, exist_ok=True)
            # fv file
            fv_id = parsed_url.path.split('/')[5]
            write_file_name = os.path.join(provider_feed_subpath, f"{fv_id}.zip")
            # prepare to hash
            sha1 = hashlib.sha1()
            # streaming download
            r = requests.get(raw_url, allow_redirects=True, stream = True)
            with open(write_file_name,"wb") as fv_file:
                for chunk in r.iter_content(chunk_size=1024):
                    # writing one chunk at a time to pdf file
                    if chunk:
                        sha1.update(chunk)
                        fv_file.write(chunk)
                print(f"Downloaded {write_file_name}")
            write_file_name_with_hash = write_file_name.replace(".zip", f"-{sha1.hexdigest()}.zip")
            os.rename(write_file_name, write_file_name_with_hash)
            print(f"Moved to {write_file_name_with_hash}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "get":
        loopThroughRequests("getFeeds")
        loopThroughRequests("getFeedVersions")
    elif args[0] == "merge":
        mergeJsonFiles("getFeeds", "feeds")
        mergeJsonFiles("getFeedVersions", "versions")
    elif args[0] == "s3urls":
        getS3Urls()
    elif args[0] == 'download':
        downloadAllFeedVersions()
    else:
        print("subcommands:")
        print("\n\t get")
        print("\n\t merge")
        print("\n\t s3urls")

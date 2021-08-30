import requests
import json
import os
import sys
import glob


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
    else:
        print("subcommands:")
        print("\n\t get")
        print("\n\t merge")
        print("\n\t s3urls")

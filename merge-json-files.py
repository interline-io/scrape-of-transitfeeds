import json
import glob

def main(endpoint, array_key):
  collected_values = []
  files = glob.glob(f"json-scrape/{endpoint}-p*.json")
  for file_path in files:
    with open(file_path, 'r') as f:
      page = json.loads(f.read())
      collected_values.extend(page["results"][array_key])
  with open(f"json-scrape/{endpoint}.json", 'w') as f:
    pretty_json = json.dumps(collected_values, indent=2, sort_keys=True, ensure_ascii=False)
    f.write(pretty_json)


if __name__ == "__main__":
    main("getFeeds", "feeds")
    main("getFeedVersions", "versions")

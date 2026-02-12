import json
import os
import requests
import serpapi


if __name__ == "__main__":
    YOUR_API_KEY = os.environ.get("SERPAPI_API_KEY")
    # resp = requests.get(f"https://serpapi.com/search.json?q=Coffee&api_key={YOUR_API_KEY}")
    # resp = requests.get(f"https://serpapi.com/search.json?engine=google_ai_mode&q=Coffee&api_key={YOUR_API_KEY}")
    params = {
    "engine": "google_ai_mode",
    "q": "mega basket ABA league team statistics",
    "api_key": YOUR_API_KEY
    }
    resp = requests.get(f"https://serpapi.com/search.json", params=params)
    resp_jn = resp.json()
    with open("serpapi_response.json", "w", encoding="utf-8") as f:
        json.dump(resp_jn, f, indent=2, ensure_ascii=False)
    # from serpapi import GoogleSearch
    


    # search = GoogleSearch(params)
    # results = search.get_dict()

    # text_blocks = results["text_blocks"]
    # https://serpapi.com/search.json?engine=google_ai_mode&q=Coffee


    # s = serpapi.search(q="Coffee", engine="google", location="Austin, Texas", hl="en", gl="us")
    print("bye")

 
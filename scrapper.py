import requests

url = (
    "https://dls.staatsarchiv.bs.ch/api/search/?page=1&page_size=350&media_type_in=pdf"
)


def scrap():
    data = requests.get(url).json()

    results = data["results"]
    output = []
    for item in results:
        output.append(
            {
                "pk": item["pk"],
                "files": list(
                    filter(lambda file: file["media_type"] == "pdf", item["files"])
                ),
            }
        )
    return output

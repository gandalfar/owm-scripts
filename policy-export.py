import requests
from collections import OrderedDict
import json
from scalpl import Cut
import arrow
import pandas as pd

from utils import en_with_fallback

FIELDS = [
    "/@id"
    "/@type"
    "/name/en"
    "/description/en"
    "/provider/\\d+/name/en"
    "/url"
    "/additionalType/\\d+/name/en"
    "/primarySector/\\d+/name/en"
    "/startDate"
    "/endDate"
    "/startTime"
    "/endTime"
    "/agent/\\d+/name/en"
    "/location/\\d+/address/."
]


def main():
    r = requests.get(
        "https://oerworldmap.org/resource/?size=&ext=json&filter.about.@type=Policy",
        headers={"X-CSV-HEADERS": ",".join(FIELDS)},
    )
    with open("policy.json", "wb") as f:
        f.write(r.content)

    raw_data = json.load(open("policy.json", "rb"))

    rows = []
    for item in raw_data.get("member"):
        data = OrderedDict()
        proxy = Cut(item)

        data["ID"] = proxy.get("feature.id")
        data["STATUS ON MAP"] = ""
        data["Title"] = proxy.get("feature.properties.name.en")
        data["Map URL"] = "https://oerworldmap.org/resource/{}".format(
            proxy.get("feature.id")
        )
        data["URL"] = proxy.get("about.url")
        data["Policy Type"] = proxy.get("feature.properties.additionalType[0].name.en")
        data["Description"] = proxy.get("about.description.en")
        data["Level"] = proxy.get("about.spatialCoverage")
        data["Scope"] = proxy.get("about.scope[0].name.en")

        for idx, focus in enumerate(proxy.get("about.focus", []), start=1):
            data["Focus ({})".format(idx)] = focus

        data["Primary educational sector"] = proxy.get("about.primarySector[0].name.en")

        for idx, sector in enumerate(proxy.get("about.secondarySector", []), start=1):
            data["Secondary educational sector ({})".format(idx)] = en_with_fallback(
                sector["name"]
            )
        for idx, publisher in enumerate(proxy.get("about.publisher", []), start=1):
            data["Publisher ({})".format(idx)] = en_with_fallback(publisher["name"])

        data["Date published"] = arrow.get(proxy.get("dateCreated")).format(
            "YYYY-MM-DD"
        )
        data["Date last modified"] = arrow.get(proxy.get("dateModified")).format(
            "YYYY-MM-DD"
        )

        for idx, creator in enumerate(proxy.get("about.creator", []), start=1):
            data["Authored by ({})".format(idx)] = en_with_fallback((creator["name"]))

        data["Language".format(idx)] = proxy.get("about.inLanguage[0]")

        data["Country"] = proxy.get("about.location[0].address.addressCountry")
        data["Region"] = proxy.get("about.location[0].address.addressRegion")

        for idx, basedOn in enumerate(proxy.get("about.isBasedOn", []), start=1):
            data["Based on / ID ({})".format(idx)] = basedOn["@id"]
            data["Based on / title ({})".format(idx)] = en_with_fallback(
                basedOn["name"]
            )

        for idx, basisFor in enumerate(proxy.get("about.isBasisFor", []), start=1):
            data["Basis for / ID ({})".format(idx)] = basisFor["@id"]
            data["Basis for / title ({})".format(idx)] = en_with_fallback(
                basisFor["name"]
            )

        for idx, tag in enumerate(proxy.get("about.keywords", []), start=1):
            data["Tags ({})".format(idx)] = tag

        rows.append(data)

    df = pd.DataFrame.from_dict(rows,)[
        [
            "ID",
            "STATUS ON MAP",
            "Title",
            "URL",
            "Map URL",
            "Policy Type",
            "Description",
            "Level",
            "Scope",
            "Primary educational sector",
            "Secondary educational sector (1)",
            "Secondary educational sector (2)",
            "Publisher (1)",
            "Publisher (2)",
            "Date published",
            "Date last modified",
            "Authored by (1)",
            "Authored by (2)",
            "Authored by (3)",
            "Language",
            "Country",
            "Region",
            "Tags (1)",
            "Tags (2)",
            "Tags (3)",
            "Tags (4)",
            "Tags (5)",
            "Tags (6)",
            "Tags (7)",
            "Tags (8)",
            "Focus (1)",
            "Focus (2)",
            "Focus (3)",
            "Focus (4)",
            "Focus (5)",
            "Focus (6)",
            "Focus (7)",
            "Focus (8)",
            "Focus (9)",
            "Focus (10)",
            "Focus (11)",
            "Based on / ID (1)",
            "Based on / title (1)",
            "Based on / ID (2)",
            "Based on / title (2)",
            "Based on / ID (3)",
            "Based on / title (3)",
            "Based on / ID (4)",
            "Based on / title (4)",
            "Basis for / ID (1)",
            "Basis for / title (1)",
            "Basis for / ID (2)",
            "Basis for / title (2)",
            "Basis for / ID (3)",
            "Basis for / title (3)",
            "Basis for / ID (4)",
            "Basis for / title (4)",
            "Basis for / ID (5)",
            "Basis for / title (5)",
            "Basis for / ID (6)",
            "Basis for / title (6)",
        ]
    ]
    df.to_excel("export.xlsx")


if __name__ == "__main__":
    main()

import json
from scalpl import Cut
from collections import OrderedDict


def en_with_fallback(item: dict) -> str:
    try:
        return item["en"]
    except KeyError:
        keys = list(item.keys())
        return item[keys[0]]


def build_concept(name: str):
    terms = json.load(open("assets/{}.json".format(name), "rb"))
    terms_tuples = []

    for term in terms.get("hasTopConcept"):
        _id = "#{}".format(term.get("@id").split("#")[-1])

        name = ""
        for name_dict in term.get("name"):
            if name_dict.get("@language") == "en":
                name = name_dict.get("@value")

        terms_tuples.append([_id, name])
    return terms_tuples


def build_columns(mapping: dict) -> [list, list]:
    columns = []
    rules = []
    for key, lookup in mapping.items():
        if isinstance(lookup, dict):
            column_name = lookup.get("name")
            lookup_type = lookup.get("type")

            if lookup_type == "list":
                lookup_keys = lookup.get("keys")
                for lkey in lookup_keys:
                    columns.append(
                        "{} - {}".format(column_name.capitalize(), lkey.upper())
                    )
                    rules.append(lookup.get("rule"))

            elif lookup_type.startswith("list_"):
                for num in range(1, lookup["count"] + 1):
                    columns.append("{} ({})".format(column_name.capitalize(), num))
                    rules.append(lookup.get("rule"))

            elif lookup_type in ["concept"]:
                columns.append(column_name)
                rules.append(lookup.get("rule"))

            elif lookup_type == "location":
                for prop in lookup.get("properties"):
                    columns.append(prop.get("name").capitalize())
                    rules.append(lookup.get("rule"))

            elif lookup_type == "freefield":
                columns.append(lookup.get("name"))

            else:
                columns.append(column_name.capitalize())
                rules.append(lookup.get("rule"))

    return columns, rules


def build_rows(columns: list, mapping: dict, raw_data: dict, languages: list) -> list:
    rows = []
    for item in raw_data.get("member")[:]:
        data = OrderedDict()
        proxy = Cut(item)

        for key, lookup in mapping.items():
            if isinstance(lookup, dict):
                results = proxy.get(key)
                if not results:
                    continue

                column_name = lookup.get("name", "")
                lookup_type = lookup.get("type")

                if lookup_type == "list":
                    lookup_keys = lookup.get("keys")
                    for lkey in lookup_keys:
                        if results.get(lkey):
                            data[
                                "{} - {}".format(column_name.capitalize(), lkey.upper())
                            ] = results.get(lkey)

                elif lookup_type == "concept":
                    concept = results[0]["name"].get("en")
                    data[column_name] = concept

                elif lookup_type.startswith("list_"):
                    lookup_key = lookup.get("key", lookup.get("lang_key"))

                    for idx, litem in enumerate(
                        results[: lookup.get("count")], start=1
                    ):
                        litem_proxy = Cut(litem)
                        column_name = "{} ({})".format(
                            lookup.get("name").capitalize(), idx
                        )

                        if lookup_type == "list_fk":
                            if lookup.get("lang_key"):
                                value = None
                                for lang in languages:
                                    lang_lookup = "{}.{}".format(lookup_key, lang)
                                    value = litem_proxy.get(lang_lookup)

                                    if value:
                                        data[column_name] = value
                                        break

                                if not value:
                                    # Fallback to first language in the list, if none of preferred
                                    # languages match
                                    data[column_name] = litem_proxy.get(
                                        "{}[0].name".format(lookup_key)
                                    )
                            else:
                                data[column_name] = litem_proxy.get(lookup_key)
                        elif lookup_type == "list_concept":
                            concept = litem_proxy.get("name.en")
                            data[column_name] = concept

                elif lookup_type == "url_id":
                    data[
                        column_name.capitalize()
                    ] = "https://oerworldmap.org/resource/{}".format(proxy.get(key))

                elif lookup_type == "comma":
                    data[column_name.capitalize()] = ", ".join(proxy.get(key))

                elif lookup_type == "direct":
                    data[column_name.capitalize()] = proxy.get(key)

                elif lookup_type == "location":
                    for prop in lookup.get("properties"):
                        column_name = prop.get("name").capitalize()
                        lproxy = Cut(results[0])
                        data[column_name] = lproxy.get(prop.get("key"))

        rows.append(data)

    return rows

import json
import pandas as pd
import requests

from gspread_pandas import Spread
from gspread_formatting import *
from gspread.utils import rowcol_to_a1

from mappings import ORG_FIELD_MAPPING, POLICY_FIELD_MAPPING, SERVICE_FIELD_MAPPING
from utils import build_columns, build_rows, build_concept


class Exporter(object):
    DROPDOWNS = {}

    def __init__(self, name):
        self.__define_dropdowns()
        self.spread = Spread(name)

    def __define_dropdowns(self):
        self.DROPDOWNS["orgs_concept_dropdown_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Concept - Organizations'!B2:B"]),
            showCustomUi=True,
        )
        self.DROPDOWNS["sectors_concept_dropdown_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Concept - Sectors'!B2:B"]),
            showCustomUi=True,
        )

        self.DROPDOWNS["policytypes_concept_dropdown_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Concept - Policytypes'!B2:B"]),
            showCustomUi=True,
        )

        self.DROPDOWNS["servicetypes_concept_dropdown_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Concept - Services'!B2:B"]),
            showCustomUi=True,
        )

        self.DROPDOWNS["sectors_concept_organization_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Organizations'!B2:C"]),
            showCustomUi=True,
        )

    def sheets_concepts(self):
        spread = Spread("OER World Map - France")
        for concept in ["sectors", "organizations", "policyTypes", "services"]:
            df = pd.DataFrame(build_concept(concept), columns=["@id", "name"])
            spread.df_to_sheet(
                df,
                index=False,
                sheet="Concept - {}".format(concept.capitalize()),
                replace=True,
            )

    def _apply_rules(self, rules, rows, sheet):
        for idx, rule in enumerate(rules, start=1):
            if rule:
                start = rowcol_to_a1(col=idx, row=2)
                end = start.split("2")[0]
                cell_range = "{}:{}".format(start, end)

                set_data_validation_for_cell_range(
                    sheet, cell_range, rule=self.DROPDOWNS[rule]
                )

        cell_wrap = CellFormat(wrapStrategy="CLIP")
        end_column = rowcol_to_a1(col=len(rules), row=1).split("1")[0]
        format_cell_ranges(sheet, [("A:{}".format(end_column), cell_wrap)])
        set_row_height(sheet, "1:{}".format(len(rows)), 22)

    def sheets_export(self, mapping=None, sheetname=None, api_url=None):
        cached_filename = "cache/{}.json".format(sheetname.lower())

        r = requests.get(api_url)
        with open(cached_filename, "wb") as f:
            f.write(r.content)

        raw_data = json.load(open(cached_filename, "rb"))

        columns, rules = build_columns(mapping=mapping)
        rows = build_rows(columns=columns, mapping=mapping, raw_data=raw_data)

        df = pd.DataFrame(columns=columns)
        df = df.append(rows, ignore_index=True)

        self.spread.clear_sheet(sheet=sheetname)
        self.spread.df_to_sheet(
            df,
            index=False,
            sheet=sheetname,
            replace=True,
        )

        # noinspection PyUnresolvedReferences
        self._apply_rules(
            rules=rules, rows=rows, sheet=self.spread.spread.worksheet(sheetname)
        )


if __name__ == "__main__":
    exp = Exporter(name="OER World Map - France (drop-downs)")
    # exp.sheets_concepts()
    exp.sheets_export(
        sheetname="Organizations",
        mapping=ORG_FIELD_MAPPING,
        api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.@type=Organization",
    )

    exp.sheets_export(
        sheetname="Policies",
        mapping=POLICY_FIELD_MAPPING,
        api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Policy&filter.feature.properties.location.address.addressCountry=FR",
    )
    exp.sheets_export(
        sheetname="Services",
        mapping=SERVICE_FIELD_MAPPING,
        api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Service&filter.feature.properties.location.address.addressCountry=FR",
    )

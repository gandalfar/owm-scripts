import json
import pandas as pd

from gspread_pandas import Spread
from gspread_formatting import *
from gspread.utils import rowcol_to_a1

from mappings import ORG_FIELD_MAPPING, POLICY_FIELD_MAPPING
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

        self.DROPDOWNS["sectors_concept_organization_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Organizations'!B2:B"]),
            showCustomUi=True,
        )

    def _sheets_concepts(self):
        spread = Spread("OER World Map - France")
        for concept in ["sectors", "organizations", "policyTypes"]:
            df = pd.DataFrame(build_concept(concept), columns=["@id", "name"])
            spread.df_to_sheet(
                df,
                index=False,
                sheet="Concept - {}".format(concept.capitalize()),
                replace=True,
            )

    def _sheets_organizations(self):
        # r = requests.get(
        #     "https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.@type=Organization",
        # )
        # with open("organization.json", "wb") as f:
        #     f.write(r.content)

        raw_data = json.load(open("organization.json", "rb"))

        columns = build_columns(mapping=ORG_FIELD_MAPPING)
        rows = build_rows(columns=columns, mapping=ORG_FIELD_MAPPING, raw_data=raw_data)

        df = pd.DataFrame(columns=columns)
        df = df.append(rows, ignore_index=True)

        spread = Spread("OER World Map - France")
        spread.clear_sheet(sheet="Organizations")
        spread.df_to_sheet(
            df,
            index=False,
            sheet="Organizations",
            replace=True,
        )

        sheet = spread.spread.worksheet("Organizations")

        set_data_validation_for_cell_range(
            sheet, "L2:L", rule=self.DROPDOWNS["orgs_concept_dropdown_rule"]
        )

        set_data_validation_for_cell_range(
            sheet, "M2:M", rule=self.DROPDOWNS["sectors_concept_dropdown_rule"]
        )

    def _apply_rules(self, rules, sheet):
        for idx, rule in enumerate(rules, start=1):
            if rule:
                start = rowcol_to_a1(col=idx, row=2)
                end = start.split("2")[0]
                cell_range = "{}:{}".format(start, end)

                set_data_validation_for_cell_range(
                    sheet, cell_range, rule=self.DROPDOWNS[rule]
                )

        # cell_wrap = CellFormat(wrapStrategy="WRAP")
        # end_column = rowcol_to_a1(col=len(rules), row=1).split("1")[0]
        # format_cell_ranges(sheet, [("A:{}".format(end_column), cell_wrap)])

    def sheets_policies(self, sheetname="Policies"):
        # r = requests.get(
        #     'https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Policy&filter.feature.properties.location.address.addressCountry=%5B"FR"%5D',
        # )
        # with open("cache/policy.json", "wb") as f:
        #     f.write(r.content)

        raw_data = json.load(open("cache/policy.json", "rb"))

        columns, rules = build_columns(mapping=POLICY_FIELD_MAPPING)
        rows = build_rows(
            columns=columns, mapping=POLICY_FIELD_MAPPING, raw_data=raw_data
        )

        df = pd.DataFrame(columns=columns)
        df = df.append(rows, ignore_index=True)

        self.spread.clear_sheet(sheet=sheetname)
        self.spread.df_to_sheet(
            df,
            index=False,
            sheet=sheetname,
            replace=True,
        )

        self._apply_rules(rules=rules, sheet=self.spread.spread.worksheet(sheetname))


if __name__ == "__main__":
    exp = Exporter(name="OER World Map - France")
    # exp._sheets_concepts()
    exp.sheets_policies(sheetname="Policies")

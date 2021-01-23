import json
import pandas as pd

from gspread_pandas import Spread
from gspread_formatting import *

from mappings import ORG_FIELD_MAPPING, POLICY_FIELD_MAPPING
from utils import build_columns, build_rows, build_concept


class Exporter(object):
    DROPDOWNS = {}

    def __init__(self):
        self.__define_dropdowns()

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

    def sheets_policies(self):
        # r = requests.get(
        #     'https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Policy&filter.feature.properties.location.address.addressCountry=%5B"FR"%5D',
        # )
        # with open("policy.json", "wb") as f:
        #     f.write(r.content)

        raw_data = json.load(open("policy.json", "rb"))

        columns = build_columns(mapping=POLICY_FIELD_MAPPING)
        rows = build_rows(
            columns=columns, mapping=POLICY_FIELD_MAPPING, raw_data=raw_data
        )

        df = pd.DataFrame(columns=columns)
        df = df.append(rows, ignore_index=True)

        # df.to_excel("policy-debug.xlsx")
        # return

        spread = Spread("OER World Map - France")
        spread.clear_sheet(sheet="Policies")
        spread.df_to_sheet(
            df,
            index=False,
            sheet="Policies",
            replace=True,
        )

        sheet = spread.spread.worksheet("Policies")

        set_data_validation_for_cell_range(
            sheet, "F2:F", rule=self.DROPDOWNS["policytypes_concept_dropdown_rule"]
        )

        set_data_validation_for_cell_range(
            sheet, "G2:G", rule=self.DROPDOWNS["sectors_concept_dropdown_rule"]
        )

        set_data_validation_for_cell_range(
            sheet, "H2:H", rule=self.DROPDOWNS["sectors_concept_organization_rule"]
        )
        set_data_validation_for_cell_range(
            sheet, "I2:I", rule=self.DROPDOWNS["sectors_concept_organization_rule"]
        )
        set_data_validation_for_cell_range(
            sheet, "J2:J", rule=self.DROPDOWNS["sectors_concept_organization_rule"]
        )

        set_data_validation_for_cell_range(
            sheet, "K2:K", rule=self.DROPDOWNS["sectors_concept_organization_rule"]
        )
        set_data_validation_for_cell_range(
            sheet, "K2:K", rule=self.DROPDOWNS["sectors_concept_organization_rule"]
        )

        cell_wrap = CellFormat(wrapStrategy="WRAP")
        format_cell_ranges(sheet, [("A:N", cell_wrap)])


if __name__ == "__main__":
    exp = Exporter()

    # exp._sheets_concepts()
    exp.sheets_policies()

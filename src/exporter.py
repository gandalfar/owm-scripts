import json
import pandas as pd
import requests

from gspread_pandas import Spread
from gspread_formatting import *
from gspread.utils import rowcol_to_a1


from src.utils import build_columns, build_rows, build_concept


class Exporter(object):
    DROPDOWNS = {}

    def __init__(
        self,
        name: str,
        languages: list,
        use_cache=False,
    ) -> None:
        self.__define_dropdowns()
        self.spread = Spread(name)
        self.use_cache = use_cache
        self.languages = languages

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

        self.DROPDOWNS["sectors_service_rule"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Services'!B2:C"]),
            showCustomUi=True,
        )

        self.DROPDOWNS["static_rights"] = DataValidationRule(
            BooleanCondition("ONE_OF_RANGE", ["='Static - Rights'!A2:A"]),
            showCustomUi=True,
        )

    def sheets_concepts(self):
        for concept in ["sectors", "organizations", "policyTypes", "services"]:
            df = pd.DataFrame(build_concept(concept), columns=["@id", "name"])
            self.spread.df_to_sheet(
                df,
                index=False,
                sheet="Concept - {}".format(concept.capitalize()),
                replace=True,
            )

        df = pd.DataFrame.from_dict({"name": ["floss", "proprietary"]})
        self.spread.clear_sheet(sheet="Static - Rights")
        self.spread.df_to_sheet(
            df,
            index=False,
            sheet="Static - Rights",
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

        if not self.use_cache:
            r = requests.get(api_url)
            with open(cached_filename, "wb") as f:
                f.write(r.content)

        raw_data = json.load(open(cached_filename, "rb"))

        columns, rules = build_columns(mapping=mapping)
        rows = build_rows(
            columns=columns,
            mapping=mapping,
            raw_data=raw_data,
            languages=self.languages,
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

        # noinspection PyUnresolvedReferences
        self._apply_rules(
            rules=rules, rows=rows, sheet=self.spread.spread.worksheet(sheetname)
        )

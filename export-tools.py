from src.exporter import Exporter
from src.mappings import (
    ORG_FIELD_MAPPING,
    POLICY_FIELD_MAPPING,
    SERVICE_FIELD_MAPPING,
    TOOLS_FIELD_MAPPING,
    LANGS,
)

if __name__ == "__main__":
    exp = Exporter(
        name="OER World Map - Commercial Platforms with OER",
        use_cache=True,
        languages=LANGS,
    )
    # exp.sheets_concepts()
    # exp.sheets_export(
    #     sheetname="Organizations",
    #     mapping=ORG_FIELD_MAPPING,
    #     api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.@type=Organization",
    # )

    # exp.sheets_export(
    #     sheetname="Policies",
    #     mapping=POLICY_FIELD_MAPPING,
    #     api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Policy&filter.feature.properties.location.address.addressCountry=FR",
    # )

    # exp.sheets_export(
    #     sheetname="Services",
    #     mapping=SERVICE_FIELD_MAPPING,
    #     api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Service",
    # )

    exp.sheets_export(
        sheetname="Tools",
        mapping=TOOLS_FIELD_MAPPING,
        api_url="https://oerworldmap.org/resource/?size=-1&ext=json&filter.about.%40type=Product",
    )

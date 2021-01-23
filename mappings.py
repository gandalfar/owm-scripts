LANGS = ["en", "fr"]

ORG_FIELD_MAPPING = {
    "feature.id": {"name": "ID", "type": "url_id"},
    "feature.properties.name": {"name": "name", "type": "list", "keys": LANGS},
    "about.description": {"name": "description", "type": "list", "keys": LANGS},
    "feature.properties.additionalType": {
        "name": "Organization type",
        "type": "concept",
        "concept": "https://oerworldmap.org/assets/json/organizations.json",
    },
    "about.primarySector": {
        "name": "Primary sector",
        "type": "concept",
        "concept": "https://oerworldmap.org/assets/json/sectors.json",
    },
}

POLICY_FIELD_MAPPING = {
    "feature.id": {"name": "ID", "type": "url_id"},
    "feature.properties.name": {"name": "name", "type": "list", "keys": LANGS},
    "about.description": {"name": "description", "type": "list", "keys": LANGS},
    "feature.properties.additionalType": {
        "name": "Policy Type",
        "type": "concept",
        "concept": "https://oerworldmap.org/assets/json/policyTypes.json",
        "rule": "policytypes_concept_dropdown_rule",
    },
    "about.primarySector": {
        "name": "Primary sector",
        "type": "concept",
        "concept": "https://oerworldmap.org/assets/json/sectors.json",
        "rule": "sectors_concept_dropdown_rule",
    },
    "about.secondarySector": {
        "name": "secondary sector",
        "type": "list_concept",
        "concept": "https://oerworldmap.org/assets/json/sectors.json",
        "count": 3,
        "rule": "sectors_concept_dropdown_rule",
    },
    "about.publisher": {
        "name": "publisher",
        "type": "list_fk",
        "key": "name.en",
        "count": 3,
        "rule": "sectors_concept_organization_rule",
    },
    "about.keywords": {
        "name": "keywords",
        "type": "comma",
    },
    "about.spatialCoverage": {"name": "level", "type": "direct"},
    "about.scope": {
        "name": "Scope",
        "type": "concept",
        "concept": "https://oerworldmap.org/assets/json/policies.json",
    },
    "about.creator": {
        "name": "authored by",
        "type": "list_fk",
        "key": "name.en",
        "count": 2,
        "rule": "sectors_concept_organization_rule",
    },
    "about.inLanguage": {
        "name": "language",
        "type": "comma",
    },
    "about.location": {
        "type": "location",
        "properties": [
            {"name": "Country", "key": "address.addressCountry"},
            {"name": "Region", "key": "address.addressRegion"},
        ],
    },
    "about.focus": {"name": "focus", "type": "comma"},
    "about.datePublished": {"name": "Published date", "type": "direct"},
    "about.endDate": {"name": "End date", "type": "direct"},
}

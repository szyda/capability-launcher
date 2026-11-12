from app.catalog import CapabilityCatalog


def test_catalog_discovers_capabilities():
    catalog = CapabilityCatalog('capabilities')
    ids = {capability.id for capability in catalog.list()}

    assert {'url_inspector', 'timezone_converter', 'csv_cleaner'} <= ids


def test_catalog_skips_invalid_manifest():
    catalog = CapabilityCatalog('capabilities')
    assert isinstance(catalog.get('url_inspector'), object)
    assert catalog.get('not_real') is None

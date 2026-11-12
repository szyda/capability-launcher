from urllib.parse import urlparse, parse_qs


def run(inputs: dict) -> dict:
    raw_url = inputs.get('url', '')
    parsed = urlparse(raw_url)
    return {
        'scheme': parsed.scheme,
        'host': parsed.hostname,
        'port': parsed.port,
        'path': parsed.path,
        'query_params': parse_qs(parsed.query),
        'is_secure': parsed.scheme in {'https', 'wss'},
    }

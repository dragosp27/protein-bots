import requests
from requests.adapters import HTTPAdapter, Retry

def get_with_retry(url: str, headers=None, timeout=10) -> requests.Response:
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500,502,503,504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    resp = session.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp
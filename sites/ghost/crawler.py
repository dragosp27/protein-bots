from bs4 import BeautifulSoup
from urllib.parse import urljoin
from common.http_client import get_with_retry
from .models import GhostProductStatus, GhostVariant

class GhostCrawler:
    CATEGORY_URL = "https://www.ghostlifestyle.com/collections/supplements/categories-protein"

    def fetch_product_links(self) -> list[str]:
        """Fetch all product URLs from the category page."""
        resp = get_with_retry(self.CATEGORY_URL)
        print(resp.text[:1000])
        soup = BeautifulSoup(resp.text, "html.parser")
        links = []
        # Ghost uses a.card-wrapper for product links
        for a in soup.select("a.card-wrapper"):
            href = a.get("href")
            if href:
                links.append(urljoin(self.CATEGORY_URL, href))
        print(f"[DEBUG] Ghost links found: {links}")
        return list(set(links))  # deduplicate

    def fetch_status_for_product(self, product_url: str) -> GhostProductStatus:
        """Fetch stock info for a single Ghost product."""
        resp = get_with_retry(product_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Product name
        name_tag = soup.select_one("h1.product-title")
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"

        variants = []
        # Flavors are rendered as radio inputs
        flavor_inputs = soup.select(".product-form__option input[type='radio']")
        for inp in flavor_inputs:
            flavor = inp.get("value") or inp.get("data-value") or "Unknown flavor"
            disabled = inp.has_attr("disabled")
            variants.append(GhostVariant(flavor=flavor, in_stock=not disabled))

        if not variants:
            # fallback if no flavor selector
            variants.append(GhostVariant(flavor="default", in_stock=True))

        return GhostProductStatus(name=name, url=product_url, variants=variants)

    def fetch_all(self) -> list[GhostProductStatus]:
        """Fetch all Ghost protein products with their variants."""
        statuses = []
        for url in self.fetch_product_links():
            try:
                statuses.append(self.fetch_status_for_product(url))
            except Exception as e:
                print(f"[GhostCrawler] Error fetching {url}: {e}")
        return statuses

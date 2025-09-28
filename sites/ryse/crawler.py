from bs4 import BeautifulSoup
from .models import ProductStatus, VariantStatus
from common.http_client import get_with_retry

class RyseCrawler:
    PRODUCT_URL = "https://rysesupps.com/products/loaded-protein"

    def fetch_status(self) -> ProductStatus:
        resp = get_with_retry(self.PRODUCT_URL)
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        # product name
        product_name = soup.find("h1").get_text(strip=True)

        # detect “Out of Stock” or in-stock status text
        stock_marker = soup.find(string=lambda t: "Out of Stock" in t)
        # this is simplistic; may need more robust logic
        is_out_of_stock = stock_marker is not None

        # find variant flavors: inspect the flavor list
        # in the HTML we saw a list under “Flavor:” label
        variants = []
        # locate container with flavor options (this might need tuning)
        flavor_container = soup.find(text="Flavor:")
        if flavor_container:
            # its parent may contain sibling elements that list variants
            parent = flavor_container.parent
            # siblings or next siblings
            for sib in parent.find_all_next():
                # simplistic: treat each <option> or <li> or span etc.
                # For now assume plain text flows; sophisticate later
                text = sib.get_text(strip=True)
                if not text:
                    continue
                # break if hits “Serving Size” or “Out of Stock” etc — heuristic
                if "Serving Size" in text or "Out of Stock" in text:
                    break
                # assume this is a flavor name
                variants.append(VariantStatus(flavor=text, in_stock=not is_out_of_stock))

        return ProductStatus(product_name=product_name, variants=variants)
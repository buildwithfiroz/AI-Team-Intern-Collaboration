import asyncio
import json, time, os, re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
AMAZON_USERNAME = os.getenv("AMAZON_USERNAME")
AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")

# login
async def amazon_login(page):
    print("Go to Login page")

    await page.goto("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0", timeout=60000)
    
    time.sleep(4) 
    # Fill email
    await page.fill("input#ap_email", AMAZON_USERNAME)
    await page.click("input#continue")
    
    time.sleep(4)
    # Fill password
    await page.fill("input#ap_password", AMAZON_PASSWORD)
    await page.click("input#signInSubmit")
    
    time.sleep(2)
    # Wait login complete
    await page.wait_for_selector("#nav-link-accountList", timeout=15000)
    print("✅ Logged in ")


async def scrape_amazon(url, max_pages=10):
    start_time =time.time()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Login first
        await amazon_login(page)
        
        # Phir product page open karo
        await page.goto(url, timeout=60000)

        # Product page ka HTML
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        def _extract_text(el):
            return el.get_text(strip=True) if el else None
        
        def extract_average_rating(soup):
            selectors = [
                "#acrPopover .a-icon-alt",                     
                "#acrPopover span.a-size-small.a-color-base"  
            ]
            for sel in selectors:
                tag = soup.select_one(sel)
                if tag:
                    text = tag.get_text(strip=True)
                    return text.split(" ")[0] if "out of" in text else text
            return None


        # ---------- Product Details ----------
        product = {
            "title": _extract_text(soup.select_one("#productTitle")),
            "img_url": soup.select_one("#landingImage")["src"] if soup.select_one("#landingImage") else None,
            "price_value": _extract_text(soup.select_one("span.a-price .a-offscreen")),
            "currency_symbol": "₹" if _extract_text(soup.select_one("span.a-price-symbol")) else None,
            "average_rating": extract_average_rating(soup),
            "reviews_count": _extract_text(soup.select_one("#acrCustomerReviewText")),
            "seller": _extract_text(soup.select_one("#sellerProfileTriggerId")),
            "availability": _extract_text(soup.select_one("#availability span")),
            "last_month_sale": _extract_text(soup.select_one("#social-proofing-faceout-title-tk_bought"))
        }

        print("\nProduct ------->", product, "\n\n")

        # ---------- Reviews Section ----------
        reviews = []
        try:
            reviews_link = soup.select_one("a[data-hook='see-all-reviews-link-foot']")
            print("Review page link -----> ", reviews_link["href"])
            if reviews_link:
                reviews_url = "https://www.amazon.in" + reviews_link["href"]

                await page.goto(reviews_url, timeout=60000)

                # reviews_section = reviews_url + "#cm_cr-review_list"
                print("Review -----> ", reviews_url)

                page_num = 1
                while page_num <= max_pages:

                    try:
                        await page.wait_for_selector("#cm_cr-review_list", timeout=20000)

                        rev_html = await page.inner_html("#cm_cr-review_list")
                        rev_soup = BeautifulSoup(rev_html, "html.parser")

                        for rev in rev_soup.select('li[data-hook="review"]'):
                            
                            # Rating text extract
                            rating_text = _extract_text(
                                rev.select_one("i[data-hook='review-star-rating'] span")
                                or rev.select_one("i[data-hook='cmps-review-star-rating'] span")
                            )
                            rating = None
                            if rating_text:
                                match = re.search(r"(\d+(\.\d+)?)", rating_text)  # only number part
                                if match:
                                    rating = match.group(1)
                            
                            review = {
                                "id": rev.get("id"),
                                "author": _extract_text(rev.select_one("span.a-profile-name")),
                                "rating": rating,
                                "text": _extract_text(rev.select_one("span[data-hook='review-body'] span")),
                                "date": _extract_text(rev.select_one("span[data-hook='review-date']")),
                                "format": _extract_text(rev.select_one("a[data-hook='format-strip']")),
                                "verified_purchase": bool(rev.select_one("span[data-hook='avp-badge']")),
                                "helpful_votes": _extract_text(rev.select_one("span[data-hook='helpful-vote-statement']"))
                            }
                            reviews.append(review)

                            time.sleep(1)

                        next_btn = rev_soup.select_one("li.a-last a")
                        if next_btn:
                            print(f"\n➡️ Going to next page {page_num}...")
                            await page.click("li.a-last a")   # ✅ Click karo
                            await page.wait_for_selector("#cm_cr-review_list", timeout=20000)  # ✅ Wait for reviews to load
                            page_num += 1
                        else:
                            print("❌ No more review pages.")
                            break

                    except:
                        print("⚠️ Reviews not visible, scrolling down...")
                        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(5000)  # wait 5s

        except Exception as e:
            print("Review scraping error:", e)


        await browser.close()

        end_time = time.time()
        print(f"Scrap data in {end_time - start_time } seconds")

        return {"product": product, "reviews": reviews}


    print("✅ Scraping Done. Reviews fetched:", len(data["reviews"]))

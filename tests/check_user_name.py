from playwright.sync_api import sync_playwright

def get_user_info():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [p_item for p_item in context.pages if "linkedin.com" in p_item.url][0]
        
        info = page.evaluate("""() => {
            const meImage = document.querySelector('img.global-nav__me-photo, img.feed-identity-module__member-photo');
            const navButtons = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText,
                aria: b.getAttribute('aria-label')
            })).filter(b => (b.aria && b.aria.includes('Foto de')) || (b.text && b.text.includes('Eu')));
            
            return {
                imgAlt: meImage ? meImage.getAttribute('alt') : null,
                navButtons: navButtons
            };
        }""")
        print("User Info:", info)

if __name__ == "__main__":
    get_user_info()

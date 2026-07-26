from playwright.sync_api import sync_playwright

def inspect_linkedin():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [p_item for p_item in context.pages if "linkedin.com" in p_item.url][0]
        
        info = page.evaluate("""() => {
            const commentBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Comentar'));
            const seeMoreBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('mais'));
            
            return {
                commentBtnsCount: commentBtns.length,
                seeMoreBtnsCount: seeMoreBtns.length,
                seeMoreBtnsInfo: seeMoreBtns.slice(0, 5).map(b => ({
                    text: b.innerText,
                    className: b.className
                }))
            };
        }""")
        print("DOM Info:", info)

if __name__ == "__main__":
    inspect_linkedin()

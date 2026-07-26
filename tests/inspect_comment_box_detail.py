import time
from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [p_item for p_item in context.pages if "linkedin.com" in p_item.url][0]
        page.bring_to_front()
        
        comment_btn = page.query_selector('button[aria-label*="Comentar"]')
        if comment_btn:
            comment_btn.scroll_into_view_if_needed()
            comment_btn.click()
            time.sleep(2)
            
            detail = page.evaluate("""() => {
                const textboxes = Array.from(document.querySelectorAll('div[role="textbox"], div[contenteditable="true"]'));
                const active = document.activeElement;
                const buttons = Array.from(document.querySelectorAll('button'));
                
                return {
                    textboxes: textboxes.map(t => ({
                        tagName: t.tagName,
                        className: t.className,
                        role: t.getAttribute('role'),
                        contenteditable: t.getAttribute('contenteditable'),
                        innerText: t.innerText,
                        isVisible: t.offsetWidth > 0 && t.offsetHeight > 0
                    })),
                    activeElement: {
                        tagName: active.tagName,
                        className: active.className,
                        role: active.getAttribute('role')
                    },
                    submitCandidates: buttons.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0).map(b => ({
                        text: b.innerText.trim(),
                        ariaLabel: b.getAttribute('aria-label'),
                        className: b.className,
                        disabled: b.disabled
                    })).filter(b => b.text === 'Comentar' || b.text === 'Publicar' || (b.ariaLabel && b.ariaLabel.includes('Publicar')))
                };
            }""")
            print("Inspection detail:", detail)

if __name__ == "__main__":
    inspect()

import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import sync_playwright

def test_submit():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [p_item for p_item in context.pages if "linkedin.com" in p_item.url][0]
        page.bring_to_front()
        
        result = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const submitBtn = btns.find(b => !b.disabled && b.innerText.trim() === 'Comentar' && (!b.getAttribute('aria-label') || b.getAttribute('aria-label') === ''));
            if (submitBtn) {
                submitBtn.click();
                return { success: true, text: submitBtn.innerText, className: submitBtn.className };
            }
            return { success: false };
        }""")
        print("[Teste Submit] Resultado:", result)

if __name__ == "__main__":
    test_submit()

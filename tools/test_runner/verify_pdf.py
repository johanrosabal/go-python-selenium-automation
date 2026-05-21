import os
import sys
import time

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from core.ui.common.driver_manager import DriverManager
from core.utils.config_manager import ConfigManager

def main():
    print("Loading config...")
    ConfigManager.load_config("applications/web/demo", "qa")
    print("Initializing webdriver...")
    driver = DriverManager.get_driver(headless=True)
    try:
        url = "http://localhost:5000"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Check title
        title = driver.title
        print(f"Page loaded. Title: {title}")
        assert "God Tier Test Runner" in title, f"Unexpected title: {title}"
        
        # Check html2pdf library presence
        print("Checking html2pdf library...")
        has_html2pdf = driver.execute_script("return typeof html2pdf !== 'undefined'")
        print(f"html2pdf library loaded: {has_html2pdf}")
        assert has_html2pdf, "html2pdf library is not loaded on the page!"
        
        # Check functions
        has_generate = driver.execute_script("return typeof generatePDFReport === 'function'")
        print(f"generatePDFReport function exists: {has_generate}")
        assert has_generate, "generatePDFReport function is not defined!"
        
        # Verify that html2canvas generates non-blank canvas pixels (High-Fidelity verification)
        print("Verifying html2canvas output is NOT blank using canvas pixel analysis...")
        js_verification = r"""
        const done = arguments[arguments.length - 1];
        
        // Save original body styles to prevent layout breakage
        const originalOverflow = document.body.style.overflow;
        const originalHeight = document.body.style.height;

        // Override body styles to allow html2canvas to measure full height
        document.body.style.overflow = 'visible';
        document.body.style.height = 'auto';

        // Build a mock request for generation
        const mockReq = {
            testName: "SEARCH-001 - Policy Search Example",
            method: "POST",
            url: "https://wapi-search-cus-test.azurewebsites.net/api/policy-search",
            status: "200 OK",
            time: "0.45s",
            reqHeaders: "{'Content-Type': 'application/json', 'X-Legacy': 'True'}",
            reqBody: '{"policyNumber": "NICO998877"}',
            resHeaders: `{"Date": "Thu, 21 May 2026 14:57:47 GMT", "Content-Type": "application/json; charset=utf-8", "Content-Length": "70", "Connection": "keep-alive", "access-control-allow-credentials": "true", "access-control-expose-headers": "Location", "Cache-Control": "no-cache", "etag": "W/\\"46-72q5oVUmp94Lb+3KeNKLCz+xhMw\\"", "expires": "-1", "location": "https://json-placeholder.typicode.com/posts/101", "nel": "{\\"report_to\\":\\"heroku-nel\\",\\"response_headers\\":[\\"Via\\"],\\"max_age\\":3600,\\"success_fraction\\":0.01,\\"failure_fraction\\":0.1}", "pragma": "no-cache", "report-to": "{\\"group\\":\\"heroku-nel\\",\\"endpoints\\":[{\\"url\\":\\"https://nel.heroku.com/reports?s=hozQKH0cWcSOQ1j7zVlpWlnKs%2FawNgAAHC%2FY%2FvVBMa%2Fc%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1779375467\\"}],\\"max_age\\":3600}", "reporting-endpoints": "heroku-nel=\\"https://nel.heroku.com/reports?s=hozQKH0cWcSOQ1j7zVlpWlnKs%2FawNgAAHC%2FY%2FvVBMa%2Fc%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1779375467\\"", "Server": "cloudflare", "vary": "Origin, X-HTTP-Method-Override, Accept-Encoding", "via": "2.0 heroku-router", "x-content-type-options": "nosniff", "x-powered-by": "Express", "x-ratelimit-limit": "1000", "x-ratelimit-remaining": "999", "x-ratelimit-reset": "1779375495", "cf-cache-status": "DYNAMIC", "CF-RAY": "9ff46f802f30c8db-SJO", "alt-svc": "h3=\\":443\\"; ma=86400"}`,
            resBody: '[{"id": 1, "status": "Active"}]'
        };

        // Create a wrapper div that is absolute positioned offscreen/below fold
        const wrapperDiv = document.createElement('div');
        wrapperDiv.style.position = 'absolute';
        wrapperDiv.style.left = '0';
        wrapperDiv.style.top = (document.documentElement.scrollHeight + 100) + 'px';
        wrapperDiv.style.zIndex = '-9999';
        wrapperDiv.style.width = '790px';
        wrapperDiv.style.background = '#ffffff';

        // Create the actual container with static positioning
        const container = document.createElement('div');
        container.style.color = '#1f2937';
        container.style.padding = '30px';
        container.style.fontFamily = 'sans-serif';
        container.style.fontSize = '12px';
        
        // Build HTML
        container.innerHTML = buildRequestEvidenceHTML(mockReq, 0, 1);
        
        // Assert that the headers are parsed and rendered in table rows (not as single pre block)
        const rows = container.querySelectorAll('.headers-table tbody tr');
        let foundContentType = false;
        let foundXLegacy = false;
        let foundDate = false;
        let foundAltSvc = false;
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length === 2) {
                const key = cells[0].textContent.trim();
                const val = cells[1].textContent.trim();
                if (key === 'Content-Type' && val === 'application/json') foundContentType = true;
                if (key === 'X-Legacy' && val === 'True') foundXLegacy = true;
                if (key === 'Date' && val === 'Thu, 21 May 2026 14:57:47 GMT') foundDate = true;
                if (key === 'alt-svc' && val.includes('ma=86400')) foundAltSvc = true;
            }
        });
        
        if (!foundContentType || !foundXLegacy || !foundDate || !foundAltSvc) {
            done({ error: "Parsing assertions failed! Headers were not correctly parsed or rendered as individual key-value rows. Rows found: " + rows.length + " Date: " + foundDate + " AltSvc: " + foundAltSvc });
            return;
        }

        wrapperDiv.appendChild(container);
        document.body.appendChild(wrapperDiv);
        
        // Use html2pdf to build canvas and inspect pixels (from container, not wrapperDiv)
        html2pdf().from(container).toCanvas().get('canvas').then(function(canvas) {
            // Restore body styles and cleanup
            document.body.style.overflow = originalOverflow;
            document.body.style.height = originalHeight;
            document.body.removeChild(wrapperDiv);
            
            const ctx = canvas.getContext('2d');
            const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            
            let isBlank = true;
            let nonBlankPixels = 0;
            
            for (let i = 0; i < imgData.length; i += 4) {
                const r = imgData[i];
                const g = imgData[i+1];
                const b = imgData[i+2];
                const a = imgData[i+3];
                
                // If the pixel is not transparent (a > 0) and not pure white (r,g,b != 255)
                if (a > 0 && !(r === 255 && g === 255 && b === 255)) {
                    isBlank = false;
                    nonBlankPixels++;
                }
            }
            
            done({ isBlank: isBlank, nonBlankPixels: nonBlankPixels, width: canvas.width, height: canvas.height });
        }).catch(function(err) {
            // Restore body styles and cleanup
            document.body.style.overflow = originalOverflow;
            document.body.style.height = originalHeight;
            if (wrapperDiv.parentNode) document.body.removeChild(wrapperDiv);
            done({ error: err.message || String(err) });
        });
        """
        
        # Set longer script timeout to allow canvas rendering
        driver.set_script_timeout(15)
        result = driver.execute_async_script(js_verification)
        
        if "error" in result:
            print(f"Canvas rendering failed: {result['error']}")
            sys.exit(1)
            
        print(f"Canvas info: size={result['width']}x{result['height']}, isBlank={result['isBlank']}, nonBlankPixels={result['nonBlankPixels']}")
        
        if result['isBlank']:
            print("ERROR: Rendered canvas is completely blank! This means the generated PDF would be blank.")
            sys.exit(1)
        else:
            print("SUCCESS: Canvas has content (non-blank pixels detected). PDF will render correctly!")
            
        # Clean run of PDF generation functions to verify they don't break
        print("Running exportRequestToPDF mock injection validation...")
        driver.execute_script("""
             sessionRequests = [{
                 testName: "SEARCH-001 - Policy Search Example",
                 method: "POST",
                 url: "https://wapi-search-cus-test.azurewebsites.net/api/policy-search",
                 status: "200 OK",
                 time: "0.45s",
                 reqHeaders: "{'Content-Type': 'application/json', 'X-Legacy': 'True'}",
                 reqBody: '{"policyNumber": "NICO998877"}',
                 resHeaders: "{'Content-Type': 'application/json', 'X-Legacy': 'True'}",
                 resBody: '[{"id": 1, "status": "Active"}]'
             }];
             activeRequestIndex = 0;
             exportRequestToPDF();
        """)
        print("Verification completed successfully!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

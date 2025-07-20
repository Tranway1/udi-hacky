# pip install playwright==1.* && playwright install chromium
import json
import time
from pathlib import Path
from typing import Optional, Union

from playwright.sync_api import (
    sync_playwright,
    ConsoleMessage,
    Error,
    Request,
)

EDITOR_URL = "https://hms-dbmi.github.io/udi-grammar/#/Editor"


def udi_editor_to_image(
    udi_spec: dict,
    out_file: Union[str, Path] = "chart.png",
    *,
    debug: bool = False,
    headless: Optional[bool] = None,   # None ⇒ headless = not debug
    timeout: int = 15_000,             # ms
) -> Path:
    headless = not debug if headless is None else headless
    out_file = Path(out_file).expanduser().resolve()
    json_text = json.dumps(udi_spec, indent=2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # ─── optional debug hooks ────────────────────────────────────────
        if debug:

            def _console(m: ConsoleMessage):
                print(f"[CONSOLE] {m.type}: {m.text}")

            def _js_err(e: Error):
                print("[JS ERROR]", e)

            def _req_fail(r: Request):
                print(f"[FAILED] {r.url} – {r.failure}")

            page.on("console", _console)
            page.on("pageerror", _js_err)
            page.on("requestfailed", _req_fail)

        # ─── 1. load the editor page ─────────────────────────────────────
        page.goto(EDITOR_URL, wait_until="networkidle")

        # ─── 2. wait until Monaco editor is ready, then inject JSON ─────
        page.wait_for_function("window.editor && window.editor.setValue")
        page.evaluate(
            """(json) => {
                  window.editor.setValue(json);
                  window.editor.setScrollPosition({ scrollTop: 0 });
               }""",
            json_text,
        )

        # ─── 3. wait until Vega canvas appears ───────────────────────────
        page.wait_for_selector(".vega-chart-container canvas", timeout=timeout)
        time.sleep(0.2)  # a tiny grace period for final paint

        # ─── 4. screenshot just the chart ───────────────────────────────
        page.locator(".vega-chart-container").screenshot(path=str(out_file))

        if debug:
            print(f"[INFO] Screenshot saved to {out_file}")
            print("[DEBUG] Close the Chromium window to exit …")
            page.wait_for_timeout(1e8)        # keep window open
        else:
            browser.close()

    return out_file


# ───────────── quick self-test ───────────────────────────────────────────
if __name__ == "__main__":
    SPEC = {
  "source": {
    "name": "donors",
    "source": "./data/donors.csv"
  },
  "representation": {
    "mark": "point",
    "mapping": [
      {
        "encoding": "y",
        "field": "height_value",
        "type": "quantitative"
      },
      {
        "encoding": "x",
        "field": "weight_value",
        "type": "quantitative"
      }
    ]
  }
}

    udi_editor_to_image(SPEC, "donors10.png", debug=True)
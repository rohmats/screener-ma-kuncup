"""
Fetch list of all stocks listed on BEI (Bursa Efek Indonesia).

Primary source: IDX API endpoint
Fallback: local data/all_stocks.csv file
"""

import os
import time
import requests
import pandas as pd
import yfinance as yf

_DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "all_stocks.csv")

IDX_API_URL = (
    "https://www.idx.co.id/primary/TradingSummary/GetStockList"
    "?language=id&start=0&length=9999"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.idx.co.id/",
}


def _fetch_from_idx_api() -> list[str]:
    """Fetch ticker list from the IDX trading summary API."""
    resp = requests.get(IDX_API_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    tickers = [item["Code"].strip() for item in data.get("data", []) if item.get("Code")]
    return [f"{t}.JK" for t in tickers if t]


def _fetch_from_idx_member_api() -> list[str]:
    """Fetch ticker list from IDX member stock list (fallback API endpoint)."""
    url = "https://www.idx.co.id/primary/ListedCompany/GetStockList"
    params = {"language": "id", "start": 0, "length": 9999}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    tickers: list[str] = []
    for item in data.get("data", []):
        code = (item.get("KodeEmiten") or item.get("Code") or "").strip()
        if code:
            tickers.append(f"{code}.JK")
    return tickers


def _load_from_csv(filepath: str) -> list[str]:
    """Load ticker list from a local CSV file."""
    df = pd.read_csv(filepath)
    col = next(
        (c for c in df.columns if c.lower() in ("ticker", "code", "symbol", "kode")),
        df.columns[0],
    )
    return df[col].dropna().astype(str).str.strip().tolist()


def fetch_all_bei_tickers(
    csv_path: str = _DEFAULT_CSV,
    update_csv: bool = True,
) -> list[str]:
    """Fetch all ticker symbols listed on BEI.

    Tries live API sources first.  If all remote calls fail, falls back to the
    local CSV file at *csv_path*.  When *update_csv* is True and a live fetch
    succeeds, the CSV is refreshed.

    Returns a list of ticker strings with the ``.JK`` suffix understood by
    yfinance (e.g. ``["AALI.JK", "ABBA.JK", ...]``).
    """
    tickers: list[str] = []
    errors: list[str] = []

    for attempt_fn in (_fetch_from_idx_api, _fetch_from_idx_member_api):
        try:
            tickers = attempt_fn()
            if tickers:
                break
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{attempt_fn.__name__}: {exc}")
            time.sleep(1)

    if not tickers:
        if errors:
            print(f"[fetch_bei_stocks] Remote fetch failed: {'; '.join(errors)}")
        if os.path.exists(csv_path):
            print(f"[fetch_bei_stocks] Using cached list from {csv_path}")
            tickers = _load_from_csv(csv_path)
        else:
            raise RuntimeError(
                "Could not fetch BEI stock list and no local fallback CSV found. "
                f"Attempted: {'; '.join(errors)}"
            )
    elif update_csv:
        save_stock_list(tickers, csv_path)

    return tickers


def fetch_all_bei_tickers_from_yahoo(
    csv_path: str = _DEFAULT_CSV,
    update_csv: bool = True,
) -> list[str]:
    """Fetch BEI symbols from Yahoo screener using yfinance.

    Uses `region=id` + `exchange=JKT` and paginates all results.
    Returns symbols with `.JK` suffix.
    """
    query = yf.EquityQuery(
        "and",
        [
            yf.EquityQuery("eq", ["region", "id"]),
            yf.EquityQuery("eq", ["exchange", "JKT"]),
        ],
    )

    first_page = yf.screen(query, size=250, offset=0)
    total = int(first_page.get("total") or 0)

    symbols: list[str] = []
    for offset in range(0, total, 250):
        page = yf.screen(query, size=250, offset=offset)
        quotes = page.get("quotes", [])
        symbols.extend([q.get("symbol", "").strip().upper() for q in quotes if q.get("symbol")])

    symbols = [s for s in symbols if s]
    symbols = list(dict.fromkeys(symbols))

    if update_csv and symbols:
        save_stock_list(symbols, csv_path)

    return symbols


def save_stock_list(tickers: list[str], filepath: str = _DEFAULT_CSV) -> None:
    """Save ticker list to a CSV file."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df = pd.DataFrame({"ticker": tickers})
    df.to_csv(filepath, index=False)
    print(f"[fetch_bei_stocks] Saved {len(tickers)} tickers to {filepath}")


if __name__ == "__main__":
    result = fetch_all_bei_tickers()
    print(f"Fetched {len(result)} tickers")
    print(result[:10])

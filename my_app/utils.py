# ── utils.py ────────────────────────────────────────────────────────────────
import hashlib, logging, random, time
from typing import Final

import numpy as np
import pandas as pd
import yfinance as yf
from django.core.cache import cache

# yfinance 0.2.37+: YFRateLimitError lives here; fall back to a generic error
try:
    from yfinance.shared._exceptions import YFRateLimitError
except ImportError:         # old yfinance or path changed
    class YFRateLimitError(Exception):  # type: ignore
        pass


log = logging.getLogger(__name__)

CACHE_TTL: Final[int] = 60 * 60 * 24         # 24 h


# --------------------------------------------------------------------------- #
# Key helpers
# --------------------------------------------------------------------------- #
def _make_cache_key(symbol: str, start: str, end: str, sma: bool) -> str:
    raw = f"{symbol}|{start}|{end}|{int(sma)}"
    return "stockdata:" + hashlib.sha1(raw.encode()).hexdigest()


# --------------------------------------------------------------------------- #
# Downloader with retry / back‑off
# --------------------------------------------------------------------------- #
def _download_with_retry(symbol: str, start: str, end: str,
                         max_tries: int = 5) -> pd.DataFrame:
    """
    Call yf.download with exponential back‑off.
    Raises the last exception if all retries fail.
    """
    for attempt in range(max_tries):
        try:
            return yf.download(symbol, start=start, end=end, auto_adjust=True)

        except YFRateLimitError:
            wait = 2 ** attempt + random.random()
            log.warning("Rate‑limited on %s (try %s/%s) – sleeping %.1fs",
                        symbol, attempt + 1, max_tries, wait)
            time.sleep(wait)

    # If we exit the loop we never succeeded
    raise YFRateLimitError(f"Exceeded {max_tries} retries for {symbol}")


# --------------------------------------------------------------------------- #
# Public helper
# --------------------------------------------------------------------------- #
def download_n_clean_data(symbol: str,
                          start_date: str,
                          end_date: str,
                          compute_sma: bool = True) -> pd.DataFrame:
    """
    Download (with caching) + normalise columns + add optional SMA columns.
    """

    key = _make_cache_key(symbol, start_date, end_date, compute_sma)

    # ---------- 1) fast path: cached ---------- #
    cached = cache.get(key)
    if cached is not None:
        print("Serving already cached data")
        return pd.read_json(cached, orient="split")

    # ---------- 2) slow path: Yahoo ---------- #
    try:
        df = _download_with_retry(symbol, start_date, end_date)
        print("Downloaded data from Yahoo")
    except YFRateLimitError:
        stale = cache.get(key)          # might be None
        if stale:
            log.warning("Serving *stale* cached data for %s", symbol)
            return pd.read_json(stale, orient="split")
        raise                                  # nothing cached – bubble up

    # ---------- 3) tidy the DataFrame ---------- #
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Date'] = df['Date'].apply(lambda x: x.timestamp())

    if compute_sma:
        df['sma_50'] = df['Close'].rolling(50).mean()
        df['sma_200'] = df['Close'].rolling(200).mean()

    df.replace({np.nan: None}, inplace=True)

    # ---------- 4) cache JSON blob ---------- #
    cache.set(key, df.to_json(orient="split"), CACHE_TTL)

    return df

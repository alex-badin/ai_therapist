"""Helpers for loading and persisting prompts in Google Sheets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional

try:  # Streamlit is optional outside the web app
    import streamlit as st
    from streamlit_gsheets import GSheetsConnection

    try:  # runtime helper appeared in newer Streamlit releases
        from streamlit import runtime  # type: ignore
    except Exception:  # Older Streamlit versions simply omit the module
        runtime = None  # type: ignore

    _STREAMLIT_AVAILABLE = True
except Exception:  # pragma: no cover - fallback when Streamlit is unavailable
    st = None  # type: ignore
    runtime = None  # type: ignore
    GSheetsConnection = None  # type: ignore
    _STREAMLIT_AVAILABLE = False

try:
    import pandas as pd
except ImportError:  # pragma: no cover - pandas ships with Streamlit but guard just in case
    pd = None  # type: ignore


PROMPT_KEYS = ["router", "dbt", "ifs", "tre", "memory"]
DEFAULT_WORKSHEET = "Prompts"


def _current_timestamp() -> str:
    """Return an ISO timestamp in UTC."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if _STREAMLIT_AVAILABLE:

    @st.cache_data(ttl=300, show_spinner=False)
    def _fetch_prompt_table(worksheet: Optional[str]) -> "pd.DataFrame":  # type: ignore # pragma: no cover - executed inside Streamlit
        """Fetch the prompt table from Google Sheets."""

        conn = st.connection("gsheets", type=GSheetsConnection)
        if worksheet:
            return conn.read(worksheet=worksheet)
        return conn.read()

else:  # pragma: no cover - executed outside Streamlit runtime

    def _fetch_prompt_table(worksheet: Optional[str]):
        raise RuntimeError("Streamlit runtime is not available")


@dataclass
class PromptRecord:
    """Simple structure describing a stored prompt."""

    key: str
    prompt: str
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None


class PromptStore:
    """Loads and saves prompts to a shared Google Sheet when available."""

    def __init__(self, worksheet: Optional[str] = None):
        self.worksheet = worksheet or DEFAULT_WORKSHEET
        self.enabled = False
        self.last_error: Optional[str] = None

        if not _STREAMLIT_AVAILABLE or pd is None:
            return

        if runtime is not None:
            try:
                if not runtime.exists():  # type: ignore[union-attr]
                    return
            except Exception:
                pass

        try:
            connection_settings = {}
            try:
                connection_settings = st.secrets.get("connections", {}).get("gsheets", {})  # type: ignore[arg-type]
            except Exception:
                connection_settings = {}

            worksheet_secret = connection_settings.get("worksheet") if isinstance(connection_settings, dict) else None
            if worksheet_secret:
                self.worksheet = str(worksheet_secret)

            # Attempt a lightweight access to verify configuration.
            try:
                _ = connection_settings.get("spreadsheet")
            except Exception:
                pass

            self.enabled = True
        except Exception as exc:  # pragma: no cover - defensive guard
            self.last_error = str(exc)
            self.enabled = False

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def load_all(self) -> Dict[str, PromptRecord]:
        """Return prompts stored remotely keyed by agent."""

        if not self.enabled:
            return {}

        try:
            table = _fetch_prompt_table(self.worksheet)
        except Exception as exc:  # pragma: no cover - logging via last_error
            self.last_error = str(exc)
            self.enabled = False
            return {}

        if table is None or table.empty:
            return {}

        prompts: Dict[str, PromptRecord] = {}

        for _, row in table.iterrows():
            key = str(row.get("key", "")).strip()
            if not key:
                continue
            prompts[key] = PromptRecord(
                key=key,
                prompt=str(row.get("prompt", "")),
                updated_at=str(row.get("updated_at", "")) or None,
                updated_by=str(row.get("updated_by", "")) or None,
            )

        return prompts

    def get_all(self, defaults: Dict[str, str]) -> Dict[str, str]:
        """Return defaults overlaid with remote overrides."""

        merged = dict(defaults)
        overrides = self.load_all()
        for key, record in overrides.items():
            if record.prompt:
                merged[key] = record.prompt
        return merged

    def get_prompt(self, key: str, default: str) -> str:
        """Get a single prompt, falling back to the provided default."""

        overrides = self.load_all()
        if key in overrides and overrides[key].prompt:
            return overrides[key].prompt
        return default

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------
    def update_prompt(self, key: str, prompt: str, updated_by: Optional[str] = None) -> bool:
        """Persist a prompt back to Google Sheets."""

        if not self.enabled or pd is None:
            return False

        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            if self.worksheet:
                table = conn.read(worksheet=self.worksheet)
            else:
                table = conn.read()
        except Exception as exc:
            self.last_error = str(exc)
            self.enabled = False
            return False

        if table is None or table.empty:
            table = pd.DataFrame(columns=["key", "prompt", "updated_at", "updated_by"])

        for column in ["key", "prompt", "updated_at", "updated_by"]:
            if column not in table.columns:
                table[column] = ""

        mask = table["key"].astype(str) == str(key)
        timestamp = _current_timestamp()

        if mask.any():
            table.loc[mask, "prompt"] = prompt
            table.loc[mask, "updated_at"] = timestamp
            if updated_by is not None:
                table.loc[mask, "updated_by"] = updated_by
        else:
            new_row = {
                "key": key,
                "prompt": prompt,
                "updated_at": timestamp,
                "updated_by": updated_by or "",
            }
            table = pd.concat([table, pd.DataFrame([new_row])], ignore_index=True)

        try:
            if self.worksheet:
                conn.update(worksheet=self.worksheet, data=table)
            else:
                conn.update(data=table)
        except Exception as exc:
            self.last_error = str(exc)
            return False

        self.last_error = None
        self.clear_cache()
        return True

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------
    def clear_cache(self) -> None:
        """Invalidate any cached prompt data."""

        if _STREAMLIT_AVAILABLE:
            try:
                _fetch_prompt_table.clear()  # type: ignore[attr-defined]
            except Exception:
                pass

    def status(self) -> str:
        """Return a human-readable status string for the UI."""

        if self.enabled:
            return "Connected"
        if self.last_error:
            return f"Disabled ({self.last_error})"
        return "Disabled"


__all__ = ["PromptStore", "PROMPT_KEYS", "DEFAULT_WORKSHEET"]

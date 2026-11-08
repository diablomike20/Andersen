#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Andersen Launcher
=================
Asztali indító a https://github.com/diablomike20/Andersen projekthez.

- első indításkor letölti a forráskódot és a függőségeket,
- elindítja a webes fejlesztői szervert, és megnyitja a böngészőt,
- kezeli a Tauri asztali módot, a frissítést és a folyamat leállítását.

Csak a Python szabványos könyvtárát és a tkintert használja.
A mellékelt assets/ mappa ikonjait a tools/make_assets.py állítja elő.
"""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, font as tkfont, messagebox, ttk
import tkinter as tk

try:
    from PIL import Image, ImageTk

    HAS_PIL = True
except Exception:  # pragma: no cover - a PIL opcionális
    HAS_PIL = False


# ---------------------------------------------------------------------------
# Állandók
# ---------------------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"
CONFIG_FILE = APP_DIR / "launcher_config.json"

REPO_URL = "https://github.com/diablomike20/Andersen.git"
REPO_WEB = "github.com/diablomike20/Andersen"
APP_BASE = "/Andersen/"
APP_URL = f"http://127.0.0.1:3000{APP_BASE}"
AGENTS_MARKER = "<!-- Andersen Launcher: generated placeholder -->"
PORT = 3000
REQUIRED_NODE = (22, 19, 0)
REQUIRED_PNPM = "12.13.0"
LAUNCHER_VERSION = "1.0"

# Andersen-paletta
BG = "#0A1220"
BG_DEEP = "#070D18"
PANEL = "#101B2D"
PANEL_2 = "#16253C"
PANEL_3 = "#1C2E49"
BORDER = "#22385A"
BORDER_SOFT = "#1A2B45"
GOLD = "#D6B36D"
GOLD_BRIGHT = "#E8CC92"
GOLD_DIM = "#9A814F"
TEXT = "#E8E1D2"
TEXT_SOFT = "#C3CFDF"
MUTED = "#8296B0"
MUTED_DIM = "#5D7290"
GREEN = "#6FD39A"
RED = "#F07C7C"
AMBER = "#F0C463"

ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

ENV_LABELS = {
    "git": "Git",
    "node": "Node.js",
    "pnpm": "pnpm",
    "repo": "Forrás",
    "port": "Port 3000",
}

LEVEL_COLORS = {"ok": GREEN, "warn": AMBER, "err": RED}


# ---------------------------------------------------------------------------
# Segédek
# ---------------------------------------------------------------------------


class LauncherError(Exception):
    """Felhasználónak megjeleníthető hiba."""


class TaskCancelled(Exception):
    """A felhasználó megszakította a műveletet."""


def parse_version(value: str) -> tuple[int, int, int]:
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", value or "")
    if not match:
        return (0, 0, 0)
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def port_open(port: int = PORT, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.45)
        return sock.connect_ex((host, port)) == 0


def shorten_path(path: Path, limit: int = 46) -> str:
    text = str(path)
    if len(text) <= limit:
        return text
    tail = path.name
    head_budget = max(8, limit - len(tail) - 3)
    head = text[:head_budget].rstrip("\\/ ")
    return f"{head}…\\{tail}"


def child_env() -> dict[str, str]:
    env = os.environ.copy()
    env["COREPACK_ENABLE_DOWNLOAD_PROMPT"] = "0"
    env["NO_COLOR"] = "1"
    env["FORCE_COLOR"] = "0"
    # A fejlesztői szerver az Andersen saját útvonalán szolgáljon ki.
    env["VITE_BASE"] = APP_BASE
    env.setdefault("PYTHONUTF8", "1")
    return env


@dataclass
class Config:
    repo_path: Path
    auto_open: bool = True

    @classmethod
    def load(cls) -> "Config":
        cfg = cls(repo_path=Path.home() / "Andersen")
        try:
            raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if raw.get("repo_path"):
                cfg.repo_path = Path(str(raw["repo_path"])).expanduser()
            cfg.auto_open = bool(raw.get("auto_open", True))
        except Exception:
            pass
        return cfg

    def save(self) -> None:
        try:
            CONFIG_FILE.write_text(
                json.dumps(
                    {"repo_path": str(self.repo_path), "auto_open": self.auto_open},
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Saját rajzolt gombok és apró felületi elemek
# ---------------------------------------------------------------------------


class Tooltip:
    """Késleltetett, sötét buborék a gombok magyarázatához."""

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tip: tk.Toplevel | None = None
        self.job: str | None = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event=None) -> None:
        self._cancel()
        self.job = self.widget.after(650, self._show)

    def _cancel(self) -> None:
        if self.job:
            try:
                self.widget.after_cancel(self.job)
            except Exception:
                pass
            self.job = None

    def _show(self) -> None:
        if self.tip is not None or not self.widget.winfo_exists():
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.configure(bg=BORDER)
        label = tk.Label(
            self.tip,
            text=self.text,
            bg=PANEL_2,
            fg=TEXT,
            font=("Segoe UI", 8),
            padx=10,
            pady=6,
            justify="left",
            wraplength=270,
        )
        label.pack(padx=1, pady=1)
        self.tip.update_idletasks()
        width = self.tip.winfo_width()
        x = min(max(8, x - width // 2), self.widget.winfo_screenwidth() - width - 8)
        self.tip.wm_geometry(f"+{x}+{y}")

    def _hide(self, _event=None) -> None:
        self._cancel()
        if self.tip is not None:
            try:
                self.tip.destroy()
            except Exception:
                pass
            self.tip = None


class PillButton(tk.Canvas):
    """Lekerekített, saját rajzolású gomb hover/press állapotokkal."""

    STYLES = {
        "primary": {
            "fill": GOLD,
            "hover": GOLD_BRIGHT,
            "press": "#C3A05B",
            "text": "#081020",
            "border": "",
            "hover_border": "",
            "shadow": "#6B5731",
        },
        "secondary": {
            "fill": PANEL_2,
            "hover": "#1C2E49",
            "press": "#0F1B2D",
            "text": TEXT,
            "border": BORDER,
            "hover_border": "#3A5678",
            "shadow": "",
        },
        "danger": {
            "fill": "#241722",
            "hover": "#33202E",
            "press": "#1B111A",
            "text": "#E8A0A0",
            "border": "#4A2B38",
            "hover_border": "#6B3B4D",
            "shadow": "",
        },
        "ghost": {
            "fill": "",
            "hover": "#17273E",
            "press": "#0F1B2D",
            "text": MUTED,
            "border": "",
            "hover_border": "",
            "shadow": "",
        },
    }

    def __init__(
        self,
        master: tk.Widget,
        text: str,
        command,
        width: int = 160,
        height: int = 40,
        style: str = "secondary",
        font: tuple | None = None,
        bg: str = PANEL,
        radius: int = 10,
        tooltip: str | None = None,
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            bg=bg,
            highlightthickness=0,
            bd=0,
            takefocus=1,
        )
        self._text = text
        self._command = command
        self._style = style
        self._font = font or ("Segoe UI", 10)
        self._radius = radius
        self._base_bg = bg
        self._enabled = True
        self._hover = False
        self._pressed = False
        self._width = width
        self._height = height
        self.configure(cursor="hand2")
        self.bind("<Configure>", self._on_configure)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<FocusIn>", lambda _e: self._draw())
        self.bind("<FocusOut>", lambda _e: self._draw())
        self.bind("<Return>", lambda _e: self._activate())
        self.bind("<space>", lambda _e: self._activate())
        if tooltip:
            Tooltip(self, tooltip)
        self._draw()

    # -- állapot ---------------------------------------------------------

    def set_text(self, text: str) -> None:
        if text != self._text:
            self._text = text
            self._draw()

    def set_enabled(self, enabled: bool) -> None:
        enabled = bool(enabled)
        if enabled != self._enabled:
            self._enabled = enabled
            self.configure(cursor="hand2" if enabled else "arrow")
            if not enabled:
                self._hover = False
                self._pressed = False
            self._draw()

    def _activate(self) -> None:
        if self._enabled and self._command:
            self._command()

    # -- események -------------------------------------------------------

    def _on_configure(self, _event) -> None:
        self._draw()

    def _on_enter(self, _event) -> None:
        if self._enabled:
            self._hover = True
            self._draw()

    def _on_leave(self, _event) -> None:
        self._hover = False
        self._pressed = False
        self._draw()

    def _on_press(self, _event) -> None:
        if self._enabled:
            self.focus_set()
            self._pressed = True
            self._draw()

    def _on_release(self, event) -> None:
        if not self._enabled:
            return
        was_pressed = self._pressed
        self._pressed = False
        self._draw()
        inside = 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height()
        if was_pressed and inside:
            self._activate()

    # -- rajzolás --------------------------------------------------------

    def _rounded(self, x1, y1, x2, y2, radius, **kwargs):
        radius = max(0, min(radius, (x2 - x1) // 2, (y2 - y1) // 2))
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self) -> None:
        if not self.winfo_exists():
            return
        style = self.STYLES.get(self._style, self.STYLES["secondary"])
        width = max(self._width, self.winfo_width())
        height = max(self._height, self.winfo_height())
        self.delete("all")

        if not self._enabled:
            fill = "#131F31"
            border = "#1C2C45"
            text_color = "#536A87"
        else:
            fill = style["press"] if self._pressed else (style["hover"] if self._hover else style["fill"])
            if not fill:
                fill = self._base_bg
            border = style["hover_border"] if self._hover else style["border"]
            text_color = style["text"]

        radius = min(self._radius, height // 2)
        shadow = style["shadow"] if self._enabled else ""
        if shadow and self._style == "primary":
            self._rounded(1, 3, width - 1, height - 1, radius, fill=shadow, outline="")
            self._rounded(0, 0, width - 1, height - 3, radius, fill=fill, outline="")
            text_y = (height - 3) / 2
        else:
            self._rounded(0, 0, width - 1, height - 1, radius, fill=fill, outline=border or fill)
            text_y = height / 2

        self.create_text(
            width / 2,
            text_y,
            text=self._text,
            fill=text_color,
            font=self._font,
        )

        if self.focus_get() is self:
            self._rounded(2, 2, width - 3, height - 4, max(0, radius - 1), fill="", outline=GOLD_DIM)


class PulseBar(tk.Canvas):
    """Vékony, futó fénycsík a folyamatban lévő műveletek jelzésére."""

    def __init__(self, master: tk.Widget, width: int = 110, height: int = 3, bg: str = BG_DEEP):
        super().__init__(master, width=width, height=height, bg=bg, highlightthickness=0, bd=0)
        self._active = False
        self._pos = 0.0
        self._job: str | None = None
        self.bind("<Configure>", lambda _e: self._draw())

    def set_active(self, active: bool) -> None:
        active = bool(active)
        if active == self._active:
            return
        self._active = active
        self._cancel()
        if active:
            self._pos = 0.0
            self._tick()
        else:
            self._draw()

    def _cancel(self) -> None:
        if self._job:
            try:
                self.after_cancel(self._job)
            except Exception:
                pass
            self._job = None

    def _tick(self) -> None:
        if not self._active or not self.winfo_exists():
            return
        self._pos = (self._pos + 0.035) % 1.4
        self._draw()
        self._job = self.after(30, self._tick)

    def _draw(self) -> None:
        if not self.winfo_exists():
            return
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1:
            return
        self.delete("all")
        if not self._active:
            return
        self.create_rectangle(0, max(0, height // 2), width, max(1, height // 2 + 1), fill=BORDER_SOFT, outline="")
        segment = max(26, int(width * 0.3))
        x = int((width + segment) * (self._pos / 1.4)) - segment
        left = max(0, x)
        right = min(width, x + segment)
        if right > left:
            self.create_rectangle(left, 0, right, height, fill=GOLD, outline="")


# ---------------------------------------------------------------------------
# Az alkalmazás
# ---------------------------------------------------------------------------


class AndersenLauncher:
    def __init__(self) -> None:
        self.config = Config.load()
        self.queue: queue.Queue = queue.Queue()
        self._closing = False
        self._env_checking = False
        self._env_announced = False
        self.busy = False
        self.server_state = "stopped"  # stopped | starting | running
        self.desktop_mode = False
        self.server_process: subprocess.Popen | None = None
        self.current_process: subprocess.Popen | None = None
        self.stop_requested = False
        self.browser_opened = False
        self.env_rows: dict[str, tuple[tk.Canvas, int, tk.Label]] = {}

        self._enable_dpi()
        self.root = tk.Tk()
        try:
            self.scale = max(1.0, min(2.0, self.root.winfo_fpixels("1i") / 96.0))
        except Exception:
            self.scale = 1.0

        self._setup_fonts()
        self._setup_window()
        self._build_ui()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.report_callback_exception = self._tk_exception
        self.root.after(80, self._drain_queue)

        self._welcome()
        self.check_environment(silent=True, update_status=True)

    # -- alapok ----------------------------------------------------------

    def _s(self, value: float) -> int:
        return int(round(value * self.scale))

    @staticmethod
    def _enable_dpi() -> None:
        if os.name != "nt":
            return
        try:
            import ctypes

            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    def _setup_fonts(self) -> None:
        try:
            families = set(tkfont.families(self.root))
        except Exception:
            families = set()
        self.ui_family = "Segoe UI" if "Segoe UI" in families else "Arial"
        self.serif_family = "Georgia" if "Georgia" in families else "Times New Roman"
        self.mono_family = "Consolas" if "Consolas" in families else "Courier New"

        self.f_wordmark = (self.serif_family, 24, "bold")
        self.f_card_title = (self.serif_family, 14)
        self.f_eyebrow = (self.ui_family, 8, "bold")
        self.f_body = (self.ui_family, 9)
        self.f_small = (self.ui_family, 8)
        self.f_tiny = (self.ui_family, 7, "bold")
        self.f_button = (self.ui_family, 9, "bold")
        self.f_button_main = (self.ui_family, 11, "bold")
        self.f_log = (self.mono_family, 9)
        self.f_status = (self.ui_family, 8)

    def _setup_window(self) -> None:
        root = self.root
        root.title("Andersen Launcher")
        root.configure(bg=BG)
        width = self._s(1040)
        height = self._s(740)
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        width = min(width, int(screen_w * 0.96))
        height = min(height, int(screen_h * 0.92))
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2 - self._s(8))
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(min(self._s(960), width), min(self._s(690), height))

        icon_ico = ASSETS_DIR / "andersen-icon.ico"
        if icon_ico.exists():
            try:
                root.iconbitmap(default=str(icon_ico))
            except Exception:
                pass

        self._emblem_photo = None
        if HAS_PIL and (ASSETS_DIR / "andersen-emblem.png").exists():
            try:
                image = Image.open(ASSETS_DIR / "andersen-emblem.png").convert("RGBA")
                size = self._s(54)
                image = image.resize((size, size), Image.LANCZOS)
                self._emblem_photo = ImageTk.PhotoImage(image)
                root.iconphoto(True, self._emblem_photo)
            except Exception:
                self._emblem_photo = None

        try:
            root.update_idletasks()
            self._enable_dark_titlebar()
        except Exception:
            pass

    def _enable_dark_titlebar(self) -> None:
        if os.name != "nt":
            return
        try:
            import ctypes

            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if not hwnd:
                hwnd = self.root.winfo_id()
            enabled = ctypes.c_int(1)
            for attribute in (20, 19):
                result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    attribute,
                    ctypes.byref(enabled),
                    ctypes.sizeof(enabled),
                )
                if result == 0:
                    break
        except Exception:
            pass

    # -- felület ---------------------------------------------------------

    def _card(self, parent: tk.Widget) -> tuple[tk.Frame, tk.Frame]:
        outer = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0,
        )
        inner = tk.Frame(outer, bg=PANEL)
        inner.pack(fill="both", expand=True, padx=self._s(16), pady=self._s(14))
        return outer, inner

    def _build_ui(self) -> None:
        root = self.root

        # Fejléc ---------------------------------------------------------
        header = tk.Frame(root, bg=BG, height=self._s(88))
        header.pack(fill="x", padx=self._s(24), pady=(self._s(14), 0))
        header.pack_propagate(False)

        if self._emblem_photo is not None:
            emblem = tk.Label(header, image=self._emblem_photo, bg=BG, bd=0)
            emblem.pack(side="left", padx=(0, self._s(14)))
        else:
            emblem = tk.Label(
                header,
                text="A",
                font=(self.serif_family, 32, "bold"),
                fg=GOLD,
                bg=BG,
                width=2,
            )
            emblem.pack(side="left", padx=(0, self._s(14)))

        brand = tk.Frame(header, bg=BG)
        brand.pack(side="left", fill="y")
        title_row = tk.Frame(brand, bg=BG)
        title_row.pack(anchor="w", pady=(self._s(9), 0))
        tk.Label(
            title_row,
            text="ANDERSEN",
            font=self.f_wordmark,
            fg=GOLD,
            bg=BG,
        ).pack(side="left")
        tk.Label(
            title_row,
            text="LAUNCHER",
            font=self.f_tiny,
            fg=GOLD,
            bg=PANEL_2,
            padx=self._s(8),
            pady=self._s(3),
        ).pack(side="left", padx=(self._s(10), 0), pady=(self._s(8), 0))
        tk.Label(
            brand,
            text="A TÖRTÉNET MŰHELYE",
            font=self.f_eyebrow,
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(self._s(1), 0))

        meta = tk.Frame(header, bg=BG)
        meta.pack(side="right", pady=(self._s(14), 0))
        tk.Label(
            meta,
            text="NYÍLT FORRÁSKÓD",
            font=self.f_tiny,
            fg=MUTED_DIM,
            bg=BG,
        ).pack(anchor="e")
        self.version_label = tk.Label(
            meta,
            text="v—",
            font=self.f_small,
            fg=GOLD,
            bg=PANEL_2,
            padx=self._s(9),
            pady=self._s(2),
        )
        self.version_label.pack(anchor="e", pady=(self._s(4), 0))

        separator = tk.Canvas(root, height=2, bg=BG, highlightthickness=0, bd=0)
        separator.pack(fill="x", padx=self._s(24), pady=(self._s(12), 0))

        def draw_separator(event) -> None:
            separator.delete("all")
            separator.create_line(0, 1, event.width, 1, fill=BORDER_SOFT)
            separator.create_line(0, 1, min(self._s(96), event.width), 1, fill=GOLD_DIM)

        separator.bind("<Configure>", draw_separator)

        # Lábléc (előbb foglaljuk le a helyét) ---------------------------
        footer = tk.Frame(root, bg=BG_DEEP, height=self._s(32))
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)

        self.status_dot = tk.Canvas(
            footer,
            width=self._s(9),
            height=self._s(9),
            bg=BG_DEEP,
            highlightthickness=0,
            bd=0,
        )
        self.status_dot.pack(side="left", padx=(self._s(24), self._s(8)))
        dot_size = self._s(9)
        self.status_dot_id = self.status_dot.create_oval(
            0, 0, dot_size, dot_size, fill=GREEN, outline=""
        )
        self.status_label = tk.Label(
            footer,
            text="Kész",
            font=self.f_status,
            fg=TEXT_SOFT,
            bg=BG_DEEP,
            anchor="w",
        )
        self.status_label.pack(side="left")

        self.pulse = PulseBar(
            footer,
            width=self._s(110),
            height=self._s(3),
            bg=BG_DEEP,
        )
        self.pulse.pack(side="right", padx=(self._s(12), self._s(20)))
        tk.Label(
            footer,
            text=f"Andersen Launcher {LAUNCHER_VERSION}",
            font=self.f_status,
            fg=MUTED_DIM,
            bg=BG_DEEP,
        ).pack(side="right")

        # Tartalom -------------------------------------------------------
        content = tk.Frame(root, bg=BG)
        content.pack(fill="both", expand=True, padx=self._s(24), pady=self._s(14))
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, minsize=self._s(352), weight=0)
        content.grid_columnconfigure(1, weight=1)

        left = tk.Frame(content, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, self._s(14)))
        left.grid_rowconfigure(0, weight=0)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)
        right = tk.Frame(content, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")

        # -- Indítás kártya ---------------------------------------------
        card_start, body = self._card(left)
        card_start.grid(row=0, column=0, sticky="ew", pady=(0, self._s(12)))

        tk.Label(
            body,
            text="MUNKATERÜLET",
            font=self.f_eyebrow,
            fg=GOLD_DIM,
            bg=PANEL,
        ).pack(anchor="w")
        tk.Label(
            body,
            text="Webes változat",
            font=self.f_card_title,
            fg=TEXT,
            bg=PANEL,
        ).pack(anchor="w", pady=(self._s(2), self._s(3)))
        tk.Label(
            body,
            text="A fejlesztői szerver a 3000-es porton indul, majd a böngészőben nyílik meg.",
            font=self.f_body,
            fg=MUTED,
            bg=PANEL,
            justify="left",
            wraplength=self._s(300),
        ).pack(anchor="w")

        self.btn_start = PillButton(
            body,
            text="INDÍTÁS",
            command=self.on_start,
            width=self._s(300),
            height=self._s(46),
            style="primary",
            font=self.f_button_main,
            bg=PANEL,
            radius=self._s(11),
            tooltip="Elindítja az Andersent, majd megnyitja a böngészőt.",
        )
        self.btn_start.pack(fill="x", pady=(self._s(12), self._s(7)))

        button_grid = tk.Frame(body, bg=PANEL)
        button_grid.pack(fill="x")
        button_grid.grid_columnconfigure(0, weight=1, uniform="button")
        button_grid.grid_columnconfigure(1, weight=1, uniform="button")

        self.btn_desktop = PillButton(
            button_grid,
            text="Asztali mód",
            command=self.on_desktop,
            width=self._s(142),
            height=self._s(36),
            style="secondary",
            font=self.f_button,
            bg=PANEL,
            radius=self._s(9),
            tooltip="Tauri asztali alkalmazás indítása. Az első indítás Rust-fordítás miatt hosszú lehet.",
        )
        self.btn_desktop.grid(row=0, column=0, sticky="ew", padx=(0, self._s(3)), pady=(0, self._s(5)))

        self.btn_update = PillButton(
            button_grid,
            text="Frissítés",
            command=self.on_update,
            width=self._s(142),
            height=self._s(36),
            style="secondary",
            font=self.f_button,
            bg=PANEL,
            radius=self._s(9),
            tooltip="Legújabb verzió letöltése (git pull), majd a függőségek frissítése.",
        )
        self.btn_update.grid(row=0, column=1, sticky="ew", padx=(self._s(3), 0), pady=(0, self._s(5)))

        self.btn_stop = PillButton(
            button_grid,
            text="Leállítás",
            command=self.on_stop,
            width=self._s(142),
            height=self._s(36),
            style="danger",
            font=self.f_button,
            bg=PANEL,
            radius=self._s(9),
            tooltip="A futó szerver vagy telepítés leállítása.",
        )
        self.btn_stop.grid(row=1, column=0, sticky="ew", padx=(0, self._s(3)))

        self.btn_folder = PillButton(
            button_grid,
            text="Mappa",
            command=self.open_folder,
            width=self._s(142),
            height=self._s(36),
            style="secondary",
            font=self.f_button,
            bg=PANEL,
            radius=self._s(9),
            tooltip="A forráskód mappájának megnyitása az Intézőben.",
        )
        self.btn_folder.grid(row=1, column=1, sticky="ew", padx=(self._s(3), 0))

        tk.Label(
            body,
            text="Az első indítás letölti a forrást és a függőségeket — ez néhány percig tarthat.",
            font=self.f_small,
            fg=MUTED_DIM,
            bg=PANEL,
            justify="left",
            wraplength=self._s(300),
        ).pack(anchor="w", pady=(self._s(7), 0))

        # -- Környezet kártya -------------------------------------------
        card_env, env_body = self._card(left)
        card_env.grid(row=1, column=0, sticky="nsew")

        env_head = tk.Frame(env_body, bg=PANEL)
        env_head.pack(fill="x")
        tk.Label(
            env_head,
            text="KÖRNYEZET",
            font=self.f_eyebrow,
            fg=GOLD_DIM,
            bg=PANEL,
        ).pack(side="left", pady=(self._s(4), 0))
        self.btn_refresh = PillButton(
            env_head,
            text="Újraellenőrzés",
            command=lambda: self.check_environment(silent=False, update_status=True),
            width=self._s(94),
            height=self._s(24),
            style="ghost",
            font=self.f_small,
            bg=PANEL,
            radius=self._s(7),
            tooltip="Git, Node.js, pnpm, a forrás és a port állapotának ellenőrzése.",
        )
        self.btn_refresh.pack(side="right")

        rows = tk.Frame(env_body, bg=PANEL)
        rows.pack(fill="x", pady=(self._s(6), 0))
        for key in ("git", "node", "pnpm", "repo", "port"):
            self._env_row(rows, key, ENV_LABELS[key])

        tk.Frame(env_body, bg=BORDER_SOFT, height=1).pack(fill="x", pady=self._s(8))

        path_head = tk.Frame(env_body, bg=PANEL)
        path_head.pack(fill="x")
        tk.Label(
            path_head,
            text="FORRÁSMAPPA",
            font=self.f_eyebrow,
            fg=GOLD_DIM,
            bg=PANEL,
        ).pack(side="left", pady=(self._s(3), 0))
        self.btn_change = PillButton(
            path_head,
            text="Módosítás",
            command=self.choose_repo,
            width=self._s(76),
            height=self._s(24),
            style="ghost",
            font=self.f_small,
            bg=PANEL,
            radius=self._s(7),
            tooltip="Másik mappa kiválasztása az Andersen forráskódjához.",
        )
        self.btn_change.pack(side="right")

        self.path_label = tk.Label(
            env_body,
            text=shorten_path(self.config.repo_path),
            font=self.f_small,
            fg=TEXT_SOFT,
            bg=PANEL,
            anchor="w",
            justify="left",
            wraplength=self._s(300),
        )
        self.path_label.pack(fill="x", pady=(self._s(2), 0))

        # -- Napló kártya -----------------------------------------------
        card_log, log_body = self._card(right)
        card_log.pack(fill="both", expand=True)

        log_head = tk.Frame(log_body, bg=PANEL)
        log_head.pack(fill="x")
        tk.Label(
            log_head,
            text="NAPLÓ",
            font=self.f_eyebrow,
            fg=GOLD_DIM,
            bg=PANEL,
        ).pack(side="left", pady=(self._s(4), 0))

        self.btn_clear = PillButton(
            log_head,
            text="Törlés",
            command=self.clear_log,
            width=self._s(58),
            height=self._s(24),
            style="ghost",
            font=self.f_small,
            bg=PANEL,
            radius=self._s(7),
            tooltip="A napló tartalmának törlése.",
        )
        self.btn_clear.pack(side="right")
        self.btn_save = PillButton(
            log_head,
            text="Mentés",
            command=self.save_log,
            width=self._s(58),
            height=self._s(24),
            style="ghost",
            font=self.f_small,
            bg=PANEL,
            radius=self._s(7),
            tooltip="A napló mentése szövegfájlba.",
        )
        self.btn_save.pack(side="right", padx=(0, self._s(4)))

        log_frame = tk.Frame(
            log_body,
            bg=BG_DEEP,
            highlightbackground=BORDER_SOFT,
            highlightthickness=1,
            bd=0,
        )
        log_frame.pack(fill="both", expand=True, pady=(self._s(8), 0))

        self._setup_scrollbar_style()
        self.log_text = tk.Text(
            log_frame,
            bg=BG_DEEP,
            fg=TEXT,
            insertbackground=GOLD,
            relief="flat",
            bd=0,
            highlightthickness=0,
            wrap="word",
            font=self.f_log,
            padx=self._s(12),
            pady=self._s(9),
            spacing1=1,
            spacing3=1,
            state="disabled",
            selectbackground=PANEL_3,
            selectforeground=TEXT,
        )
        scrollbar = ttk.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.log_text.yview,
            style="Andersen.Vertical.TScrollbar",
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y", padx=(0, self._s(3)), pady=self._s(3))

        self.log_text.tag_configure("time", foreground="#5A6F8C")
        self.log_text.tag_configure("info", foreground="#DCE5F0")
        self.log_text.tag_configure("output", foreground="#AEBFD3")
        self.log_text.tag_configure("cmd", foreground=GOLD_DIM)
        self.log_text.tag_configure("ok", foreground=GREEN)
        self.log_text.tag_configure("warn", foreground=AMBER)
        self.log_text.tag_configure("err", foreground=RED)
        self.log_text.tag_configure("dim", foreground=MUTED_DIM)

        self._update_buttons()
        self._update_pulse()

    def _setup_scrollbar_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Andersen.Vertical.TScrollbar",
            background=PANEL_2,
            troughcolor=BG_DEEP,
            bordercolor=BG_DEEP,
            darkcolor=PANEL_2,
            lightcolor=PANEL_2,
            arrowcolor=MUTED,
            width=self._s(9),
        )
        style.map(
            "Andersen.Vertical.TScrollbar",
            background=[("active", BORDER)],
            arrowcolor=[("active", GOLD)],
        )

    def _env_row(self, parent: tk.Widget, key: str, label: str) -> None:
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=self._s(1))
        size = self._s(8)
        dot = tk.Canvas(
            row,
            width=size,
            height=size,
            bg=PANEL,
            highlightthickness=0,
            bd=0,
        )
        dot.pack(side="left", padx=(0, self._s(7)))
        oval = dot.create_oval(0, 0, size, size, fill=MUTED_DIM, outline="")
        tk.Label(
            row,
            text=label,
            font=self.f_body,
            fg=MUTED,
            bg=PANEL,
            anchor="w",
        ).pack(side="left")
        value = tk.Label(
            row,
            text="…",
            font=self.f_body,
            fg=MUTED,
            bg=PANEL,
            anchor="e",
        )
        value.pack(side="right")
        self.env_rows[key] = (dot, oval, value)

    # -- napló és üzenetek ----------------------------------------------

    def _welcome(self) -> None:
        self.log(f"Andersen Launcher {LAUNCHER_VERSION} — A történet műhelye.", "ok")
        self.log(f"Forrás: {REPO_WEB}", "dim")
        self.log(
            "Kattints az INDÍTÁS gombra. Első alkalommal a launcher letölti a forráskódot és a függőségeket.",
            "info",
        )

    def log(self, text: str, tag: str = "info") -> None:
        self.queue.put(("log", (text, tag)))

    def _drain_queue(self) -> None:
        if self._closing:
            return
        try:
            for _ in range(300):
                kind, payload = self.queue.get_nowait()
                try:
                    self._handle_event(kind, payload)
                except Exception:
                    traceback.print_exc()
        except queue.Empty:
            pass
        if not self._closing:
            self.root.after(60, self._drain_queue)

    def _handle_event(self, kind: str, payload) -> None:
        if kind == "log":
            text, tag = payload
            self._append_log(text, tag)
        elif kind == "status":
            text, color = payload
            self.set_status(text, color)
        elif kind == "busy":
            self._set_busy(bool(payload))
        elif kind == "env":
            self._apply_env(payload)
        elif kind == "server_ready":
            self._on_server_ready(str(payload))
        elif kind == "desktop_running":
            self._on_desktop_running()
        elif kind == "server_exited":
            self._on_server_exited(int(payload))
        elif kind == "task_done":
            self._on_task_done(str(payload))
        elif kind == "task_failed":
            self._on_task_failed(str(payload))
        elif kind == "start_failed":
            self._on_start_failed(str(payload))
        elif kind == "aborted":
            self._on_aborted()
        elif kind == "refresh_env":
            self.check_environment(silent=True, update_status=bool(payload))
        elif kind == "version":
            self.version_label.configure(text=f"v{payload}")

    def _append_log(self, text: str, tag: str = "info") -> None:
        if not self.log_text.winfo_exists():
            return
        self.log_text.configure(state="normal")
        stamp = time.strftime("%H:%M:%S")
        for line in text.splitlines() or [""]:
            self.log_text.insert("end", f"{stamp}  ", "time")
            self.log_text.insert("end", line + "\n", tag)
        try:
            line_count = int(self.log_text.index("end-1c").split(".")[0])
            if line_count > 4000:
                self.log_text.delete("1.0", "1200.0")
        except Exception:
            pass
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    @staticmethod
    def _output_tag(line: str) -> str:
        low = line.lower()
        if re.search(r"\b(error|failed|fatal|cannot|eacces|enotfound|exception)\b", low):
            return "err"
        if re.search(r"\bwarn(ing)?\b", low):
            return "warn"
        return "output"

    def clear_log(self) -> None:
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self.log("Napló törölve.", "dim")

    def save_log(self) -> None:
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Napló mentése",
            defaultextension=".txt",
            initialfile=f"andersen-launcher-{time.strftime('%Y%m%d-%H%M')}.txt",
            filetypes=[("Szövegfájl", "*.txt"), ("Minden fájl", "*.*")],
        )
        if not path:
            return
        try:
            content = self.log_text.get("1.0", "end-1c")
            Path(path).write_text(content + "\n", encoding="utf-8")
            self.log(f"Napló mentve: {path}", "ok")
        except Exception as exc:
            messagebox.showerror("Mentési hiba", str(exc), parent=self.root)

    # -- állapot ---------------------------------------------------------

    def set_status(self, text: str, color: str = GREEN) -> None:
        self.status_label.configure(text=text)
        self.status_dot.itemconfig(self.status_dot_id, fill=color)

    def _update_buttons(self) -> None:
        idle = not self.busy
        stopped = self.server_state == "stopped"
        starting = self.server_state == "starting"
        running = self.server_state == "running"

        if running and not self.desktop_mode:
            start_text = "MEGNYITÁS"
            start_enabled = True
        elif starting:
            start_text = "INDUL…"
            start_enabled = False
        elif running and self.desktop_mode:
            start_text = "ASZTALI MÓD"
            start_enabled = False
        else:
            start_text = "INDÍTÁS"
            start_enabled = idle

        self.btn_start.set_text(start_text)
        self.btn_start.set_enabled(start_enabled)
        self.btn_desktop.set_enabled(idle and stopped)
        self.btn_update.set_enabled(idle and stopped)
        self.btn_stop.set_enabled(self.busy or starting or running)
        self.btn_folder.set_enabled(True)
        self.btn_change.set_enabled(idle and stopped)
        self.btn_refresh.set_enabled(idle and not starting)

    def _update_pulse(self) -> None:
        self.pulse.set_active(self.busy or self.server_state == "starting")

    def _set_busy(self, busy: bool) -> None:
        self.busy = bool(busy)
        self._update_buttons()
        self._update_pulse()

    # -- környezetellenőrzés --------------------------------------------

    def check_environment(self, silent: bool = False, update_status: bool = True) -> None:
        if self._env_checking:
            return
        self._env_checking = True
        if update_status and not self.busy and self.server_state == "stopped":
            self.set_status("Környezet ellenőrzése…", GOLD)
        threading.Thread(
            target=self._env_worker,
            args=(silent, update_status),
            daemon=True,
        ).start()

    def _env_worker(self, silent: bool, update_status: bool) -> None:
        data: dict[str, dict | str] = {}
        repo = self.config.repo_path
        try:
            git = shutil.which("git")
            if git:
                code, out = self._capture([git, "--version"], timeout=15)
                match = re.search(r"\d+\.\d+\.\d+", out)
                version = match.group(0) if match else out.strip()
                data["git"] = {
                    "text": version or "elérhető",
                    "level": "ok" if code == 0 else "err",
                }
            else:
                data["git"] = {"text": "hiányzik", "level": "err"}

            node = shutil.which("node")
            if node:
                code, out = self._capture([node, "--version"], timeout=15)
                version = out.strip()
                if code == 0:
                    ok = parse_version(version) >= REQUIRED_NODE
                    data["node"] = {
                        "text": version if ok else f"{version} (22.19+ kell)",
                        "level": "ok" if ok else "err",
                    }
                else:
                    data["node"] = {"text": "hiba", "level": "err"}
            else:
                data["node"] = {"text": "hiányzik", "level": "err"}

            corepack = shutil.which("corepack")
            pnpm = shutil.which("pnpm")
            repo_is_dir = repo.is_dir()
            repo_has_pkg = repo_is_dir and (repo / "package.json").exists()
            deps_installed = repo_is_dir and (repo / "node_modules" / ".modules.yaml").exists()

            if corepack:
                if deps_installed:
                    code, out = self._capture(
                        [corepack, "pnpm", "--version"],
                        cwd=repo,
                        timeout=120,
                    )
                    version = out.strip().splitlines()[-1] if out.strip() else ""
                    if code == 0 and version:
                        data["pnpm"] = {
                            "text": version,
                            "level": "ok" if version == REQUIRED_PNPM else "warn",
                        }
                    else:
                        data["pnpm"] = {"text": "corepack hiba", "level": "err"}
                else:
                    data["pnpm"] = {
                        "text": f"{REQUIRED_PNPM} (corepack)",
                        "level": "ok",
                    }
            elif pnpm:
                code, out = self._capture([pnpm, "--version"], timeout=20)
                version = out.strip()
                data["pnpm"] = {
                    "text": version or "elérhető",
                    "level": "ok" if version == REQUIRED_PNPM else "warn",
                }
            else:
                data["pnpm"] = {"text": "hiányzik", "level": "err"}

            has_git = repo_is_dir and (repo / ".git").exists()
            if repo_has_pkg and has_git:
                data["repo"] = {"text": "rendben", "level": "ok"}
            elif repo_has_pkg:
                data["repo"] = {"text": "git nélkül", "level": "warn"}
            elif repo.is_file() or (repo_is_dir and any(repo.iterdir())):
                data["repo"] = {"text": "nem Andersen-mappa", "level": "err"}
            else:
                data["repo"] = {"text": "letöltésre vár", "level": "warn"}

            occupied = port_open(PORT)
            data["port"] = {
                "text": "foglalt" if occupied else "szabad",
                "level": "warn" if occupied else "ok",
            }

            if repo_has_pkg:
                try:
                    package = json.loads((repo / "package.json").read_text(encoding="utf-8"))
                    if package.get("version"):
                        data["version"] = str(package["version"])
                except Exception:
                    pass
        finally:
            self._env_checking = False
            self.queue.put(("env", (data, update_status)))

    def _apply_env(self, payload) -> None:
        data, update_status = payload
        for key, (dot, oval, value) in self.env_rows.items():
            item = data.get(key)
            if not isinstance(item, dict):
                continue
            level = str(item.get("level", "ok"))
            color = LEVEL_COLORS.get(level, MUTED)
            dot.itemconfig(oval, fill=color)
            value.configure(text=str(item.get("text", "—")), fg=TEXT_SOFT if level == "ok" else color)

        if data.get("version"):
            self.version_label.configure(text=f"v{data['version']}")
        self.path_label.configure(text=shorten_path(self.config.repo_path))

        if self.server_state in ("starting", "running") and not self.desktop_mode:
            self._set_env_row("port", "fut", GREEN)

        problems = [
            (ENV_LABELS.get(key, key), item)
            for key, item in data.items()
            if isinstance(item, dict) and item.get("level") == "err"
        ]
        if problems:
            for label, item in problems:
                self.log(f"{label}: {item.get('text', '')}", "warn")
        elif not self._env_announced:
            self.log("Minden előfeltétel rendben.", "dim")
        self._env_announced = True

        if update_status and not self.busy and self.server_state == "stopped":
            if problems:
                self.set_status("Hiányos környezet", AMBER)
            else:
                self.set_status("Kész", GREEN)

    def _set_env_row(self, key: str, text: str, color: str) -> None:
        row = self.env_rows.get(key)
        if not row:
            return
        dot, oval, value = row
        dot.itemconfig(oval, fill=color)
        value.configure(text=text, fg=TEXT_SOFT if color == GREEN else color)

    def _read_version(self) -> str | None:
        try:
            package = json.loads(
                (self.config.repo_path / "package.json").read_text(encoding="utf-8")
            )
            version = package.get("version")
            return str(version) if version else None
        except Exception:
            return None

    # -- folyamatkezelés -------------------------------------------------

    def _capture(self, cmd: list[str], cwd: Path | None = None, timeout: int = 20):
        try:
            result = subprocess.run(
                cmd,
                cwd=str(cwd) if cwd else None,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=child_env(),
                creationflags=CREATE_NO_WINDOW,
            )
            out = (result.stdout or "").strip()
            if not out:
                out = (result.stderr or "").strip()
            return result.returncode, out
        except FileNotFoundError:
            return -1, "nem található"
        except subprocess.TimeoutExpired:
            return -1, "időtúllépés"
        except Exception as exc:
            return -1, str(exc)

    def _popen(self, cmd: list[str], cwd: Path) -> subprocess.Popen:
        display = " ".join(f'"{part}"' if " " in str(part) else str(part) for part in cmd)
        self.log(f"$ {display}", "cmd")
        return subprocess.Popen(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=child_env(),
            creationflags=CREATE_NO_WINDOW,
        )

    def _pump(self, proc: subprocess.Popen) -> int:
        try:
            if proc.stdout is not None:
                for raw in proc.stdout:
                    line = ANSI_RE.sub("", raw).replace("\r", "").rstrip()
                    if line:
                        self.log(line, self._output_tag(line))
        finally:
            try:
                code = proc.wait()
            except Exception:
                code = -1
        return code

    def _run(self, cmd: list[str], cwd: Path, label: str) -> None:
        proc = self._popen(cmd, cwd)
        self.current_process = proc
        try:
            code = self._pump(proc)
        finally:
            self.current_process = None
        if self.stop_requested:
            raise TaskCancelled()
        if code != 0:
            raise LauncherError(
                f"{label} sikertelen (kilépési kód: {code}). A részletek a naplóban."
            )

    def _pnpm_cmd(self) -> list[str]:
        corepack = shutil.which("corepack")
        if corepack:
            return [corepack, "pnpm"]
        pnpm = shutil.which("pnpm")
        if pnpm:
            return [pnpm]
        raise LauncherError(
            "A pnpm nem érhető el.\n\n"
            "Telepítsd a Node.js 22.19-es vagy újabb verzióját (a Corepack része), "
            "vagy futtasd: corepack enable"
        )

    # -- előkészítés -----------------------------------------------------

    def _ensure_toolchain(self) -> None:
        node = shutil.which("node")
        if not node:
            raise LauncherError(
                "A Node.js nem található.\n\n"
                "Telepítsd a Node.js 22.19-es vagy újabb verzióját: https://nodejs.org"
            )
        code, out = self._capture([node, "--version"], timeout=20)
        if code != 0:
            raise LauncherError(f"A Node.js nem indítható el: {out}")
        if parse_version(out) < REQUIRED_NODE:
            raise LauncherError(
                f"A Node.js verziója túl régi ({out}).\n\n"
                "Az Andersenhez legalább 22.19.0 szükséges: https://nodejs.org"
            )
        self._pnpm_cmd()

    def _ensure_repo(self) -> None:
        repo = self.config.repo_path
        package_file = repo / "package.json"

        if repo.exists() and repo.is_file():
            raise LauncherError(f"A forrásmappa helyén fájl található:\n{repo}")

        if (repo / ".git").exists() and package_file.exists():
            self.log(f"Forrás: {repo}", "dim")
            return

        if repo.exists() and any(repo.iterdir()):
            if package_file.exists():
                self.log(
                    "A mappa nem Git-repo, de Andersen-forrást tartalmaz. "
                    "A frissítés nem lesz elérhető.",
                    "warn",
                )
                return
            raise LauncherError(
                "A megadott mappa nem üres, és nem Andersen-forrás:\n"
                f"{repo}\n\n"
                "Válassz másik mappát a „Módosítás” gombbal."
            )

        git = shutil.which("git")
        if not git:
            raise LauncherError(
                "A Git nem található, így a forráskód nem tölthető le.\n\n"
                "Telepítsd a Git for Windowst: https://git-scm.com/download/win"
            )

        repo.parent.mkdir(parents=True, exist_ok=True)
        self.log(f"Andersen letöltése ide: {repo}", "info")
        self.log("Az első letöltés néhány percig tarthat (kb. 50 MB).", "dim")
        self._run(
            [git, "clone", "--depth", "1", "--progress", REPO_URL, str(repo)],
            repo.parent,
            "git clone",
        )
        if not package_file.exists():
            raise LauncherError(
                "A letöltés befejeződött, de a package.json nem található. "
                "Ellenőrizd a naplót."
            )
        self.log("Forrás letöltve.", "ok")
        version = self._read_version()
        if version:
            self.queue.put(("version", version))

    def _ensure_agents_marker(self) -> None:
        """A publikus tárolóból hiányzó AGENTS.md pótlása a predev szkripthez."""
        agents = self.config.repo_path / "AGENTS.md"
        if agents.exists():
            return
        try:
            agents.write_text(
                "# Andersen\n\n"
                f"{AGENTS_MARKER}\n\n"
                "**Version:** `0.0.0`\n",
                encoding="utf-8",
            )
            self.log(
                "A tárolóból hiányzó AGENTS.md pótolva (a fejlesztői szerver előfeltétele).",
                "warn",
            )
        except OSError as exc:
            self.log(f"Az AGENTS.md nem hozható létre: {exc}", "warn")

    @staticmethod
    def _is_generated_path(path: str) -> bool:
        normalized = path.replace("\\", "/")
        return normalized == "public/locales" or normalized.startswith("public/locales/")

    def _drop_generated_agents(self, repo: Path) -> None:
        """Frissítés előtt eltávolítja a launcher által készített helyőrzőt."""
        agents = repo / "AGENTS.md"
        try:
            if agents.is_file() and AGENTS_MARKER in agents.read_text(
                encoding="utf-8", errors="ignore"
            ):
                agents.unlink()
        except OSError:
            pass

    def _ensure_deps(self) -> None:
        repo = self.config.repo_path
        self._ensure_agents_marker()
        marker = repo / "node_modules" / ".modules.yaml"
        if marker.exists():
            self.log("Függőségek: rendben.", "dim")
            return

        cmd = self._pnpm_cmd()
        self.log("Függőségek telepítése — pnpm install…", "info")
        self.log("Ez az első alkalommal több percig is eltarthat.", "dim")
        self._run(cmd + ["install"], repo, "pnpm install")
        self.log("Függőségek telepítve.", "ok")

    def _prepare(self) -> None:
        self.log("Előkészítés…", "dim")
        self._ensure_toolchain()
        if self.stop_requested:
            raise TaskCancelled()
        self._ensure_repo()
        if self.stop_requested:
            raise TaskCancelled()
        self._ensure_deps()
        if self.stop_requested:
            raise TaskCancelled()
        version = self._read_version()
        if version:
            self.queue.put(("version", version))
        self.queue.put(("refresh_env", False))

    # -- indítás ---------------------------------------------------------

    def on_start(self) -> None:
        if self.server_state == "running" and not self.desktop_mode:
            self.open_app()
            return
        if self.busy or self.server_state != "stopped":
            return
        if port_open(PORT):
            if messagebox.askyesno(
                "Andersen",
                f"A {PORT}-es porton már fut egy folyamat.\n\n"
                "Megnyitod a böngészőben?",
                parent=self.root,
            ):
                self.open_app()
            return

        self.stop_requested = False
        self.browser_opened = False
        self.server_state = "starting"
        self.desktop_mode = False
        self._set_busy(True)
        self.set_status("Előkészítés…", GOLD)
        threading.Thread(target=self._web_worker, daemon=True).start()

    def _web_worker(self) -> None:
        try:
            self._prepare()
            if self.stop_requested:
                raise TaskCancelled()
            cmd = self._pnpm_cmd()
            self.log("Fejlesztői szerver indítása…", "info")
            proc = self._popen(cmd + ["run", "dev"], self.config.repo_path)
            self.server_process = proc
            self.queue.put(("busy", False))
            self.queue.put(("status", ("A szerver indul…", GOLD)))
            threading.Thread(
                target=self._watch_server,
                args=(proc,),
                daemon=True,
            ).start()
            code = self._pump(proc)
            self.queue.put(("server_exited", code))
        except TaskCancelled:
            self.queue.put(("aborted", None))
        except LauncherError as exc:
            self.queue.put(("start_failed", str(exc)))
        except Exception as exc:
            self.queue.put(("start_failed", f"Váratlan hiba: {exc}"))

    def _watch_server(self, proc: subprocess.Popen) -> None:
        deadline = time.time() + 420
        while time.time() < deadline:
            if self.stop_requested or proc.poll() is not None:
                return
            if port_open(PORT):
                self.queue.put(("server_ready", APP_URL))
                return
            time.sleep(0.5)
        if proc.poll() is None:
            self.queue.put(
                (
                    "log",
                    (
                        "A szerver 7 perc alatt nem jelzett a 3000-es porton. "
                        "Nézd meg a naplót, vagy állítsd le a folyamatot.",
                        "warn",
                    ),
                )
            )

    def on_desktop(self) -> None:
        if self.busy or self.server_state != "stopped":
            return
        if port_open(PORT):
            messagebox.showwarning(
                "Asztali mód",
                f"A {PORT}-es port már foglalt. Állítsd le a futó szervert, "
                "majd indítsd újra az asztali módot.",
                parent=self.root,
            )
            return
        if not messagebox.askyesno(
            "Asztali mód",
            "A Tauri asztali alkalmazás indítása Rust-fordítást igényel.\n"
            "Az első indítás több percig is eltarthat.\n\n"
            "Indítod?",
            parent=self.root,
        ):
            return

        self.stop_requested = False
        self.server_state = "starting"
        self.desktop_mode = True
        self._set_busy(True)
        self.set_status("Asztali mód előkészítése…", GOLD)
        threading.Thread(target=self._desktop_worker, daemon=True).start()

    def _desktop_worker(self) -> None:
        try:
            self._prepare()
            if self.stop_requested:
                raise TaskCancelled()
            cmd = self._pnpm_cmd()
            self.log("Asztali alkalmazás indítása (tauri dev)…", "info")
            self.log("Az első Rust-fordítás akár 5–15 percig is eltarthat.", "dim")
            proc = self._popen(cmd + ["run", "tauri:dev"], self.config.repo_path)
            self.server_process = proc
            self.queue.put(("busy", False))
            self.queue.put(("desktop_running", None))
            code = self._pump(proc)
            self.queue.put(("server_exited", code))
        except TaskCancelled:
            self.queue.put(("aborted", None))
        except LauncherError as exc:
            self.queue.put(("start_failed", str(exc)))
        except Exception as exc:
            self.queue.put(("start_failed", f"Váratlan hiba: {exc}"))

    # -- frissítés -------------------------------------------------------

    def on_update(self) -> None:
        if self.busy or self.server_state != "stopped":
            return
        if not messagebox.askyesno(
            "Frissítés",
            "Letölti a legújabb változatot a GitHubról, majd frissíti a "
            "függőségeket.\n\nA helyi módosítások nem lesznek felülírva.",
            parent=self.root,
        ):
            return

        self.stop_requested = False
        self._set_busy(True)
        self.set_status("Frissítés…", GOLD)
        threading.Thread(target=self._update_worker, daemon=True).start()

    def _update_worker(self) -> None:
        try:
            self._ensure_toolchain()
            if self.stop_requested:
                raise TaskCancelled()
            self._ensure_repo()
            if self.stop_requested:
                raise TaskCancelled()

            repo = self.config.repo_path
            git = shutil.which("git")
            if not git:
                raise LauncherError("A Git nem található, a frissítés nem lehetséges.")
            code, out = self._capture(
                [git, "status", "--porcelain", "--untracked-files=no"],
                cwd=repo,
                timeout=30,
            )
            if code != 0:
                raise LauncherError(f"A Git állapot nem olvasható: {out}")
            real_changes = []
            for line in out.splitlines():
                if not line.strip():
                    continue
                parts = line.strip().split(maxsplit=1)
                path = parts[1].strip().strip('"') if len(parts) > 1 else ""
                if not self._is_generated_path(path):
                    real_changes.append(line)
            if real_changes:
                raise LauncherError(
                    "A forrásmappában helyi módosítások vannak.\n\n"
                    "A frissítés biztonsági okból kimaradt. Commitold vagy "
                    "állítsd vissza a módosításokat, majd próbáld újra."
                )
            if out.strip():
                self.log(
                    "Generált nyelvi fájlok visszaállítása a frissítés előtt…", "dim"
                )
                self._run([git, "checkout", "--", "public/locales"], repo, "git checkout")

            self._drop_generated_agents(repo)
            self.log("Legújabb változat letöltése…", "info")
            self._run([git, "pull", "--ff-only"], repo, "git pull")

            self.log("Függőségek frissítése…", "info")
            cmd = self._pnpm_cmd()
            self._run(cmd + ["install"], repo, "pnpm install")

            version = self._read_version()
            if version:
                self.queue.put(("version", version))
            self.queue.put(("task_done", "Frissítve"))
            self.queue.put(("refresh_env", False))
        except TaskCancelled:
            self.queue.put(("aborted", None))
        except LauncherError as exc:
            self.queue.put(("task_failed", str(exc)))
        except Exception as exc:
            self.queue.put(("task_failed", f"Váratlan hiba: {exc}"))

    # -- leállítás -------------------------------------------------------

    def on_stop(self) -> None:
        if not (self.busy or self.server_state in ("starting", "running")):
            return
        self.stop_requested = True
        processes: list[subprocess.Popen] = []
        for proc in (self.current_process, self.server_process):
            if proc is not None and proc.poll() is None and proc not in processes:
                processes.append(proc)

        if not processes:
            if self.server_state == "starting" and not self.busy:
                self.server_state = "stopped"
                self._update_buttons()
                self._update_pulse()
            self.set_status("Leállítás…", AMBER)
            return

        self.log("Folyamat leállítása…", "warn")
        self.set_status("Leállítás…", AMBER)
        for proc in processes:
            self._kill_tree(proc)

    def _kill_tree(self, proc: subprocess.Popen) -> None:
        try:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    creationflags=CREATE_NO_WINDOW,
                )
            else:
                proc.terminate()
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    # -- eseménykezelők --------------------------------------------------

    def _on_server_ready(self, url: str) -> None:
        if self.server_state != "starting":
            return
        self.server_state = "running"
        self.desktop_mode = False
        self._set_busy(False)
        self.set_status(f"Fut — {url}", GREEN)
        self.log(f"Az Andersen fut: {url}", "ok")
        self._update_buttons()
        self._update_pulse()
        if self.config.auto_open and not self.browser_opened:
            self.browser_opened = True
            self.open_app()
        self.check_environment(silent=True, update_status=False)

    def _on_desktop_running(self) -> None:
        self.server_state = "running"
        self.desktop_mode = True
        self._set_busy(False)
        self.set_status("Asztali mód fut", GREEN)
        self.log("Az asztali alkalmazás elindult.", "ok")
        self._update_buttons()
        self._update_pulse()
        self.check_environment(silent=True, update_status=False)

    def _on_server_exited(self, code: int) -> None:
        self.server_process = None
        self.desktop_mode = False
        self.server_state = "stopped"
        self._set_busy(False)
        stopped_by_user = self.stop_requested
        self.stop_requested = False

        if stopped_by_user:
            self.set_status("Leállítva", MUTED)
            self.log("A folyamat leállt.", "info")
        elif code == 0:
            self.set_status("Leállt", MUTED)
            self.log("A folyamat kilépett.", "info")
        else:
            self.set_status("Hiba történt – nézd meg a naplót", RED)
            self.log(
                f"A folyamat váratlanul leállt (kilépési kód: {code}).",
                "err",
            )
        self._update_buttons()
        self._update_pulse()
        self.check_environment(silent=True, update_status=False)

    def _on_task_done(self, message: str) -> None:
        self._set_busy(False)
        self.set_status(message, GREEN)
        self.log(message + ".", "ok")
        self._update_pulse()

    def _on_task_failed(self, message: str) -> None:
        self._set_busy(False)
        self.set_status("Hiba", RED)
        self.log(message, "err")
        messagebox.showerror("Andersen Launcher", message, parent=self.root)

    def _on_start_failed(self, message: str) -> None:
        self.server_state = "stopped"
        self.desktop_mode = False
        self.stop_requested = False
        self._set_busy(False)
        self.set_status("Hiba", RED)
        self.log(message, "err")
        messagebox.showerror("Indítási hiba", message, parent=self.root)

    def _on_aborted(self) -> None:
        self.server_state = "stopped"
        self.desktop_mode = False
        self.stop_requested = False
        self._set_busy(False)
        self.set_status("Megszakítva", AMBER)
        self.log("A művelet megszakítva.", "warn")
        self._update_pulse()

    # -- egyéb műveletek -------------------------------------------------

    def open_app(self) -> None:
        webbrowser.open(APP_URL)
        self.log(f"Böngésző megnyitása: {APP_URL}", "dim")

    def open_folder(self) -> None:
        repo = self.config.repo_path
        if not repo.exists():
            messagebox.showinfo(
                "Andersen Launcher",
                "A forrásmappa még nem létezik. Indítsd el az Andersent, "
                "vagy válassz másik mappát.",
                parent=self.root,
            )
            return
        try:
            if os.name == "nt":
                os.startfile(str(repo))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(repo)])
        except Exception as exc:
            messagebox.showerror("Andersen Launcher", str(exc), parent=self.root)

    def choose_repo(self) -> None:
        if self.busy or self.server_state != "stopped":
            return
        chosen = filedialog.askdirectory(
            parent=self.root,
            title="Válaszd ki az Andersen mappáját",
            initialdir=str(self.config.repo_path.parent),
            mustexist=False,
        )
        if not chosen:
            return
        path = Path(chosen)
        if path.is_file():
            messagebox.showerror(
                "Andersen Launcher",
                "A kiválasztott útvonal fájl, nem mappa.",
                parent=self.root,
            )
            return
        if path.exists() and any(path.iterdir()):
            package_file = path / "package.json"
            if not package_file.exists():
                messagebox.showerror(
                    "Andersen Launcher",
                    "A kiválasztott mappa nem üres, és nem tartalmaz "
                    "Andersen-forrást.\n\nVálassz üres mappát, vagy a meglévő "
                    "Andersen repo mappáját.",
                    parent=self.root,
                )
                return
            try:
                package = json.loads(package_file.read_text(encoding="utf-8"))
                name = str(package.get("name", ""))
            except Exception:
                name = ""
            if name != "worldscript-studio" and path.name.lower() != "andersen":
                messagebox.showerror(
                    "Andersen Launcher",
                    "A kiválasztott mappa package.json fájlja nem az "
                    "Andersen projekthez tartozik.",
                    parent=self.root,
                )
                return

        self.config.repo_path = path
        self.config.save()
        self.path_label.configure(text=shorten_path(path))
        self.log(f"Forrásmappa beállítva: {path}", "info")
        self.check_environment(silent=False, update_status=True)

    # -- lezárás ---------------------------------------------------------

    def _on_close(self) -> None:
        active = self.busy or self.server_state in ("starting", "running")
        if active:
            answer = messagebox.askyesnocancel(
                "Kilépés",
                "Jelenleg fut egy folyamat.\n\n"
                "Leállítsam kilépéskor?\n\n"
                "Igen — leállítás és kilépés\n"
                "Nem — futni hagyom\n"
                "Mégse — visszatérés",
                parent=self.root,
            )
            if answer is None:
                return
            if answer:
                self.stop_requested = True
                for proc in (self.current_process, self.server_process):
                    if proc is not None and proc.poll() is None:
                        self._kill_tree(proc)
                deadline = time.time() + 2.0
                for proc in (self.current_process, self.server_process):
                    if proc is not None:
                        try:
                            proc.wait(timeout=max(0.1, deadline - time.time()))
                        except Exception:
                            pass
        self._closing = True
        self.root.destroy()

    def _tk_exception(self, exc_type, exc_value, exc_tb) -> None:
        details = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        try:
            self.log(f"Felületi hiba: {exc_value}", "err")
        except Exception:
            pass
        traceback.print_exc()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    try:
        app = AndersenLauncher()
        app.run()
    except Exception as exc:
        try:
            messagebox.showerror(
                "Andersen Launcher",
                f"Nem sikerült elindítani a launchert:\n\n{exc}",
            )
        except Exception:
            print(exc, file=sys.stderr)
            raise


if __name__ == "__main__":
    main()

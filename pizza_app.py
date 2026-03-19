"""
Patel's Pizzas — Python Desktop App
A pizza restaurant game with animated pizza building, restaurant background,
and real-time canvas preview of your pizza being assembled.

Run with:  python pizza_app.py
Requires:  Python 3.8+ with tkinter (usually bundled, or install python3-tk)
"""

import json
import math
import os
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

# ─── Game Data ────────────────────────────────────────────────────────────────

PIZZA_BASES = [
    {"id": "thin",    "name": "Thin Crust",   "emoji": "⬜", "cost": 2,  "value": 4,
     "color": "#D4B483", "crust": "#B8955A"},
    {"id": "thick",   "name": "Thick Crust",  "emoji": "🟨", "cost": 3,  "value": 6,
     "color": "#DFC089", "crust": "#C4A060"},
    {"id": "stuffed", "name": "Stuffed Crust","emoji": "🟫", "cost": 5,  "value": 10,
     "color": "#E8CF96", "crust": "#D0A860"},
    {"id": "gluten",  "name": "Gluten-Free",  "emoji": "🌾", "cost": 4,  "value": 8,
     "color": "#C8A870", "crust": "#A88850"},
]

PIZZA_SAUCES = [
    {"id": "tomato", "name": "Tomato",     "emoji": "🍅", "cost": 1, "value": 2,
     "color": "#C0392B"},
    {"id": "white",  "name": "White Sauce","emoji": "🤍", "cost": 2, "value": 4,
     "color": "#F5F0E8"},
    {"id": "bbq",    "name": "BBQ Sauce",  "emoji": "🔴", "cost": 2, "value": 4,
     "color": "#7B3000"},
    {"id": "pesto",  "name": "Pesto",      "emoji": "🟢", "cost": 3, "value": 6,
     "color": "#2E7D32"},
]

TOPPINGS = {
    # Tier 1 — always available
    "cheese":      {"name": "Mozzarella",  "emoji": "🧀", "cost": 2,  "value": 4,
                    "color": "#F4D03F", "dot": "#D4B000", "tier": 1, "unlockReq": None},
    "basil":       {"name": "Basil",       "emoji": "🌿", "cost": 1,  "value": 2,
                    "color": "#1E8449", "dot": "#155724", "tier": 1, "unlockReq": None},
    "oregano":     {"name": "Oregano",     "emoji": "🌱", "cost": 1,  "value": 2,
                    "color": "#2D6A1F", "dot": "#1A4011", "tier": 1, "unlockReq": None},
    # Tier 2
    "mushrooms":   {"name": "Mushrooms",   "emoji": "🍄", "cost": 2,  "value": 5,
                    "color": "#7D6608", "dot": "#5D4A06", "tier": 2,
                    "unlockReq": {"pizzaType": "1", "amount": 5,  "pizzaName": "Margherita"}},
    "pepperoni":   {"name": "Pepperoni",   "emoji": "🔴", "cost": 3,  "value": 7,
                    "color": "#C0392B", "dot": "#922B21", "tier": 2,
                    "unlockReq": {"pizzaType": "2", "amount": 5,  "pizzaName": "Pepperoni"}},
    "bell_peppers":{"name": "Bell Peppers","emoji": "🫑", "cost": 2,  "value": 5,
                    "color": "#27AE60", "dot": "#1E8449", "tier": 2,
                    "unlockReq": {"pizzaType": "3", "amount": 5,  "pizzaName": "Vegetarian"}},
    "onions":      {"name": "Onions",      "emoji": "🧅", "cost": 2,  "value": 4,
                    "color": "#9B59B6", "dot": "#7D3C98", "tier": 2,
                    "unlockReq": {"pizzaType": "1", "amount": 10, "pizzaName": "Margherita"}},
    # Tier 3
    "jalapenos":   {"name": "Jalapeños",   "emoji": "🌶", "cost": 2,  "value": 5,
                    "color": "#E74C3C", "dot": "#C0392B", "tier": 3,
                    "unlockReq": {"pizzaType": "2", "amount": 15, "pizzaName": "Pepperoni"}},
    "pineapple":   {"name": "Pineapple",   "emoji": "🍍", "cost": 2,  "value": 6,
                    "color": "#F39C12", "dot": "#D68910", "tier": 3,
                    "unlockReq": {"pizzaType": "6", "amount": 8,  "pizzaName": "Hawaiian"}},
    "chicken":     {"name": "Chicken",     "emoji": "🍗", "cost": 4,  "value": 10,
                    "color": "#E8B74A", "dot": "#C8970A", "tier": 3,
                    "unlockReq": {"pizzaType": "5", "amount": 10, "pizzaName": "BBQ Chicken"}},
    # Tier 4
    "bacon":       {"name": "Bacon",       "emoji": "🥓", "cost": 4,  "value": 10,
                    "color": "#922B21", "dot": "#6E1F18", "tier": 4,
                    "unlockReq": {"pizzaType": "2", "amount": 20, "pizzaName": "Pepperoni"}},
    "beef":        {"name": "Beef",        "emoji": "🥩", "cost": 5,  "value": 12,
                    "color": "#884422", "dot": "#5C2E17", "tier": 4,
                    "unlockReq": {"pizzaType": "4", "amount": 15, "pizzaName": "Supreme"}},
    "olives":      {"name": "Black Olives","emoji": "🫒", "cost": 3,  "value": 7,
                    "color": "#1C2833", "dot": "#0E1626", "tier": 4,
                    "unlockReq": {"pizzaType": "3", "amount": 15, "pizzaName": "Vegetarian"}},
    # Tier 5
    "shrimp":      {"name": "Shrimp",      "emoji": "🦐", "cost": 6,  "value": 15,
                    "color": "#F1948A", "dot": "#E57068", "tier": 5,
                    "unlockReq": {"pizzaType": "4", "amount": 25, "pizzaName": "Supreme"}},
    "truffle":     {"name": "Truffle Oil", "emoji": "💎", "cost": 10, "value": 25,
                    "color": "#5D6D7E", "dot": "#2E4057", "tier": 5,
                    "unlockReq": {"pizzaType": "7", "amount": 10, "pizzaName": "Truffle"}},
    "gold":        {"name": "Gold Flakes", "emoji": "✨", "cost": 20, "value": 50,
                    "color": "#F4D03F", "dot": "#D4AC0D", "tier": 5,
                    "unlockReq": {"pizzaType": "7", "amount": 20, "pizzaName": "Truffle"}},
}

MENU_PIZZAS = {
    "1":  {"name": "Margherita",    "emoji": "🍅", "price": 12, "cost": 3, "time": 8,
           "difficulty": 1, "storage_req": 1},
    "2":  {"name": "Pepperoni",     "emoji": "🌶️", "price": 15, "cost": 4, "time": 10,
           "difficulty": 2, "storage_req": 1},
    "3":  {"name": "Vegetarian",    "emoji": "🥒", "price": 14, "cost": 4, "time": 9,
           "difficulty": 2, "storage_req": 2},
    "6":  {"name": "Hawaiian",      "emoji": "🍍", "price": 18, "cost": 5, "time": 11,
           "difficulty": 2, "storage_req": 2},
    "8":  {"name": "Four Cheese",   "emoji": "🧀", "price": 16, "cost": 5, "time": 10,
           "difficulty": 2, "storage_req": 2},
    "5":  {"name": "BBQ Chicken",   "emoji": "🍗", "price": 20, "cost": 6, "time": 12,
           "difficulty": 3, "storage_req": 3},
    "4":  {"name": "Supreme",       "emoji": "👑", "price": 25, "cost": 8, "time": 15,
           "difficulty": 3, "storage_req": 3},
    "9":  {"name": "Meat Feast",    "emoji": "🥩", "price": 22, "cost": 7, "time": 14,
           "difficulty": 3, "storage_req": 3},
    "7":  {"name": "Truffle",       "emoji": "💎", "price": 50, "cost": 12, "time": 18,
           "difficulty": 4, "storage_req": 4},
    "10": {"name": "Lobster Royale","emoji": "🦞", "price": 65, "cost": 15, "time": 20,
           "difficulty": 4, "storage_req": 4},
}

UPGRADE_COSTS = {
    "oven":      {1: 0, 2: 100, 3: 250, 4: 500, 5: 1000, 6: 2000},
    "workers":   {1: 0, 2: 150, 3: 350, 4: 700, 5: 1500},
    "quality":   {1: 0, 2: 75,  3: 150, 4: 300, 5: 600},
    "marketing": {1: 0, 2: 50,  3: 100, 4: 200, 5: 400},
    "storage":   {1: 0, 2: 100, 3: 250, 4: 500},
    "delivery":  {1: 0, 2: 75,  3: 175, 4: 350, 5: 700},
    "recipe":    {1: 0, 2: 100, 3: 225, 4: 450, 5: 900},
    "loyalty":   {1: 0, 2: 60,  3: 140, 4: 280, 5: 560},
}

UPGRADE_MAX = {
    "oven": 6, "workers": 5, "quality": 5, "marketing": 5,
    "storage": 4, "delivery": 5, "recipe": 5, "loyalty": 5,
}

SAVE_FILE = os.path.join(os.path.expanduser("~"), ".patels_pizzas_save.json")

# Colour palette
C_BG       = "#1a0a00"     # very dark brown — main window bg
C_WALL     = "#3B1A08"     # brick wall
C_MORTAR   = "#5C3317"     # mortar / lighter brick
C_BANNER   = "#8B0000"     # deep red banner
C_GOLD     = "#FFD700"     # gold text
C_GREEN    = "#4CAF50"     # success green
C_CARD     = "#2d1a0a"     # card background
C_COUNTER  = "#5C3317"     # wooden counter
C_WHITE    = "#FFFFFF"
C_GREY     = "#AAAAAA"
C_DKGREY   = "#555555"


# ─── Helper: draw restaurant background on a Canvas ──────────────────────────

def draw_restaurant_bg(canvas: tk.Canvas, width: int, height: int,
                       title: str = "") -> None:
    """Render a stylised restaurant background with bricks, lights and counter."""
    canvas.delete("bg")

    # ── Brick wall ──
    brick_h, brick_w, gap = 26, 76, 3
    for row in range(height // brick_h + 2):
        shade = "#3D1A08" if row % 2 == 0 else "#421E0A"
        offset = (brick_w // 2) if row % 2 else 0
        for col in range(-1, width // brick_w + 2):
            x1 = col * brick_w + offset
            y1 = row * brick_h
            x2 = x1 + brick_w - gap
            y2 = y1 + brick_h - gap
            canvas.create_rectangle(x1, y1, x2, y2,
                                    fill=shade, outline="#2A0F04",
                                    width=1, tags="bg")

    # ── Wooden counter strip at the bottom ──
    counter_y = height - 80
    canvas.create_rectangle(0, counter_y, width, height,
                             fill="#5C3317", outline="", tags="bg")
    canvas.create_rectangle(0, counter_y - 6, width, counter_y + 4,
                             fill="#7B4A1E", outline="", tags="bg")
    for x in range(0, width, 20):
        canvas.create_line(x, counter_y, x + 10, height,
                           fill="#4A2810", width=1, tags="bg")

    # ── Hanging light bulbs ──
    for bx in range(80, width, 140):
        canvas.create_line(bx, 0, bx, 44, fill="#C8A050", width=2, tags="bg")
        canvas.create_oval(bx - 12, 34, bx + 12, 58,
                           fill="#FFF8DC", outline="#C8A050",
                           width=2, tags="bg")
        # glow halo
        canvas.create_oval(bx - 26, 20, bx + 26, 72,
                           outline="#C8A050", fill="", width=4, tags="bg")

    # ── Small pizza oven silhouette (left) ──
    ov_x, ov_y = 20, counter_y - 110
    canvas.create_rectangle(ov_x, ov_y, ov_x + 80, counter_y - 8,
                             fill="#222", outline="#444", width=2, tags="bg")
    canvas.create_oval(ov_x + 8, ov_y + 8, ov_x + 72, ov_y + 50,
                       fill="#FF4500", outline="#FF6600", width=2, tags="bg")
    canvas.create_text(ov_x + 40, ov_y + 29, text="🔥",
                       font=("Arial", 14), tags="bg")
    canvas.create_text(ov_x + 40, counter_y - 18, text="OVEN",
                       fill="#AAAAAA", font=("Arial", 8, "bold"), tags="bg")

    # ── Title banner ──
    if title:
        bw, bh = min(480, width - 40), 56
        bx2 = (width - bw) // 2
        by2 = 10
        canvas.create_rectangle(bx2, by2, bx2 + bw, by2 + bh,
                                 fill="#8B0000", outline="#FFD700",
                                 width=3, tags="bg")
        canvas.create_text(bx2 + bw // 2, by2 + bh // 2, text=title,
                           fill="#FFD700", font=("Arial", 20, "bold"),
                           tags="bg")


# ─── Pizza Canvas Drawing ─────────────────────────────────────────────────────

def topping_positions(count: int, max_r: float):
    """Sunflower/Fibonacci spiral positions for toppings inside a circle."""
    if count == 0:
        return []
    golden = (1 + math.sqrt(5)) / 2
    positions = []
    for i in range(count):
        angle = 2 * math.pi * i / golden
        dist = max_r * math.sqrt((i + 0.5) / count)
        positions.append((math.cos(angle) * dist, math.sin(angle) * dist))
    return positions


def draw_pizza(canvas: tk.Canvas, cx: int, cy: int, r: int,
               base_id: str, sauce_id: str, toppings_list: list,
               baked: bool = False) -> None:
    """Draw a pizza on `canvas` centred at (cx, cy) with radius r."""
    canvas.delete("pizza")

    # Pick base colours
    base_obj = next((b for b in PIZZA_BASES if b["id"] == base_id), PIZZA_BASES[0])
    if baked:
        dough_fill  = "#C89820"
        crust_fill  = "#8B6410"
    else:
        dough_fill  = base_obj["color"]
        crust_fill  = base_obj["crust"]

    # Wooden pizza board
    canvas.create_oval(cx - r - 18, cy - r - 18,
                       cx + r + 18, cy + r + 18,
                       fill="#6B4226", outline="#4A2E18",
                       width=3, tags="pizza")
    canvas.create_oval(cx - r - 14, cy - r - 14,
                       cx + r + 14, cy + r + 14,
                       fill="#8B5A2B", outline="",
                       tags="pizza")

    # Crust ring
    canvas.create_oval(cx - r - 10, cy - r - 10,
                       cx + r + 10, cy + r + 10,
                       fill=crust_fill, outline="#5C3A10",
                       width=2, tags="pizza")

    # Dough base
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                       fill=dough_fill, outline="#7A5C30",
                       width=1, tags="pizza")

    # Sauce layer
    sauce_obj = next((s for s in PIZZA_SAUCES if s["id"] == sauce_id), PIZZA_SAUCES[0])
    sr = int(r * 0.88)
    if baked:
        # slightly darkened sauce when baked
        sauce_color = sauce_obj["color"]
    else:
        sauce_color = sauce_obj["color"]
    canvas.create_oval(cx - sr, cy - sr, cx + sr, cy + sr,
                       fill=sauce_color, outline="", tags="pizza")

    # Toppings
    if toppings_list:
        positions = topping_positions(len(toppings_list), r * 0.76)
        for i, key in enumerate(toppings_list):
            t = TOPPINGS.get(key)
            if not t:
                continue
            tx, ty = positions[i] if i < len(positions) else (0.0, 0.0)
            tr = 16 if r < 120 else 20
            # Coloured blob
            canvas.create_oval(cx + tx - tr, cy + ty - tr,
                               cx + tx + tr, cy + ty + tr,
                               fill=t["color"], outline=t["dot"],
                               width=1, tags="pizza")
            # Emoji label
            font_size = 11 if r < 120 else 14
            canvas.create_text(cx + tx, cy + ty, text=t["emoji"],
                               font=("Segoe UI Emoji", font_size),
                               tags="pizza")

    # If baked: add golden sheen + star
    if baked:
        canvas.create_oval(cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2,
                           outline="#FFD700", width=3, tags="pizza")

    # Base name label
    canvas.create_text(cx, cy + r + 26, text=f"🍕 {base_obj['name']} Pizza",
                       fill=C_GOLD, font=("Arial", 10, "bold"), tags="pizza")


# ─── Main Application ─────────────────────────────────────────────────────────

class PatelsPizzasApp:
    """Main application class for Patel's Pizzas desktop game."""

    # ── Init ──────────────────────────────────────────────────────────────────

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("🍕 Patel's Pizzas")
        self.root.geometry("1150x760")
        self.root.configure(bg=C_BG)
        self.root.minsize(960, 680)

        self.game_state: dict = self._default_state()
        self.custom_state: dict = {"base": "thin", "sauce": "tomato", "toppings": []}

        # Animation
        self._anim_step = 0
        self._anim_steps: list = []
        self._anim_job: str | None = None
        self._anim_cost = 0
        self._anim_sell_value = 0

        # Timer
        self._timer_job: str | None = None

        # Bg canvas references (updated on resize)
        self._bg_canvas: dict[str, tk.Canvas] = {}

        self._build_all_screens()
        self._show_screen("intro")

    # ── State ─────────────────────────────────────────────────────────────────

    def _default_state(self) -> dict:
        return {
            "money": 100,
            "total_earned": 0,
            "pizzas_sold": 0,
            "total_baked": 0,
            "custom_made": 0,
            "custom_profit": 0,
            "pizza_stats": {k: 0 for k in MENU_PIZZAS},
            "oven_level": 1,
            "workers_level": 1,
            "quality_level": 1,
            "marketing_level": 1,
            "storage_level": 1,
            "delivery_level": 1,
            "recipe_level": 1,
            "loyalty_level": 1,
            "ovens": [],
            "session_start": time.time(),
            "game_running": False,
            "total_bonuses": 0,
        }

    # ── Screen Management ─────────────────────────────────────────────────────

    def _build_all_screens(self) -> None:
        self.screens: dict[str, tk.Frame] = {}
        self._build_intro()
        self._build_game()
        self._build_custom_builder()
        self._build_making_screen()
        self._build_shop()

    def _show_screen(self, name: str) -> None:
        for s in self.screens.values():
            s.place_forget()
        self.screens[name].place(x=0, y=0, relwidth=1.0, relheight=1.0)
        if name == "game":
            self._refresh_game()
        elif name == "custom":
            self._refresh_custom()
        elif name == "shop":
            self._refresh_shop()

    # ── Restaurant background helper ──────────────────────────────────────────

    def _make_bg_canvas(self, parent: tk.Widget, title: str = "") -> tk.Canvas:
        """Create a canvas with a resizable restaurant background."""
        canvas = tk.Canvas(parent, highlightthickness=0, bg=C_WALL)
        canvas.pack(fill="both", expand=True)

        def _on_resize(event: tk.Event) -> None:
            draw_restaurant_bg(canvas, event.width, event.height, title)

        canvas.bind("<Configure>", _on_resize)
        # Trigger once the canvas has been mapped
        canvas.after(30, lambda: draw_restaurant_bg(
            canvas,
            canvas.winfo_width() or 1150,
            canvas.winfo_height() or 760,
            title,
        ))
        return canvas

    # ─────────────────────────────────────────────────────────────────────────
    # INTRO SCREEN
    # ─────────────────────────────────────────────────────────────────────────

    def _build_intro(self) -> None:
        frame = tk.Frame(self.root, bg=C_BG)
        self.screens["intro"] = frame

        canvas = self._make_bg_canvas(frame, "🍕  PATEL'S PIZZAS  🍕")

        # Centred content overlay
        overlay = tk.Frame(canvas, bg=C_CARD, bd=3, relief="ridge")
        overlay.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(overlay, text="🍕", font=("Segoe UI Emoji", 64),
                 bg=C_CARD).pack(pady=(20, 4))
        tk.Label(overlay, text="PATEL'S PIZZAS",
                 font=("Arial", 32, "bold"), bg=C_CARD, fg=C_GOLD).pack()
        tk.Label(overlay, text="Rizwan Waseem  ×  Ali Imran",
                 font=("Arial", 12), bg=C_CARD, fg=C_GREY).pack(pady=4)
        tk.Label(overlay, text="© 2026  All Rights Reserved",
                 font=("Arial", 9), bg=C_CARD, fg="#666666").pack()

        btn_f = tk.Frame(overlay, bg=C_CARD)
        btn_f.pack(pady=20)

        self._btn(btn_f, "🎮  Start New Game",
                  lambda: self._start_new_game(),
                  bg="#C0392B").pack(fill="x", pady=4, padx=30)
        self._btn(btn_f, "📂  Load Game",
                  self._load_game, bg="#2980B9").pack(fill="x", pady=4, padx=30)
        self._btn(btn_f, "📖  How to Play",
                  self._show_instructions, bg="#27AE60").pack(fill="x", pady=4, padx=30)
        self._btn(btn_f, "❌  Quit",
                  self.root.quit, bg=C_DKGREY).pack(fill="x", pady=4, padx=30)

    # ─────────────────────────────────────────────────────────────────────────
    # GAME SCREEN
    # ─────────────────────────────────────────────────────────────────────────

    def _build_game(self) -> None:
        frame = tk.Frame(self.root, bg=C_BG)
        self.screens["game"] = frame

        # ── Top stats bar ──
        top = tk.Frame(frame, bg=C_BANNER, pady=5)
        top.pack(fill="x")

        self._lbl_money = self._stat_lbl(top, "💰 $100")
        self._lbl_sold  = self._stat_lbl(top, "🍕 Sold: 0")
        self._lbl_earned = self._stat_lbl(top, "📊 Earned: $0")
        self._lbl_time  = self._stat_lbl(top, "⏱️ 0s")

        # ── Navigation bar ──
        nav = tk.Frame(frame, bg="#1a0a00", pady=3)
        nav.pack(fill="x")

        self._btn(nav, "🍕 Custom Pizza", self._open_custom,
                  bg="#C0392B").pack(side="left", padx=4, pady=2)
        self._btn(nav, "🏪 Shop", lambda: self._show_screen("shop"),
                  bg="#2980B9").pack(side="left", padx=4, pady=2)
        self._btn(nav, "💾 Save", self._save_game,
                  bg="#27AE60").pack(side="left", padx=4, pady=2)
        self._btn(nav, "🚪 Main Menu",
                  lambda: self._show_screen("intro"),
                  bg=C_DKGREY).pack(side="right", padx=4, pady=2)

        # ── Body: menu (left) + oven panel (right) ──
        body = tk.Frame(frame, bg=C_BG)
        body.pack(fill="both", expand=True, padx=8, pady=6)

        # Left: scrollable pizza menu
        left = tk.Frame(body, bg=C_BG)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="📋  PIZZA MENU",
                 font=("Arial", 13, "bold"),
                 bg=C_BG, fg=C_GOLD).pack(pady=4)

        scroll_canvas = tk.Canvas(left, bg=C_BG, highlightthickness=0)
        vsb = ttk.Scrollbar(left, orient="vertical",
                            command=scroll_canvas.yview)
        self._menu_frame = tk.Frame(scroll_canvas, bg=C_BG)
        self._menu_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(
                scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=self._menu_frame,
                                    anchor="nw")
        scroll_canvas.configure(yscrollcommand=vsb.set)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Right: oven status
        right = tk.Frame(body, bg=C_MORTAR, bd=2, relief="ridge", width=300)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.pack_propagate(False)

        tk.Label(right, text="🔥  OVEN STATUS",
                 font=("Arial", 13, "bold"),
                 bg=C_MORTAR, fg=C_GOLD).pack(pady=8)

        self._oven_labels: list[tk.Label] = []
        for i in range(6):
            lbl = tk.Label(right, text=f"Slot {i + 1}: Empty",
                           font=("Arial", 10), bg=C_MORTAR, fg=C_GREY,
                           relief="groove", padx=8, pady=6, anchor="w",
                           wraplength=260)
            lbl.pack(fill="x", padx=8, pady=3)
            self._oven_labels.append(lbl)

    def _refresh_game(self) -> None:
        gs = self.game_state
        self._lbl_money.config(text=f"💰 ${gs['money']:,}")
        self._lbl_sold.config(text=f"🍕 Sold: {gs['pizzas_sold']}")
        self._lbl_earned.config(text=f"📊 Earned: ${gs['total_earned']:,}")

        # Rebuild menu cards
        for w in self._menu_frame.winfo_children():
            w.destroy()

        storage = gs["storage_level"]
        for key, pizza in MENU_PIZZAS.items():
            if pizza["storage_req"] > storage:
                continue
            sold = gs["pizza_stats"].get(key, 0)
            price = self._pizza_price(pizza)
            can_afford = gs["money"] >= pizza["cost"]
            bake_t = self._bake_time(pizza["time"])

            card = tk.Frame(self._menu_frame, bg=C_CARD,
                            relief="ridge", bd=2)
            card.pack(fill="x", padx=4, pady=3)

            r1 = tk.Frame(card, bg=C_CARD)
            r1.pack(fill="x", padx=8, pady=(6, 2))
            tk.Label(r1,
                     text=f"{pizza['emoji']}  {pizza['name']}",
                     font=("Arial", 12, "bold"),
                     bg=C_CARD, fg=C_GOLD).pack(side="left")
            tk.Label(r1, text=f"💰 ${price}",
                     font=("Arial", 11), bg=C_CARD, fg="#4CAF50").pack(side="right")

            r2 = tk.Frame(card, bg=C_CARD)
            r2.pack(fill="x", padx=8)
            stars = "⭐" * pizza["difficulty"]
            tk.Label(r2,
                     text=f"Cost: ${pizza['cost']}  |  Bake: {bake_t}s  |  {stars}  |  Sold: {sold}",
                     font=("Arial", 9), bg=C_CARD, fg=C_GREY).pack(side="left")

            r3 = tk.Frame(card, bg=C_CARD)
            r3.pack(fill="x", padx=8, pady=(4, 6))
            self._btn(r3, f"🍕 Bake  (−${pizza['cost']})",
                      lambda k=key: self._bake_pizza(k),
                      bg="#C0392B" if can_afford else C_DKGREY,
                      state="normal" if can_afford else "disabled",
                      font=("Arial", 11, "bold")).pack(side="left")

        self._refresh_oven_labels()

    def _refresh_oven_labels(self) -> None:
        gs = self.game_state
        cap = self._oven_cap()
        now = time.time()

        for i, lbl in enumerate(self._oven_labels):
            if i >= cap:
                lbl.config(text=f"Slot {i + 1}: 🔒 Locked",
                           fg="#555555", bg="#1A0800", cursor="arrow")
                lbl.unbind("<Button-1>")
                continue

            if i < len(gs["ovens"]):
                slot = gs["ovens"][i]
                remaining = max(0.0, slot["finish_time"] - now)
                pizza = MENU_PIZZAS[slot["pizza_key"]]
                if remaining > 0:
                    lbl.config(
                        text=f"Slot {i + 1}: {pizza['emoji']} {pizza['name']}"
                             f"  ({remaining:.0f}s left)",
                        fg=C_GOLD, bg=C_MORTAR, cursor="arrow")
                    lbl.unbind("<Button-1>")
                else:
                    price = self._pizza_price(pizza)
                    lbl.config(
                        text=f"Slot {i + 1}: ✅ {pizza['name']}"
                             f"  — tap to sell ${price}",
                        fg="#4CAF50", bg="#1A3A1A", cursor="hand2")
                    lbl.bind("<Button-1>", lambda e, idx=i: self._sell_pizza(idx))
            else:
                lbl.config(text=f"Slot {i + 1}: Empty",
                           fg=C_GREY, bg=C_MORTAR, cursor="arrow")
                lbl.unbind("<Button-1>")

    def _bake_pizza(self, key: str) -> None:
        gs = self.game_state
        pizza = MENU_PIZZAS[key]
        cap = self._oven_cap()

        if len(gs["ovens"]) >= cap:
            messagebox.showwarning(
                "Oven Full",
                "All oven slots are in use!\nSell a finished pizza first.")
            return
        if gs["money"] < pizza["cost"]:
            messagebox.showwarning(
                "Not Enough Money",
                f"You need ${pizza['cost']} to bake this pizza.")
            return

        gs["money"] -= pizza["cost"]
        bake_t = self._bake_time(pizza["time"])
        gs["ovens"].append({
            "pizza_key": key,
            "finish_time": time.time() + bake_t,
        })
        gs["total_baked"] += 1
        self._refresh_game()

    def _sell_pizza(self, slot_idx: int) -> None:
        gs = self.game_state
        if slot_idx >= len(gs["ovens"]):
            return
        slot = gs["ovens"][slot_idx]
        if time.time() < slot["finish_time"]:
            return

        pizza = MENU_PIZZAS[slot["pizza_key"]]
        price = self._pizza_price(pizza)
        delivery_bonus = (gs["delivery_level"] - 1) * 2
        doubled = random.random() < (gs["loyalty_level"] - 1) * 0.05
        total = (price + delivery_bonus) * (2 if doubled else 1)

        gs["money"] += total
        gs["total_earned"] += total
        gs["pizzas_sold"] += 1
        gs["total_bonuses"] += delivery_bonus
        gs["pizza_stats"][slot["pizza_key"]] = (
            gs["pizza_stats"].get(slot["pizza_key"], 0) + 1)
        gs["ovens"].pop(slot_idx)

        msg = f"✅ Sold {pizza['emoji']} {pizza['name']} for ${total}!"
        if doubled:
            msg += "  🎉 DOUBLED!"
        self._toast(msg)
        self._refresh_game()

    # ─────────────────────────────────────────────────────────────────────────
    # CUSTOM PIZZA BUILDER
    # ─────────────────────────────────────────────────────────────────────────

    def _build_custom_builder(self) -> None:
        frame = tk.Frame(self.root, bg=C_BG)
        self.screens["custom"] = frame

        # Header
        hdr = tk.Frame(frame, bg=C_BANNER, pady=5)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🍕  CUSTOM PIZZA BUILDER",
                 font=("Arial", 15, "bold"), bg=C_BANNER, fg=C_GOLD).pack(side="left", padx=15)
        self._lbl_builder_money = tk.Label(
            hdr, text="💰 $100", font=("Arial", 13, "bold"),
            bg=C_BANNER, fg="#4CAF50")
        self._lbl_builder_money.pack(side="right", padx=15)
        self._btn(hdr, "← Back", lambda: self._show_screen("game"),
                  bg=C_DKGREY).pack(side="right", padx=6, pady=2)

        # Body: left = options, right = live pizza preview
        body = tk.Frame(frame, bg=C_BG)
        body.pack(fill="both", expand=True, padx=8, pady=6)

        # LEFT — options panel
        left_outer = tk.Frame(body, bg=C_BG)
        left_outer.pack(side="left", fill="both", expand=True)

        lcan = tk.Canvas(left_outer, bg=C_BG, highlightthickness=0)
        lsb = ttk.Scrollbar(left_outer, orient="vertical",
                             command=lcan.yview)
        self._builder_inner = tk.Frame(lcan, bg=C_CARD)
        self._builder_inner.bind(
            "<Configure>",
            lambda e: lcan.configure(scrollregion=lcan.bbox("all")))
        lcan.create_window((0, 0), window=self._builder_inner, anchor="nw")
        lcan.configure(yscrollcommand=lsb.set)
        lcan.pack(side="left", fill="both", expand=True)
        lsb.pack(side="right", fill="y")

        # RIGHT — live pizza preview
        right = tk.Frame(body, bg=C_BG, width=380)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.pack_propagate(False)

        tk.Label(right, text="👀  WATCH YOUR PIZZA",
                 font=("Arial", 13, "bold"),
                 bg=C_BG, fg=C_GOLD).pack(pady=8)

        # Pizza preview canvas
        self._preview_canvas = tk.Canvas(
            right, width=340, height=340,
            bg="#2D1A0A", highlightthickness=3,
            highlightbackground=C_GOLD)
        self._preview_canvas.pack(pady=4)

        # Cost info
        cost_f = tk.Frame(right, bg=C_BG)
        cost_f.pack(fill="x", padx=10, pady=4)
        self._lbl_cost   = tk.Label(cost_f, text="Cost: $0",
                                    font=("Arial", 11), bg=C_BG, fg="#E74C3C")
        self._lbl_cost.pack()
        self._lbl_value  = tk.Label(cost_f, text="Sell Value: $0",
                                    font=("Arial", 11), bg=C_BG, fg="#4CAF50")
        self._lbl_value.pack()
        self._lbl_profit = tk.Label(cost_f, text="Profit: $0",
                                    font=("Arial", 12, "bold"), bg=C_BG,
                                    fg=C_GOLD)
        self._lbl_profit.pack()

        self._btn_make = self._btn(
            right, "🍕  Make My Pizza!",
            self._start_making,
            font=("Arial", 13, "bold"),
            bg="#C0392B", pady=10)
        self._btn_make.pack(fill="x", padx=10, pady=8)

    def _refresh_custom(self) -> None:
        gs = self.game_state
        self._lbl_builder_money.config(text=f"💰 ${gs['money']:,}")

        inner = self._builder_inner
        for w in inner.winfo_children():
            w.destroy()

        # ── Base selection ──
        self._section_header(inner, "🍞  Choose Your Base")
        row = tk.Frame(inner, bg=C_CARD)
        row.pack(fill="x", padx=10, pady=2)
        for b in PIZZA_BASES:
            sel = self.custom_state["base"] == b["id"]
            self._opt_btn(row, f"{b['emoji']} {b['name']}\n${b['cost']}",
                          lambda bid=b["id"]: self._sel_base(bid),
                          selected=sel).pack(side="left", padx=3, pady=3)

        # ── Sauce selection ──
        self._section_header(inner, "🍅  Choose Your Sauce")
        row2 = tk.Frame(inner, bg=C_CARD)
        row2.pack(fill="x", padx=10, pady=2)
        for s in PIZZA_SAUCES:
            sel = self.custom_state["sauce"] == s["id"]
            self._opt_btn(row2, f"{s['emoji']} {s['name']}\n${s['cost']}",
                          lambda sid=s["id"]: self._sel_sauce(sid),
                          selected=sel).pack(side="left", padx=3, pady=3)

        # ── Toppings ──
        self._section_header(inner,
                             "🧀  Choose Toppings  (max 6 — sell menu pizzas to unlock more!)")

        sorted_keys = sorted(
            TOPPINGS.keys(),
            key=lambda k: (TOPPINGS[k]["tier"], TOPPINGS[k]["value"]))

        grid_f = tk.Frame(inner, bg=C_CARD)
        grid_f.pack(fill="x", padx=10)
        col = 0
        max_cols = 4
        row_f = None

        for key in sorted_keys:
            t = TOPPINGS[key]
            unlocked = self._topping_unlocked(key)
            selected = key in self.custom_state["toppings"]

            if col % max_cols == 0:
                row_f = tk.Frame(grid_f, bg=C_CARD)
                row_f.pack(fill="x", pady=2)

            if unlocked:
                label = f"{t['emoji']} {t['name']}\n+${t['cost']}"
                if selected:
                    label += "  ✓"
                self._opt_btn(row_f, label,
                              lambda k=key: self._toggle_topping(k),
                              selected=selected,
                              width=10).pack(side="left", padx=2, pady=1)
            else:
                req = t.get("unlockReq") or {}
                progress = gs["pizza_stats"].get(req.get("pizzaType", ""), 0)
                label = (f"{t['emoji']} {t['name']}\n"
                         f"🔒 {progress}/{req.get('amount', '?')}")
                tk.Button(row_f, text=label,
                          font=("Arial", 8), bg="#222222", fg="#555555",
                          relief="flat", width=10, wraplength=80,
                          justify="center", state="disabled",
                          pady=4).pack(side="left", padx=2, pady=1)
            col += 1

        # ── Cost summary ──
        cost  = self._calc_cost()
        value = self._calc_value()
        profit = value - cost

        self._lbl_cost.config(text=f"Ingredient Cost: ${cost}")
        self._lbl_value.config(text=f"Sell Value: ${value}")
        self._lbl_profit.config(
            text=f"Profit: {'+' if profit >= 0 else ''}{profit}",
            fg="#4CAF50" if profit >= 0 else "#E74C3C")

        can_make = gs["money"] >= cost and len(self.custom_state["toppings"]) > 0
        if not can_make:
            msg = (f"❌ Need ${cost}" if gs["money"] < cost
                   else "🍕 Select at least one topping!")
            self._btn_make.config(text=msg, state="disabled", bg=C_DKGREY)
        else:
            self._btn_make.config(
                text=f"🍕  Make My Pizza!  (−${cost})",
                state="normal", bg="#C0392B")

        # Live pizza preview
        self._draw_preview()

    def _draw_preview(self) -> None:
        c = self._preview_canvas
        c.delete("all")
        c.create_rectangle(0, 0, 340, 340, fill="#2D1A0A", outline="")
        draw_pizza(c, 170, 170, 130,
                   self.custom_state["base"],
                   self.custom_state["sauce"],
                   self.custom_state["toppings"])

    def _sel_base(self, bid: str) -> None:
        self.custom_state["base"] = bid
        self._refresh_custom()

    def _sel_sauce(self, sid: str) -> None:
        self.custom_state["sauce"] = sid
        self._refresh_custom()

    def _toggle_topping(self, key: str) -> None:
        if not self._topping_unlocked(key):
            return
        t = self.custom_state["toppings"]
        if key in t:
            t.remove(key)
        else:
            if len(t) >= 6:
                self._toast("⚠️ Maximum 6 toppings allowed!")
                return
            t.append(key)
        self._refresh_custom()

    def _topping_unlocked(self, key: str) -> bool:
        req = TOPPINGS[key].get("unlockReq")
        if not req:
            return True
        return (self.game_state["pizza_stats"].get(req["pizzaType"], 0)
                >= req["amount"])

    def _calc_cost(self) -> int:
        base   = next((b for b in PIZZA_BASES
                       if b["id"] == self.custom_state["base"]), None)
        sauce  = next((s for s in PIZZA_SAUCES
                       if s["id"] == self.custom_state["sauce"]), None)
        cost = (base["cost"] if base else 0) + (sauce["cost"] if sauce else 0)
        for k in self.custom_state["toppings"]:
            cost += TOPPINGS[k]["cost"]
        return cost

    def _calc_value(self) -> int:
        base  = next((b for b in PIZZA_BASES
                      if b["id"] == self.custom_state["base"]), None)
        sauce = next((s for s in PIZZA_SAUCES
                      if s["id"] == self.custom_state["sauce"]), None)
        value = (base["value"] if base else 0) + (sauce["value"] if sauce else 0)
        for k in self.custom_state["toppings"]:
            value += TOPPINGS[k]["value"]
        recipe_mult = 1 + (self.game_state["recipe_level"] - 1) * 0.2
        return int(value * recipe_mult)

    # ─────────────────────────────────────────────────────────────────────────
    # PIZZA MAKING ANIMATION SCREEN
    # ─────────────────────────────────────────────────────────────────────────

    def _build_making_screen(self) -> None:
        frame = tk.Frame(self.root, bg=C_BG)
        self.screens["making"] = frame

        # Header
        hdr = tk.Frame(frame, bg=C_BANNER, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👨‍🍳  WATCH YOUR PIZZA BEING MADE!",
                 font=("Arial", 16, "bold"), bg=C_BANNER, fg=C_GOLD).pack()

        # Body
        body = tk.Frame(frame, bg=C_BG)
        body.pack(fill="both", expand=True, padx=20, pady=12)

        # LEFT — animated pizza canvas
        left = tk.Frame(body, bg=C_BG)
        left.pack(side="left", fill="both", expand=True)

        self._making_canvas = tk.Canvas(
            left, width=420, height=420,
            bg="#2D1A0A", highlightthickness=3,
            highlightbackground=C_GOLD)
        self._making_canvas.pack(pady=8)

        self._lbl_step = tk.Label(
            left, text="Preparing...",
            font=("Arial", 14, "bold"), bg=C_BG, fg=C_GOLD,
            wraplength=420)
        self._lbl_step.pack(pady=4)

        prog_f = tk.Frame(left, bg=C_BG)
        prog_f.pack(fill="x", padx=10)
        self._progress = ttk.Progressbar(
            prog_f, length=400, mode="determinate", maximum=100)
        self._progress.pack(fill="x")

        # RIGHT — details panel
        right = tk.Frame(body, bg=C_CARD, bd=2, relief="ridge", width=290)
        right.pack(side="right", fill="y", padx=(14, 0))
        right.pack_propagate(False)

        tk.Label(right, text="📋  PIZZA DETAILS",
                 font=("Arial", 13, "bold"), bg=C_CARD, fg=C_GOLD).pack(pady=10)

        self._lbl_details = tk.Label(
            right, text="", font=("Arial", 11),
            bg=C_CARD, fg=C_WHITE, justify="left", wraplength=260)
        self._lbl_details.pack(padx=12, pady=4, anchor="w")

        self._lbl_result = tk.Label(
            right, text="", font=("Arial", 14, "bold"),
            bg=C_CARD, fg="#4CAF50", wraplength=260)
        self._lbl_result.pack(padx=12, pady=20)

    def _start_making(self) -> None:
        cost = self._calc_cost()
        gs = self.game_state

        if gs["money"] < cost:
            messagebox.showwarning("Not Enough Money",
                                   f"You need ${cost} to make this pizza!")
            return
        if not self.custom_state["toppings"]:
            messagebox.showwarning("No Toppings",
                                   "Please select at least one topping!")
            return

        gs["money"] -= cost
        self._refresh_game()

        # Build animation steps
        base  = next(b for b in PIZZA_BASES
                     if b["id"] == self.custom_state["base"])
        sauce = next(s for s in PIZZA_SAUCES
                     if s["id"] == self.custom_state["sauce"])
        sel_toppings = list(self.custom_state["toppings"])
        sell_val = self._calc_value()

        steps = [
            {"label": f"🍞  Preparing {base['name']} dough...",
             "progress": 8, "show_sauce": False, "toppings": []},
            {"label": f"{sauce['emoji']}  Spreading {sauce['name']} sauce...",
             "progress": 18, "show_sauce": True, "toppings": []},
        ]
        added: list[str] = []
        for i, key in enumerate(sel_toppings):
            t = TOPPINGS[key]
            prog = 18 + int(((i + 1) / len(sel_toppings)) * 55)
            added = added + [key]
            steps.append({
                "label": f"{t['emoji']}  Adding {t['name']}...",
                "progress": prog,
                "show_sauce": True,
                "toppings": list(added),
            })
        steps.append({"label": "🔥  Sliding into the oven...",
                      "progress": 80, "show_sauce": True,
                      "toppings": list(added)})
        steps.append({"label": "⏳  Baking your masterpiece...",
                      "progress": 92, "show_sauce": True,
                      "toppings": list(added)})
        steps.append({"label": "🍕  Almost done!",
                      "progress": 100, "show_sauce": True,
                      "toppings": list(added)})

        self._anim_steps = steps
        self._anim_step  = 0
        self._anim_cost  = cost
        self._anim_sell_value = sell_val

        # Reset result label
        self._lbl_result.config(text="")
        self._show_screen("making")
        self._run_anim()

    def _run_anim(self) -> None:
        if self._anim_step >= len(self._anim_steps):
            self._finish_making()
            return

        step = self._anim_steps[self._anim_step]
        self._lbl_step.config(text=step["label"])
        self._progress["value"] = step["progress"]

        # Draw pizza state
        c = self._making_canvas
        c.delete("all")
        c.create_rectangle(0, 0, 420, 420, fill="#2D1A0A", outline="")

        cx, cy, r = 210, 200, 155
        # wooden board
        c.create_oval(cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18,
                      fill="#6B4226", outline="#4A2E18", width=3)
        c.create_oval(cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14,
                      fill="#8B5A2B", outline="")

        base_obj = next(b for b in PIZZA_BASES
                        if b["id"] == self.custom_state["base"])
        crust_f = base_obj["crust"]
        dough_f = base_obj["color"]

        c.create_oval(cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10,
                      fill=crust_f, outline="#5C3A10", width=2)
        c.create_oval(cx - r, cy - r, cx + r, cy + r,
                      fill=dough_f, outline="#7A5C30", width=1)

        if step["show_sauce"]:
            sauce_obj = next(s for s in PIZZA_SAUCES
                             if s["id"] == self.custom_state["sauce"])
            sr = int(r * 0.88)
            c.create_oval(cx - sr, cy - sr, cx + sr, cy + sr,
                          fill=sauce_obj["color"], outline="")

        if step["toppings"]:
            positions = topping_positions(len(step["toppings"]), r * 0.76)
            for i, key in enumerate(step["toppings"]):
                t = TOPPINGS.get(key)
                if not t:
                    continue
                tx, ty = positions[i] if i < len(positions) else (0.0, 0.0)
                c.create_oval(cx + tx - 20, cy + ty - 20,
                              cx + tx + 20, cy + ty + 20,
                              fill=t["color"], outline=t["dot"], width=1)
                c.create_text(cx + tx, cy + ty, text=t["emoji"],
                              font=("Segoe UI Emoji", 15))

        # Oven glow on last two steps
        if self._anim_step >= len(self._anim_steps) - 2:
            for i in range(4):
                gr = r + 18 + i * 9
                c.create_oval(cx - gr, cy - gr, cx + gr, cy + gr,
                              outline=f"#FF{(60 + i * 20):02X}00", width=2)

        c.create_text(cx, 390, text=f"🍕 {base_obj['name']} Pizza",
                      fill=C_GOLD, font=("Arial", 11, "bold"))

        # Details panel
        base_n = base_obj["name"]
        sauce_n = next(s["name"] for s in PIZZA_SAUCES
                       if s["id"] == self.custom_state["sauce"])
        details = f"Base:   {base_n}\nSauce: {sauce_n}\n\nToppings added:\n"
        for k in step["toppings"]:
            details += f"  {TOPPINGS[k]['emoji']}  {TOPPINGS[k]['name']}\n"
        self._lbl_details.config(text=details)

        self._anim_step += 1
        self._anim_job = self.root.after(650, self._run_anim)

    def _finish_making(self) -> None:
        gs = self.game_state
        sv   = self._anim_sell_value
        cost = self._anim_cost
        profit = sv - cost

        gs["money"]        += sv
        gs["total_earned"] += sv
        gs["custom_made"]  += 1
        gs["custom_profit"] += profit

        self._lbl_step.config(text="✅  Pizza Ready!  Sold!")
        self._progress["value"] = 100

        self._lbl_result.config(
            text=f"🎉 Sold for ${sv}!\nProfit: {'+' if profit >= 0 else ''}{profit}",
            fg="#4CAF50" if profit >= 0 else "#E74C3C")

        # Draw the final baked pizza
        c = self._making_canvas
        c.delete("all")
        c.create_rectangle(0, 0, 420, 420, fill="#2D1A0A", outline="")
        draw_pizza(c, 210, 200, 155,
                   self.custom_state["base"],
                   self.custom_state["sauce"],
                   self.custom_state["toppings"],
                   baked=True)
        c.create_text(210, 22, text="⭐  PERFECT!  ⭐",
                      fill=C_GOLD, font=("Arial", 16, "bold"))
        c.create_text(210, 390, text=f"💰 Sold for ${sv}!",
                      fill="#4CAF50", font=("Arial", 12, "bold"))

        self.root.after(2600, self._after_making)

    def _after_making(self) -> None:
        self.custom_state["toppings"] = []
        self._show_screen("custom")
        self._toast(f"🍕 Custom pizza sold for ${self._anim_sell_value}! "
                    f"Profit: ${self._anim_sell_value - self._anim_cost}")

    # ─────────────────────────────────────────────────────────────────────────
    # UPGRADE SHOP
    # ─────────────────────────────────────────────────────────────────────────

    def _build_shop(self) -> None:
        frame = tk.Frame(self.root, bg=C_BG)
        self.screens["shop"] = frame

        hdr = tk.Frame(frame, bg=C_BANNER, pady=5)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏪  UPGRADE SHOP",
                 font=("Arial", 16, "bold"), bg=C_BANNER, fg=C_GOLD).pack(side="left", padx=15)
        self._lbl_shop_money = tk.Label(
            hdr, text="💰 $100", font=("Arial", 13, "bold"),
            bg=C_BANNER, fg="#4CAF50")
        self._lbl_shop_money.pack(side="right", padx=15)
        self._btn(hdr, "← Back to Game",
                  lambda: self._show_screen("game"),
                  bg=C_DKGREY).pack(side="right", padx=6, pady=2)

        shop_canvas = tk.Canvas(frame, bg=C_BG, highlightthickness=0)
        ssb = ttk.Scrollbar(frame, orient="vertical",
                            command=shop_canvas.yview)
        self._shop_inner = tk.Frame(shop_canvas, bg=C_BG)
        self._shop_inner.bind(
            "<Configure>",
            lambda e: shop_canvas.configure(
                scrollregion=shop_canvas.bbox("all")))
        shop_canvas.create_window((0, 0), window=self._shop_inner, anchor="nw")
        shop_canvas.configure(yscrollcommand=ssb.set)
        shop_canvas.pack(side="left", fill="both", expand=True)
        ssb.pack(side="right", fill="y")

    UPGRADES = [
        ("oven",       "🔥  Oven",           "Reduces bake time 30% per level"),
        ("workers",    "👨‍💼  Workers",        "Increases oven capacity"),
        ("quality",    "⭐  Quality",         "+15% pizza price per level"),
        ("marketing",  "📢  Marketing",       "+10% pizza price per level"),
        ("storage",    "📦  Storage",         "Unlocks more pizza recipes"),
        ("delivery",   "🚚  Delivery",        "+$2 bonus per pizza per level"),
        ("recipe",     "📖  Recipe Mastery",  "+20% custom pizza value"),
        ("loyalty",    "🎁  Loyalty",         "+5% double-earnings chance"),
    ]

    def _refresh_shop(self) -> None:
        gs = self.game_state
        self._lbl_shop_money.config(text=f"💰 ${gs['money']:,}")

        inner = self._shop_inner
        for w in inner.winfo_children():
            w.destroy()

        row_f: tk.Frame | None = None
        for idx, (key, name, desc) in enumerate(self.UPGRADES):
            if idx % 2 == 0:
                row_f = tk.Frame(inner, bg=C_BG)
                row_f.pack(fill="x", padx=10, pady=4)

            level   = gs.get(f"{key}_level", 1)
            max_lv  = UPGRADE_MAX[key]

            card = tk.Frame(row_f, bg=C_CARD, relief="ridge", bd=2,
                            padx=12, pady=10)
            card.pack(side="left", fill="both", expand=True, padx=4)

            tk.Label(card, text=name, font=("Arial", 12, "bold"),
                     bg=C_CARD, fg=C_GOLD).pack(anchor="w")
            tk.Label(card, text=desc, font=("Arial", 9),
                     bg=C_CARD, fg=C_GREY, wraplength=200).pack(anchor="w")
            tk.Label(card, text=f"Level {level} / {max_lv}",
                     font=("Arial", 10), bg=C_CARD, fg=C_WHITE).pack(
                anchor="w", pady=2)

            if level >= max_lv:
                tk.Label(card, text="⭐  MAXED OUT!",
                         font=("Arial", 11, "bold"),
                         bg=C_CARD, fg=C_GOLD).pack()
            else:
                cost = UPGRADE_COSTS[key].get(level + 1, 99999)
                affordable = gs["money"] >= cost
                self._btn(
                    card,
                    f"Upgrade  —  ${cost}",
                    lambda k=key, c=cost: self._upgrade(k, c),
                    bg="#27AE60" if affordable else C_DKGREY,
                    state="normal" if affordable else "disabled",
                ).pack(pady=4)

    def _upgrade(self, key: str, cost: int) -> None:
        gs = self.game_state
        if gs["money"] < cost:
            messagebox.showwarning("Not Enough Money",
                                   f"You need ${cost} for this upgrade!")
            return
        gs["money"] -= cost
        gs[f"{key}_level"] = gs.get(f"{key}_level", 1) + 1
        self._toast(f"✅ {key.title()} upgraded to level {gs[f'{key}_level']}!")
        self._refresh_shop()

    # ─────────────────────────────────────────────────────────────────────────
    # GAME LOGIC HELPERS
    # ─────────────────────────────────────────────────────────────────────────

    def _pizza_price(self, pizza: dict) -> int:
        gs = self.game_state
        mult = (1.0
                + (gs["quality_level"]   - 1) * 0.15
                + (gs["marketing_level"] - 1) * 0.10)
        return int(pizza["price"] * mult)

    def _bake_time(self, base_time: int) -> int:
        gs = self.game_state
        reduction = (gs["oven_level"] - 1) * 0.30
        return max(2, int(base_time * (1 - reduction)))

    def _oven_cap(self) -> int:
        return min(6, 1 + self.game_state["workers_level"])

    # ─────────────────────────────────────────────────────────────────────────
    # TIMER LOOP (updates oven countdown every 500 ms)
    # ─────────────────────────────────────────────────────────────────────────

    def _start_timer(self) -> None:
        if self._timer_job:
            self.root.after_cancel(self._timer_job)
        self._tick()

    def _tick(self) -> None:
        if not self.game_state.get("game_running"):
            return
        elapsed = int(time.time() - self.game_state["session_start"])
        self._lbl_time.config(text=f"⏱️ {elapsed}s")
        self._refresh_oven_labels()
        self._timer_job = self.root.after(500, self._tick)

    # ─────────────────────────────────────────────────────────────────────────
    # GAME START / SAVE / LOAD
    # ─────────────────────────────────────────────────────────────────────────

    def _start_new_game(self) -> None:
        self.game_state = self._default_state()
        self.game_state["game_running"] = True
        self.game_state["session_start"] = time.time()
        self._show_screen("game")
        self._start_timer()

    def _open_custom(self) -> None:
        self.custom_state = {"base": "thin", "sauce": "tomato", "toppings": []}
        self._show_screen("custom")

    def _save_game(self) -> None:
        state_to_save = {
            k: v for k, v in self.game_state.items()
            if k != "ovens"  # oven timers are wall-clock, don't persist
        }
        state_to_save["ovens"] = []
        try:
            with open(SAVE_FILE, "w") as fh:
                json.dump(state_to_save, fh, indent=2)
            self._toast("💾 Game saved!")
        except OSError as exc:
            messagebox.showerror("Save Error", str(exc))

    def _load_game(self) -> None:
        if not os.path.exists(SAVE_FILE):
            messagebox.showinfo("Load Game", "No save file found.")
            return
        try:
            with open(SAVE_FILE) as fh:
                data = json.load(fh)
            self.game_state = self._default_state()
            self.game_state.update(data)
            self.game_state["game_running"] = True
            self.game_state["session_start"] = time.time()
            self.game_state["ovens"] = []
            self._show_screen("game")
            self._start_timer()
            self._toast("📂 Game loaded!")
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Load Error", str(exc))

    # ─────────────────────────────────────────────────────────────────────────
    # INSTRUCTIONS
    # ─────────────────────────────────────────────────────────────────────────

    def _show_instructions(self) -> None:
        messagebox.showinfo(
            "How to Play — Patel's Pizzas",
            "Welcome to Patel's Pizzas!\n\n"
            "MENU PIZZAS\n"
            "• Click 'Bake' on any pizza to start baking it.\n"
            "• When it's done, click the green oven slot to sell it.\n"
            "• Upgrades in the Shop increase prices and speed.\n\n"
            "CUSTOM PIZZA BUILDER\n"
            "• Pick a base, sauce and up to 6 toppings.\n"
            "• Watch the live preview update as you choose!\n"
            "• Click 'Make My Pizza!' to see an animated\n"
            "  step-by-step making sequence.\n"
            "• Sell menu pizzas to unlock premium toppings.\n\n"
            "UPGRADES\n"
            "• Oven  — faster baking\n"
            "• Workers — more oven slots\n"
            "• Quality / Marketing — higher sell prices\n"
            "• Storage — more menu recipes\n"
            "• Delivery — bonus $$ per sale\n"
            "• Recipe Mastery — custom pizza value\n"
            "• Loyalty — chance to double earnings\n\n"
            "Save your progress anytime with the Save button. Good luck!"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # UI HELPERS
    # ─────────────────────────────────────────────────────────────────────────

    def _btn(self, parent: tk.Widget, text: str, command,
             bg: str = C_BANNER, fg: str = C_WHITE,
             font: tuple = ("Arial", 11),
             state: str = "normal",
             pady: int = 5) -> tk.Button:
        return tk.Button(parent, text=text, command=command,
                         font=font, bg=bg, fg=fg,
                         relief="flat", padx=12, pady=pady,
                         cursor="hand2" if state == "normal" else "arrow",
                         activebackground=bg,
                         state=state)

    def _opt_btn(self, parent: tk.Widget, text: str, command,
                 selected: bool = False, width: int = 11) -> tk.Button:
        bg = C_GOLD if selected else "#3D1A08"
        fg = "#1A0A00" if selected else C_WHITE
        return tk.Button(parent, text=text, command=command,
                         font=("Arial", 9), bg=bg, fg=fg,
                         relief="flat", padx=5, pady=5,
                         cursor="hand2", width=width,
                         wraplength=88, justify="center",
                         activebackground=C_GOLD)

    def _stat_lbl(self, parent: tk.Widget, text: str) -> tk.Label:
        lbl = tk.Label(parent, text=text, font=("Arial", 12, "bold"),
                       bg=C_BANNER, fg=C_GOLD)
        lbl.pack(side="left", padx=18)
        return lbl

    def _section_header(self, parent: tk.Widget, text: str) -> None:
        tk.Label(parent, text=text, font=("Arial", 12, "bold"),
                 bg=C_CARD, fg=C_GOLD).pack(
            anchor="w", padx=10, pady=(12, 4))

    def _toast(self, message: str, duration: int = 2800) -> None:
        """Show a temporary popup notification."""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        lbl = tk.Label(toast, text=message,
                       font=("Arial", 11, "bold"),
                       bg="#1A3A1A", fg="#4CAF50",
                       padx=18, pady=10)
        lbl.pack()
        self.root.update_idletasks()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        tw = lbl.winfo_reqwidth() + 36
        th = lbl.winfo_reqheight() + 20
        toast.geometry(f"{tw}x{th}+{rx + (rw - tw) // 2}+{ry + rh - th - 70}")
        toast.after(duration, toast.destroy)


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main() -> None:
    root = tk.Tk()
    # Try to set a nicer font on Linux
    try:
        root.option_add("*Font", "Arial 10")
    except Exception:
        pass
    _app = PatelsPizzasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

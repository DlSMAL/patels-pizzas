# 🍕 Patel's Pizzas

A pizza restaurant game — now as a Python desktop app!

## Features

- **Restaurant background** — brick walls, hanging lights, wooden counter and a glowing oven
- **Live pizza preview** — watch your pizza build in real-time as you pick toppings
- **Animated pizza making** — step-by-step canvas animation: dough → sauce → each topping → oven → done!
- **Menu pizzas** — bake and sell 10 different recipes with real-time countdown timers
- **Upgrade Shop** — improve your oven, hire workers, boost quality, marketing, delivery and more
- **Topping unlock system** — sell enough menu pizzas to unlock premium toppings
- **Save / Load** — your progress is saved to `~/.patels_pizzas_save.json`

## Requirements

- Python 3.8 or later
- `tkinter` (usually bundled with Python; on Ubuntu/Debian install with `sudo apt install python3-tk`)

## How to Run

```bash
python pizza_app.py
```

## How to Play

### Menu Pizzas
1. Click **Bake** on any pizza card to start baking (costs money + time).
2. Once done the oven slot turns green — click it to sell and collect your money.
3. Upgrade your **Workers** to unlock more oven slots.

### Custom Pizza Builder
1. Click **🍕 Custom Pizza** from the game screen.
2. Choose a **base**, **sauce**, and up to **6 toppings**.
3. Watch the live pizza canvas update as you make selections.
4. Click **Make My Pizza!** to launch the step-by-step animation.
5. Sell menu pizzas to unlock higher-tier toppings.

### Upgrades
| Upgrade | Effect |
|---|---|
| 🔥 Oven | −30% bake time per level |
| 👨‍💼 Workers | +1 oven slot per level |
| ⭐ Quality | +15% sell price per level |
| 📢 Marketing | +10% sell price per level |
| 📦 Storage | Unlocks more menu recipes |
| 🚚 Delivery | +$2 bonus per sale per level |
| 📖 Recipe Mastery | +20% custom pizza value |
| 🎁 Loyalty | +5% chance of double earnings |

## Credits

Rizwan Waseem × Ali Imran  
© 2026 All Rights Reserved

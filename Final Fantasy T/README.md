# Final Fantasy T (Terminal JRPG)

A tiny terminal JRPG battle vignette with chunky ASCII art, HP/MP bars, items, magic, and a **two-phase boss fight**. Built for fun and tinkering.

## ✨ Highlights
- **Party of 3** (Swordsman, Mage, Assassin) vs **Fiend + Imp + Bahamut**
- **Phase 2:** Bahamut resurrects as **BAHAMUT ZERO**
- **ASCII sprites** for heroes & enemies; **fire overlay** on fallen heroes
- **HP/MP bars** and tidy right/left battlefield layout

---

## 🚀 Requirements
- **Python 3.8+**
- Standard library only (no external packages required)
- A terminal that can show **≥120 columns** (148 recommended) for best ASCII alignment

> **Tips:**  
> Windows → use Windows Terminal/PowerShell with a monospace font (e.g., Cascadia Mono).  
> macOS/Linux → Terminal/iTerm/kitty/Alacritty all work great.

---

## 🧩 Project Layout

> - Main.py     →   # game loop, sprites, UI, battle flow, modes  
> - Mechanics.py →  # Person class (HP/MP, damage, actions)  
> - Magic.py  → # Spell class + damage formulas  
> - Inventory.py  → # Item class + item effects  


---

## ▶️ Run

From the project folder:
```bash
> python3 Main.py
```
---

## Optional Flags

- `--ezwin` – Adds **OMNISLASH** as option 4 for the **Swordsman**. One use clears all current enemies (great for skipping to Phase 2 or testing).

- `--unwinnable` – After the first player phase, **Bahamut** uses **GIGAFLARE (OHKO MOVE)** and wipes the party.  
  *(Note: `--ezwin` takes precedence if both are provided.)*

### Examples

```bash
# Normal game
python Main.py

# Give Swordsman Omnislash (auto-win current phase)
python3 Main.py --ezwin

# Guaranteed loss after first round (Gigaflare)
python3 Main.py --unwinnable

# If you pass both, ezwin wins:
python3 Main.py --unwinnable --ezwin
```

---
## 🎮 How to Play

Each round has two phases.

### 🧝 Player Phase

Each living hero takes a turn:

- **Attack** – Single-target physical damage  
- **Magic** –  
  - Black magic (Fire, Thunder, Blizzard, Meteor, Twister…) deals damage  
  - White magic (Cura, Recover) heals  
- **Items** – Potions, Elixers, Grenades, Phoenix Down / Mega Phoenix (revive)

---

### 👹 Enemy Phase

Each living enemy acts:

- Enemies always deal damage via a physical move or black magic  
- In Phase 2, **Bahamut ZERO** occasionally casts **MEGAFLARE (AOE)** when off cooldown  

**Controls:**  
Type the number for your choice and press Enter.  
Invalid inputs will reprompt.

---

## 🐉 Boss Phases

### Phase 1
You fight **Fiend**, **Imp**, and **Bahamut** together.  
Defeat them all to trigger Phase 2.

### Phase 2 – BAHAMUT ZERO
Bahamut returns as **BAHAMUT ZERO**.  
- Has a chance (~30% by default) to use **MEGAFLARE (AOE SKILL)** when off cooldown (3 rounds).  
- Uses aggressive black magic and heavy physicals otherwise.

**Win/Lose Conditions**  
- Defeat Bahamut ZERO →  **YOU WIN**  
- Party wiped (or `--unwinnable` Gigaflare) →  **YOU LOSE** 

---

## 🧯 Items & Revives

| Item | Effect |
|------|---------|
| Potion / Super Potion / Max Potion | Heal fixed HP |
| Elixer / Mega-Elixer | Restore HP/MP (single target or whole party) |
| Grenade | Fixed damage to a single enemy |
| Phoenix Down | Revives one ally to 50% HP |
| Mega Phoenix | Revives all allies to 50% HP |

---

## ⚙️ Tuning & Modding

You can tweak most balance and visuals in **Main.py**:

- **Bahamut ZERO behavior**  
  - Chance to AOE: `bz.megaflare_chance = 0.30`  
  - Cooldown: `bz.megaflare_cd = 3`  
  - Stats: in `spawn_bahamut_zero()`  
- **Enemy physical move names:** `PHYS_MOVES` dictionary  
- **Hero/Enemy base stats:** inside `Person(...)` initializers  
- **Spells/Items:** add or modify in `Magic.py` and `Inventory.py`, then register in `Main.py`  
- **ASCII Layout:** edit `HERO_SPRITES`, `ENEMY_SPRITES`, or alignment in `compose_battlefield(...)`  
- **HP/MP bar widths:** adjust `bar(..., width=18)` for HP and `width=10` for MP  

---

## 🧪 Special Modes

### `--ezwin` (Omnislash Test Mode)
Gives **Swordsman** an extra menu option `(4. OMNISLASH)`.  
Instantly defeats all current enemies (perfect for skipping to Phase 2 or testing Bahamut ZERO).

### `--unwinnable` (Gigaflare Wipe Mode)
After the first player phase, **Bahamut** casts **GIGAFLARE**, annihilating the party.  
Displays the **YOU LOSE** ASCII banner.  
If both `--unwinnable` and `--ezwin` are passed, `--ezwin` takes precedence so you can still test.

---

## 🖼️ ASCII & UI Notes

- The battlefield clears and reprints after each round  
- Fallen heroes are replaced with a small flame animation  
- Use a terminal width of ≥120 columns (ideally **148**) for best results  
- If your ASCII looks misaligned, switch to a monospace font (e.g., Consolas, Cascadia Mono)

---

## 🛠️ Troubleshooting

- **Art misalignment / wrapping** → Widen your terminal or reduce font size slightly.  
- **Input skipped / instant skip** → Try another terminal or add a small `time.sleep()` after prompts.  

---

## 📜 License & Credits

- Game designed & developed by **Alexrkh**
- ASCII art taken from public resources online and modified to suit the **FF** vibe
- Released under the **MIT License** 

> **Disclaimer:**  
> This project is a **non-commercial fan-made tribute** inspired by *Final Fantasy*.  
> All characters, names, spells, and other references to *Final Fantasy* are the **intellectual property of Square Enix Co., Ltd.**  
> This work is not affiliated with, endorsed by, or approved by Square Enix.  
>  
> The name “Final Fantasy T (Terminal JRPG)” is used purely for **parody, educational, and non-profit purposes.**  
> Please support the official games.

---

## 📝 Notes

- Game is currently **Not Balanced** → you are going to lose playing this game
    - Modify the game as instructed in ***⚙️ Tuning & Modding*** to make the game more fair
## 🗺️ Roadmap (Ideas)

- Status effects (Poison, Blind, Regen)  
- Multi-target black magic (“All” cast options)  
- Speed-based initiative system (ATB-style)  
- More encounters & a tiny overworld menu  
- Save best times / damage logs  

## Enjoy!!!

                                                 ╓<≈w                        
                                                   ╠╫µ▄╬▓                       
                                                    ▓Ñ╣▓Ñ                       
                                                    ▓▓▒╣w                       
     ,  .;,,`                         ,,,           ▓ÑH╫M                       
     ╟▐▓^*┴╫Ñ                     ║╣▓╨╙>╫─      ,▄╓;▓╣M▓▄µ,;w                   
     ╟▐╫   ⌠,,.,,  ,,       ,,,   ║▐╫   `    ,,╚▓Å"╠▓▌▓▓▓╙"╨   ,╓µ,,,,  .µ,     
     ╟▐╫   $╫▌ ▓╫w ╟▓  ▒▓▄  B╫Ñ   ║j╫   ╠╫▓  ▐▒▌ .ΦH╣╣▓█` Æ╫▌ Ä▓``╫║╙▓  j║┴     MMP""MM""YMM
     ╠▐▓▄▄▄$╫▌ ╬╜▓▄╟▌ ╓▓▐▓  b╫Γ   ║j╫╓▄µ╫▌╫░ ▐▌\\▀▓▓ ╟╬▓▓ ▐Φb╫H ╚▀▓w ╙J▓╓╣`          MM
     ╠j╣   L╫▌ ╢.`U╫▌ ╬▀É╫L H╫M   ║▐╫  ▐▓▀╨╫ ▐▌ )╠▓ ║░▓▌ £▌║╙▌  `Ü▀φ V╫▓M            MM
     ⌡j╫   $╫▌ ╢   @▌,╫─╞╠▓ H╫M   ║▐╫  £▌ ⌐╫H▐▌  ╠╣ ║½▓▌ M⌐"»╫'   H▓  ╨▓             MM
     ⌡j╫   P╫▌ ╢`  |▌╠▓ "]▓⌐H╫M   ▐▐╫  ╣⌐ Ü╢▌▐▌   ╢ ▐'█▌.╫  W╢▌   N▌ ⁿ]╫             MM
     ⌡]╣   ÑÅ▌~▀K  $ÑÑ▌ »Ñ▀WÑ▀▀Φ▀ ║▐╫ «▀⌐ ╧╩▀╝▌   Å ▐ ▓▌╝▀  ╩╝╝ßΦÅ╙  ╙;╫           .JMML.
     ⌡╟▓                          ║▐▓                 ▓▌             J»▓             
     ╠╟▓                          ║▐▓⌐               ▄█▌             ▐è▓            2.0
     ▄╨`                          ║╝`                ▓█▌               ╙        
                                                     ╫▌H                                               
                                                     ╫▓                         
                                                     ║▓                         
                                                     "▀       
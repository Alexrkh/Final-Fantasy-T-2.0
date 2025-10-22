import argparse
import random
import sys
import os
import time

# Try to ensure Unicode-friendly stdout (helps your banner on Windows)
try:
    sys.stdout.reconfigure(encoding='utf-8')  # Python 3.7+
except Exception:
    pass

from Inventory import Item
from Magic import Spell
from Mechanics import Person

# ---------------- YOUR BANNER (kept verbatim) ----------------
TITLE = """
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
"""

# ---------------- Hero ASCII ----------------
HERO_SPRITES = {
    "Swordsman": [
        "      k",
        "   O  |",
        " ()Y==o",
        "  /_\\ |",
        "  _W_ |",
    ],
    "Mage": [
        "   _/\\_",
        "  ( . .)",
        "  /_||_\\",
        "  \\_()_/",
        "   |__|",
    ],
    "Assassin": [
        "  o",
        " |\\O   )",
        "  \\Y==d",
        "  /_\\",
        "  / >",
    ],
}

# ---------------- Enemy ASCII (Phase 1) ----------------
_BAHAMUT_BLOCK = r"""
                               /|
            .==.        .==.   //
           //`^\\      //^`\\ //
          // ^ ^\(\__/)/^ ^^\//
         //^ ^^ ^/6  6\ ^^ ^//\
        //^ ^^ ^/( .. )\^ _// \\
       // ^^ ^/\| v""v |/@@@) ^\\
      // ^^/\/ /  `~~`   @"/\^ ^\\
      \\^ /  _/  /IIII. \_/  \^ //
       \\/  /(  (IIIIII/  \   \//
        ^  /  \  \IIII'    \   ^
           \  ((((`II'     /
         .--'  /\_____/\  `--.
        ((((--'         '--))))
"""
BAHAMUT_SPRITE = _BAHAMUT_BLOCK.splitlines()[1:]

FIEND_SPRITE = [
    "  .--.   ",
    " (_^_^_) ",
    " / __ \\  ",
    " \\_)(_/  ",
]

IMP_SPRITE = [
    "  _^^_   ",
    " (o__o)  ",
    " /|  |\\  ",
    "  /__\\   ",
]

# ---------------- Bahamut ZERO (Phase 2) — YOUR FINAL ART ----------------
_BAHAMUT_ZERO_BLOCK = r"""
                                                 /===-_---~~~~~~~~~------____
                                                |===-~___                _,-'
                 -==\\                         `//~\\   ~~~~`---.___.-~~
             ______-==|                         | |  \\           _-~`
       __--~~~  ,-/-==\\                        | |   `\        ,'
    _-~       /'    |  \\                      / /      \      /
  .'        /     -==\\ \\                   /' /       /===-_---~~~~~~~~~------__
 /  ____  /   ______-==| \\ .__/-~~ ~ \ _ _/'  /      `//~\\   ~~~~`---.___.-~~
/-'~     __--~~ ,-/-==\\    /           ( )   /'       | |  \\           _-~`
      _-~       /'\_|  \\  /        _)   ;  ),   __--~| | ` \        ,'~
    .'        /     '~~--_/      _-~/-  / \   '-~ \  / /     \     / 
   /  ____  /-==\\ {\__--_/}    / \\_>- )<__\   /===-_---~~~~~~~~~------____
  /-'~      ______ /'   (_/  _-~  | |__>--<__|===-~___                _,-'
       .'        /|0  0 _/) )-~-- | |__>--<`//~ \\   ~~~~`---.___.-~~
      /  ____  /  / /~ ,_/       / /__>---<__/ / \\          _-~`
     /-'~   ~~~~ o o _//      ~-/-~_>---<__-/' /  \\       /'    
                 (^(~  \_|     /~_>---<__/'  /      \     /' 
                ,/|    '~~--_ /__>--<__/    ), _____--~  / 
             ,//('(          |__>--<__|     /                  .----_
            ( ( '))          |__>--<__|    |                 /' _---_~\
         `-)) )) (           |__>--<__|    |               /'  /     ~\`\
        ,/,'//( (             \__>--<__\    \            /'  //        ||
      ,( ( ((, ))              ~-__>--<_~-_  ~--____---~' _/'/        /' 
    `~/  )` ) ,/|                 ~-_~>--<_/-__       __-~ _/
  ._-~//( )/ )) `                    ~~-'_/_/ /~~~~~~~__--~
   ;'( ')/ ,)(                              ~~~~~~~~~~
  ' ') '( (/
    '   '  `
"""
BAHAMUT_ZERO_SPRITE = _BAHAMUT_ZERO_BLOCK.splitlines()[1:]

# ---------------- Enemy sprite registry ----------------
def name_key_for_enemy(name_label):
    base = name_label.strip(" :")
    if base.startswith("Bahamut ZERO"): return "BahamutZERO"
    if base.startswith("Bahamut"):      return "Bahamut"
    if base.startswith("Fiend"):        return "Fiend"
    if base.startswith("Imp"):          return "Imp"
    return "Fiend"

ENEMY_SPRITES = {
    "Bahamut": BAHAUMUT_SPRITE if 'BAHAUMUT_SPRITE' in globals() else BAHAMUT_SPRITE,  # safety
    "BahamutZERO": BAHAMUT_ZERO_SPRITE,
    "Fiend": FIEND_SPRITE,
    "Imp": IMP_SPRITE,
}

# ------------- Fire animation frames (used for Gigaflare & KO overlay) -------------
FIRE_FRAMES = [
    [
        "   (  )   ",
        "   )\\/(   ",
        "  ( /\\ )  ",
        "   /  \\   ",
    ],
    [
        "    ) (    ",
        "   ( /\\)   ",
        "    \\/ (   ",
        "    /  \\   ",
    ],
    [
        "    ( )    ",
        "    (\\/    ",
        "    /\\)    ",
        "    /  \\   ",
    ],
]

# ---------------- ASCII-only Victory/Defeat (mono-safe) ----------------
VICTORY = r"""
 __     __          __          ___         _ 
 \ \   / /          \ \        / (_)       | |
  \ \_/ /__  _   _   \ \  /\  / / _ _ __   | |
   \   / _ \| | | |   \ \/  \/ / | | '_ \  | |
    | | (_) | |_| |    \  /\  /  | | | | | |_|
    |_|\___/ \__,_|     \/  \/   |_|_| |_| |_|
"""
DEFEAT = r"""
  _____       __           _   
 |  __ \     / _|         | |  
 | |  | | __| |_ ___  __ _| |_ 
 | |  | |/ _`  _/ _ \/ _` | __|
 | |__| | __| ||  __/ (_| | |_ 
 |_____/ \__,_| \___|\__,_|\__|
"""

# ---------------- Helpers: input, screen, rendering ----------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner(text):
    print("\n" + "=" * 75)
    print(text.center(75))
    print("=" * 75 + "\n")

def show_title():
    banner("FINAL FANTASY T")
    print(TITLE)

def name_key_for_hero(name_label):
    base = name_label.strip(" :")
    if base.startswith("Swordsman"): return "Swordsman"
    if base.startswith("Mage"):      return "Mage"
    if base.startswith("Assassin"):  return "Assassin"
    return "Swordsman"

def pad_right(s, width):
    return s + " " * max(0, width - len(s))

def stack_sprites(lines_list):
    out = []
    for sprite in lines_list:
        out.extend(sprite)
        out.append("")  # gap
    if out and out[-1] == "": out.pop()
    return out

def bar(current, maximum, width=18, fill='█', empty=' '):
    ratio = 0.0 if maximum <= 0 else max(0.0, min(1.0, current / float(maximum)))
    ticks = int(round(width * ratio))
    return fill * ticks + empty * (width - ticks)

def compose_battlefield(players, enemies, left_width=32, gap=6, fire_for=None, fire_frame=None):
    if fire_frame is None and fire_for:
        fire_frame = FIRE_FRAMES[0]

    left_sprites = []
    for p in players:
        key = name_key_for_hero(p.name)
        if p.get_hp() > 0:
            left_sprites.append([f"{p.name.strip()}"])
            left_sprites.append(HERO_SPRITES[key])
            hp_line = f"HP {p.hp}/{p.maxhp} [{bar(p.hp, p.maxhp)}]"
            mp_line = f"MP {p.mp}/{p.maxmp} [{bar(p.mp, p.maxmp, width=10)}]"
            left_sprites.append([hp_line])
            left_sprites.append([mp_line])
            left_sprites.append([""])
        else:
            frame = fire_frame if (fire_for == "players" and fire_frame) else FIRE_FRAMES[0]
            left_sprites.append([f"{p.name.strip()} (defeated)"])
            left_sprites.append(frame)
            left_sprites.append([""])

    right_sprites = []
    for e in enemies:
        key = name_key_for_enemy(e.name)
        if e.get_hp() > 0:
            right_sprites.append([f"{e.name.strip()}"])
            right_sprites.append(ENEMY_SPRITES[key])
            hp_line = f"HP {e.hp}/{e.maxhp} [{bar(e.hp, e.maxhp)}]"
            mp_line = f"MP {e.mp}/{e.maxmp} [{bar(e.mp, e.maxmp, width=10)}]"
            right_sprites.append([hp_line])
            right_sprites.append([mp_line])
            right_sprites.append([""])
        else:
            pass  # dead enemies hidden

    left_block = stack_sprites([s if isinstance(s, list) else [s] for s in left_sprites]) or [""]
    right_block = stack_sprites([s if isinstance(s, list) else [s] for s in right_sprites]) or [""]

    H = max(len(left_block), len(right_block))
    left_block += [""] * (H - len(left_block))
    right_block += [""] * (H - len(right_block))

    lines = []
    for i in range(H):
        L = pad_right(left_block[i], left_width)
        R = right_block[i]
        lines.append(L + " " * gap + R)
    return lines

def render_round(players, enemies, round_no, fire_for=None, fire_frame=None):
    clear_screen()
    show_title()
    print(f"Round {round_no}")
    print("\nBattlefield:\n")
    for line in compose_battlefield(players, enemies, fire_for=fire_for, fire_frame=fire_frame):
        print(line)
    print("\n")

def pause_after_enemy():
    try:
        input("\n[Enemy phase complete] Press Enter to continue...")
    except EOFError:
        time.sleep(1.2)

def prompt_choice(label, lo, hi):
    while True:
        try:
            v = int(input(label))
            if lo <= v <= hi:
                return v
            print(f"Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("Please enter a valid number.")

def prompt_index(max_count, label="   Choose: "):
    return prompt_choice(label, 1, max_count) - 1

# --- End screen helper: prints only the big ASCII banner ---
def show_end(result):
    clear_screen()
    show_title()
    if result == "win":
        print(VICTORY)
    else:
        print(DEFEAT)

# ---------------- Spells & Items ----------------
# Black Magic
fire    = Spell("Fire",    25, 200, "black")
thunder = Spell("Thunder", 25, 200, "black")
blizzard= Spell("Blizzard",25, 200, "black")
meteor  = Spell("Meteor",  40, 500, "black")
quake   = Spell("Quake",   14, 140, "black")
twister = Spell("Twister", 50,1000, "black")

# White Magic
cura    = Spell("Cura",    25, 220, "white")
recover = Spell("Recover", 32,1500, "white")

# Items
potion        = Item("Potion",        "potion", "Heals 50 HP",                  50)
superpotion   = Item("Super Potion",  "potion", "Heals 100 HP",                100)
maxpotion     = Item("Max Potion",    "potion", "Heals 500 HP",                500)
elixer        = Item("Elixer",        "elixer", "Fully restores one ally",    9999)
megaelixer    = Item("Mega-Elixer",   "elixer", "Fully restores the party",   9999)
grenade       = Item("Grenade",       "attack", "Deals 500 damage",            500)
phoenix_down  = Item("Phoenix Down",  "revive", "Revives one ally to 50% HP",   50)  # percent
mega_phoenix  = Item("Mega Phoenix",  "revive_all", "Revives all allies to 50% HP", 50)

player_spells = [fire, thunder, blizzard, meteor, cura, recover]
enemy_spells  = [fire, meteor, cura, twister]
player_items  = [
    {"item": potion,        "quantity": 5},
    {"item": superpotion,   "quantity": 4},
    {"item": maxpotion,     "quantity": 2},
    {"item": elixer,        "quantity": 2},
    {"item": megaelixer,    "quantity": 1},
    {"item": phoenix_down,  "quantity": 3},
    {"item": mega_phoenix,  "quantity": 1},
    {"item": grenade,       "quantity": 2},
]

# ---------------- Parties (Phase 1) ----------------
player1 = Person("Swordsman  :", 1160, 100, 300, 34, player_spells, list(player_items))
player2 = Person("Mage       :", 1110, 300, 100, 34, player_spells, list(player_items))
player3 = Person("Assassin   :", 1000, 150, 150, 34, player_spells, list(player_items))

enemy1 = Person("Fiend :",   1250,  90, 100, 20, enemy_spells, [])
enemy2 = Person("Bahamut:", 12000, 200, 200, 50, enemy_spells, [])  # boss
enemy3 = Person("Imp   :",   1250, 100,  90, 20, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

# ---------------- Enemy AI helpers ----------------
PHYS_MOVES = {
    "Bahamut": ["Tail Swipe", "Claw Smash", "Wing Buffet"],
    "Fiend":   ["Vicious Slash", "Savage Strike", "Rend"],
    "Imp":     ["Cackle Jab", "Needle Poke", "Nuisance Nip"],
    "Bahamut ZERO": ["Void Rake", "Gravity Claw", "Aether Rend"],
}

def enemy_use_physical(enemy, players):
    base = "Bahamut ZERO" if enemy.name.strip().startswith("Bahamut ZERO") else \
           "Bahamut" if enemy.name.strip().startswith("Bahamut") else \
           "Fiend" if enemy.name.strip().startswith("Fiend") else "Imp"
    move = random.choice(PHYS_MOVES.get(base, ["Strike"]))
    targets = [p for p in players if p.get_hp() > 0]
    if not targets:
        return
    target = random.choice(targets)
    dmg = enemy.generate_damage()
    target.take_damage(dmg)
    print(f"{enemy.name.strip()} uses {move} on {target.name.strip()} for {dmg} damage.")

def enemy_use_spell(enemy, players):
    dmg_spells = [s for s in enemy.magic if s.type == "black" and enemy.get_mp() >= s.cost]
    if not dmg_spells:
        return False
    spell = random.choice(dmg_spells)
    enemy.reduce_mp(spell.cost)
    dmg = spell.generate_damage()
    targets = [p for p in players if p.get_hp() > 0]
    if not targets:
        return True
    target = random.choice(targets)
    target.take_damage(dmg)
    print(f"{enemy.name.strip()} casts {spell.name} on {target.name.strip()} for {dmg} damage.")
    return True

# ---------------- Bahamut ZERO special: MEGAFLARE ----------------
def ensure_bz_fields(bz):
    if not hasattr(bz, "megaflare_cd"):
        bz.megaflare_cd = 1           # slight delay before first chance
    if not hasattr(bz, "megaflare_chance"):
        bz.megaflare_chance = 0.30    # 30% when off cooldown

def bahamut_zero_take_turn(bz, players):
    """Bahamut ZERO AI: occasional AOE MEGAFLARE with cooldown, else aggressive action."""
    ensure_bz_fields(bz)

    # tick cooldown
    if bz.megaflare_cd > 0:
        bz.megaflare_cd -= 1

    # Try MEGAFLARE
    if bz.megaflare_cd == 0 and random.random() < bz.megaflare_chance:
        print("Bahamut ZERO gathers cosmic energy...")
        time.sleep(0.8)
        print("MEGAFLARE!!!")
        for p in [x for x in players if x.get_hp() > 0]:
            base = int(bz.generate_damage() * 0.9) + random.randint(180, 260)
            p.take_damage(base)
            print(f"  {p.name.strip()} takes {base} damage!")
        bz.megaflare_cd = 3  # 3-turn cooldown
        return

    # Otherwise, normal aggression (spell if possible, else physical)
    dmg_spells = [s for s in bz.magic if s.type == "black" and bz.get_mp() >= s.cost]
    if dmg_spells and random.random() < 0.6:
        if not enemy_use_spell(bz, players):
            enemy_use_physical(bz, players)
    else:
        enemy_use_physical(bz, players)

# ---------------- Utility ----------------
def all_dead(group):
    return all(x.get_hp() == 0 for x in group)

def choose_target_alive(group):
    return [g for g in group if g.get_hp() > 0]

# ---------------- Phase 2 (Bahamut ZERO) ----------------
def spawn_bahamut_zero():
    zero_spells = [fire, meteor, twister]  # aggressive kit
    bz = Person("Bahamut ZERO:", 18000, 400, 260, 70, zero_spells, [])
    bz.megaflare_cd = 1
    bz.megaflare_chance = 0.30
    return bz

def begin_phase2(players, enemies, round_no):
    print("\nThe ground trembles… Bahamut rises again as BAHAMUT ZERO!")
    bz = spawn_bahamut_zero()
    enemies[:] = [bz]  # replace in place
    time.sleep(1.2)
    render_round(players, enemies, round_no)

# ---------------- Game Start ----------------
def main():
    parser = argparse.ArgumentParser(description="Final Fantasy T")
    parser.add_argument("--unwinnable", action="store_true",
                        help="Bahamut wipes the party with Gigaflare after the first player phase.")
    parser.add_argument("--ezwin", action="store_true",
                        help="Swordsman gains OMNISLASH (option 4) that defeats all current enemies.")
    args = parser.parse_args()
    UNWINNABLE = args.unwinnable and not args.ezwin  # ezwin takes precedence
    EZWIN = args.ezwin

    round_no = 1
    PHASE = 1
    gigaflare_done = False

    render_round(players, enemies, round_no)

    while True:
        # ---------- Player Phase ----------
        for player in players:
            if player.get_hp() == 0:
                continue

            print(f"{player.name.strip()} turn.")
            if EZWIN and player.name.strip().startswith("Swordsman"):
                print("   1. Attack   2. Magic   3. Items   4. OMNISLASH")
                choice = prompt_choice("    Choose Action: ", 1, 4)
            else:
                print("   1. Attack   2. Magic   3. Items")
                choice = prompt_choice("    Choose Action: ", 1, 3)
            index = choice - 1

            if EZWIN and player.name.strip().startswith("Swordsman") and index == 3:
                living = [e for e in enemies if e.get_hp() > 0]
                if living:
                    print("\nSwordsman channels a thousand blades...")
                    time.sleep(0.6)
                    print("**OMNISLASH!!!**")
                    for e in living:
                        e.hp = 0
                    time.sleep(0.8)
                else:
                    print("No foes remain.")
            elif index == 0:  # Attack
                visible = [x for x in enemies if x.get_hp() > 0]
                if not visible:
                    break
                for i, e in enumerate(visible, start=1):
                    print(f"     {i}. {e.name.strip()}")
                sel = prompt_index(len(visible), "   Choose Target: ")
                target = visible[sel]
                dmg = player.generate_damage()
                target.take_damage(dmg)
                print(f"You attacked {target.name.strip()} for {dmg} damage.")
                if target.get_hp() == 0:
                    print(f"{target.name.strip()} has been defeated!")
            elif index == 1:  # Magic
                for i, sp in enumerate(player.magic, start=1):
                    print(f"     {i}. {sp.name} (cost: {sp.cost})")
                if not player.magic:
                    print("No spells available.")
                else:
                    magic_choice = prompt_index(len(player.magic), "    Choose Magic: ")
                    spell = player.magic[magic_choice]
                    magic_dmg = spell.generate_damage()
                    if spell.cost > player.get_mp():
                        print("Not enough MP.")
                    else:
                        player.reduce_mp(spell.cost)
                        if spell.type == "white":
                            player.heal(magic_dmg)
                            print(f"{spell.name} heals {magic_dmg} HP.")
                        else:
                            visible = [x for x in enemies if x.get_hp() > 0]
                            if not visible:
                                print("No valid targets.")
                            else:
                                for i, e in enumerate(visible, start=1):
                                    print(f"     {i}. {e.name.strip()}")
                                sel = prompt_index(len(visible), "   Choose Target: ")
                                target = visible[sel]
                                target.take_damage(magic_dmg)
                                print(f"{spell.name} deals {magic_dmg} to {target.name.strip()}.")
                                if target.get_hp() == 0:
                                    print(f"{target.name.strip()} has been defeated!")
            elif index == 2:  # Items
                if not player.items:
                    print("No items.")
                else:
                    for i, inv in enumerate(player.items, start=1):
                        print(f"     {i}. {inv['item'].name}: {inv['item'].description} x({inv['quantity']})")
                    item_choice = prompt_index(len(player.items), "    Choose Item: ")
                    inv = player.items[item_choice]
                    item = inv["item"]

                    if inv["quantity"] <= 0:
                        print(f"Out of {item.name}s!")
                    elif item.type == "potion":
                        player.heal(item.prop)
                        inv["quantity"] -= 1
                        print(f"{item.name} heals {item.prop} HP.")
                    elif item.type == "elixer":
                        inv["quantity"] -= 1
                        if item.name == "Mega-Elixer":
                            for i in players:
                                i.hp, i.mp = i.maxhp, i.maxmp
                        else:
                            player.hp, player.mp = player.maxhp, player.maxmp
                        print(f"{item.name} fully restores HP/MP.")
                    elif item.type == "attack":
                        visible = [x for x in enemies if x.get_hp() > 0]
                        if not visible:
                            print("No valid targets.")
                        else:
                            for i, e in enumerate(visible, start=1):
                                print(f"     {i}. {e.name.strip()}")
                            sel = prompt_index(len(visible), "   Choose Target: ")
                            target = visible[sel]
                            target.take_damage(item.prop)
                            inv["quantity"] -= 1
                            print(f"{item.name} deals {item.prop} damage to {target.name.strip()}.")
                            if target.get_hp() == 0:
                                print(f"{target.name.strip()} has been defeated!")
                    elif item.type == "revive":
                        fallen = [p for p in players if p.get_hp() == 0]
                        if not fallen:
                            print("No allies to revive.")
                        else:
                            for i, ally in enumerate(fallen, start=1):
                                print(f"     {i}. {ally.name.strip()} (KO)")
                            sel = prompt_index(len(fallen), "   Choose Ally to Revive: ")
                            ally = fallen[sel]
                            restore = max(1, int((item.prop / 100.0) * ally.maxhp))
                            ally.hp = min(ally.maxhp, restore)
                            inv["quantity"] -= 1
                            print(f"{item.name} revives {ally.name.strip()} to {ally.hp}/{ally.maxhp} HP!")
                    elif item.type == "revive_all":
                        any_ko = any(p.get_hp() == 0 for p in players)
                        if not any_ko:
                            print("No allies to revive.")
                        else:
                            for ally in players:
                                if ally.get_hp() == 0:
                                    restore = max(1, int((item.prop / 100.0) * ally.maxhp))
                                    ally.hp = min(ally.maxhp, restore)
                            inv["quantity"] -= 1
                            print(f"{item.name} revives the party!")

        # ----- Instant Gigaflare (unwinnable) after first player phase -----
        if UNWINNABLE and not gigaflare_done and round_no == 1:
            print("\nBahamut begins to glow with catastrophic power...")
            print("GIGAFLARE!!!")
            time.sleep(1.5)
            for h in players:
                h.hp = 0
            gigaflare_done = True
            for i in range(6):
                frame = FIRE_FRAMES[i % len(FIRE_FRAMES)]
                render_round(players, enemies, round_no, fire_for="players", fire_frame=frame)
                time.sleep(0.5)
            show_end("lose")
            return

        # ----- Phase transition check -----
        if not all_dead(players) and all_dead(enemies):
            if PHASE == 1:
                PHASE = 2
                begin_phase2(players, enemies, round_no)
            else:
                render_round(players, enemies, round_no)
                show_end("win")
                return

        if all_dead(players):
            render_round(players, enemies, round_no)
            show_end("lose")
            return

        # ---------- Enemy Phase ----------
        alive_before = {id(p) for p in players if p.get_hp() > 0}

        for enemy in enemies:
            if enemy.get_hp() == 0:
                continue

            if enemy.name.strip().startswith("Bahamut ZERO"):
                bahamut_zero_take_turn(enemy, players)
            else:
                # 50/50 between black-magic (if affordable) and physical
                dmg_spells = [s for s in enemy.magic if s.type == "black" and enemy.get_mp() >= s.cost]
                casted = False
                if dmg_spells and random.random() < 0.5:
                    casted = enemy_use_spell(enemy, players)
                if not casted:
                    enemy_use_physical(enemy, players)

        pause_after_enemy()

        # Flame flicker for newly dead heroes
        newly_dead = [p for p in players if p.get_hp() == 0 and id(p) in alive_before]
        if newly_dead:
            for i in range(3):
                frame = FIRE_FRAMES[i % len(FIRE_FRAMES)]
                render_round(players, enemies, round_no, fire_for="players", fire_frame=frame)
                time.sleep(0.25)

        # end-of-round
        round_no += 1
        render_round(players, enemies, round_no)


if __name__ == "__main__":
    main()

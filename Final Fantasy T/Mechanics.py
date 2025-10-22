import random

class Person:
    BAR_HP = 25
    BAR_MP = 10

    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= max(0, dmg - self.df)
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self): return self.hp
    def get_max_hp(self): return self.maxhp
    def get_mp(self): return self.mp
    def get_max_mp(self): return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost
        if self.mp < 0:
            self.mp = 0

    def choose_action(self):
        i = 1
        print(f"\n   {self.name}")
        print("   ACTIONS:")
        for item in self.actions:
            print(f"     {i}. {item}")
            i += 1

    def choose_magic(self):
        i = 1
        print("\n   MAGIC")
        for spell in self.magic:
            print(f"     {i}. {spell.name} (cost: {spell.cost})")
            i += 1

    def choose_item(self):
        i = 1
        print("\n   ITEMS")
        for item in self.items:
            print(f"     {i}. {item['item'].name}: {item['item'].description} x({item['quantity']})")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n   TARGET")
        living = []
        for enemy in enemies:
            if enemy.get_hp() > 0:
                print(f"     {i}. {enemy.name}")
                living.append(enemy)
                i += 1
        choice = int(input("   Choose Target: ")) - 1
        return enemies.index(living[choice])

    def _bar(self, current, maximum, width, fill_char="█"):
        ratio = (current / maximum) if maximum else 0
        ticks = int(ratio * width)
        return fill_char * max(0, ticks) + " " * (width - max(0, ticks))

    def get_enemy_stats(self):
        hp_bar = self._bar(self.hp, self.maxhp, 50)
        print("                          " + "_" * 50)
        print(f"{self.name}  {self.hp}/{self.maxhp}|{hp_bar}|")

    def get_stats(self):
        hp_bar = self._bar(self.hp, self.maxhp, self.BAR_HP)
        mp_bar = self._bar(self.mp, self.maxmp, self.BAR_MP)
        print("                         " + "_" * 23 + "            " + "_" * 10)
        print(
            f"{self.name}  {self.hp}/{self.maxhp}|{hp_bar}|   "
            f"{self.mp}/{self.maxmp}|{mp_bar}|"
        )

    def choose_enemy_spell(self):
        # simple AI: prefer damage unless hurt; ensure MP available
        choices = list(range(len(self.magic)))
        random.shuffle(choices)
        for idx in choices:
            spell = self.magic[idx]
            if self.mp < spell.cost:
                continue
            if spell.type == "white" and (self.hp / self.maxhp) > 0.5:
                continue
            dmg = spell.generate_damage()
            return spell, dmg
        # fallback: basic attack number returned as "damage"
        return None, self.generate_damage()

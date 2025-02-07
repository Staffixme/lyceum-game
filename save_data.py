import json
import os.path

import items


class Data:
    screen_size = tuple()

    def __init__(self):
        self.player_group = list()
        self.player_items = list()
        self.stage = 0

    def update_items(self):
        for i in self.player_items:
            if i.count < 1:
                self.player_items.remove(i)

    def set_leader(self, player):
        player.is_leader = True

    def add_item(self, item):
        if item not in self.player_items:
            print(f"Item {item.name} not in inventory")
            self.player_items.append(item)
        else:
            self.player_items[self.player_items.index(item)].count += 1
            print(f"Item {item.name} in inventory")

    def get_items(self):
        return self.player_items

    def set_screen_size(self, size):
        Data.screen_size = size

    @staticmethod
    def get_screen_size():
        return Data.screen_size

    @staticmethod
    def save_game(slot, inventory, stage, characters):
        serialized_inventory = list()
        serialized_characters = list()
        for i in inventory:
            item = dict()
            if type(i) is items.HealItem:
                item["class"] = "Heal"
            elif type(i) is items.AttackItem:
                item["class"] = "Attack"
            item["item_id"] = i.item_id
            item["count"] = i.count
            serialized_inventory.append(item)
        for i in characters:
            hero = dict()
            hero["hp"] = i.cur_health
            hero["mp"] = i.cur_mana
            serialized_characters.append(hero)
        info = {
            "save": {
                "inventory": serialized_inventory,
                "stage": stage,
                "players_group": serialized_characters
            }
        }
        with open(f"data/saves/save {slot}.json", "w") as f:
            json.dump(info, f)

    @staticmethod
    def load_stage(slot):
        if os.path.exists(f"data/saves/save {slot}.json"):
            with open(f"data/saves/save {slot}.json", "r") as f:
                return json.load(f)["save"]["stage"]
        return -1

    @staticmethod
    def load_game(slot, data):
        if os.path.exists(f"data/saves/save {slot}.json"):
            with open(f"data/saves/save {slot}.json", "r") as f:
                loaded_save = json.load(f)["save"]
                data.stage = loaded_save["stage"]
                for i in range(len(data.player_group)):
                    data.player_group[i].cur_health = loaded_save["players_group"][i]["hp"]
                    data.player_group[i].cur_mana = loaded_save["players_group"][i]["mp"]
                Data.create_items(loaded_save["inventory"], data)

    @staticmethod
    def create_items(inventory, data):
        data.player_items.clear()
        for i in inventory:
            for key, item in items.ITEMS.items():
                if i["item_id"] == item.item_id:
                    for j in range(i["count"]):
                        data.add_item(items.ITEMS[key])

    @staticmethod
    def new_game(data):
        data.stage = 0
        data.player_items.clear()
        for i in data.player_group:
            i.cur_health = i.health
            i.cur_mana = i.mana


current_data = Data()

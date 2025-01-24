class Data:
    screen_size = tuple()

    def __init__(self):
        self.player_group = list()
        self.player_items = list()
        self.difficult = ""

    def update_items(self):
        for i in self.player_items:
            if i.count < 1:
                self.player_items.remove(i)

    def set_leader(self, player):
        player.is_leader = True

    def add_item(self, item):
        if item not in self.player_items:
            self.player_items.append(item)
        else:
            self.player_items[self.player_items.index(item)].count += 1

    def get_items(self):
        return self.player_items

    def set_screen_size(self, size):
        Data.screen_size = size

    @staticmethod
    def get_screen_size():
        return Data.screen_size


current_data = Data()

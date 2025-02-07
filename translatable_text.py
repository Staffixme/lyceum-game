STRINGS = {
    "dummy": ("Dummy", "Манекен"),
    "dialogue_ex": ("This is dialogue example.", "Это пример диалога."),
    "new_game": ("New game", "Новая игра"),
    "load": ("Load game", "Загрузить"),
    "save": ("Save", "Сохранение"),
    "empty_slot": ("No data", "Нет данных"),
    "menu": ("Menu", "Меню"),
    "received": ("Received", "Получено"),
    "language": ("Переключиться на русский язык", "Switch to english"),
    "quit": ("Quit", "Выйти"),
    "to_menu": ("Back to title", "Выйти в гл. меню"),
    "attack": ("Melee", "Ближний бой"),
    "skill": ("Skill", "Навык"),
    "item": ("Item", "Предмет"),
    "defense": ("Defense", "Защита"),
    "escape": ("Escape", "Побег"),
    "use_skill": ("Use skill", "Использовать навык"),
    "use_item": ("Use item", "Использовать предмет"),
    "select_target": ("Select target", "Выберите цель"),
    "you_have": ("You have", "У вас есть"),
    "target_selection": ("target selection", "Выбор цели"),
    "selected_ally": ("Selected ally", "Выбранный союзник"),
    "action_selection": ("Action selection", "Выбор действия"),
    "navigation": ("Navigation", "Навигация"),
    "select": ("Select", "Выбрать"),
    "continue": ("Continue", "Продолжить"),
    "back": ("Back", "Назад"),
    "hp": ("HP", "ОЗ"),
    "mp": ("MP", "ОД"),
    "stage": ("Stage", "Этаж"),
    "recover": ("Recover", "Восстановление"),
    "recover_desc": ("Recover a large amount of HP to one ally", "Восстанавливает большое количество ОЗ одному союзнику"),
    "absolute_heal": ("Absolute heal", "Абсолютное исцеление"),
    "absolute_heal_desc": ("Recover a large amount of HP to one ally", "Восстанавливает огромное количество ОЗ всей команде"),
    "Samurai": ("Samurai", "Самурай"),
    "Kunoichi": ("Kunoichi", "Киноичи"),
    "Archer": ("Archer", "Лучник"),
    "Wizard": ("Wizard", "Маг"),
    "Magma": ("Magma", "Магма"),
    "katana": ("Katana", "Катана"),
    "bow": ("Bow", "Лук"),
    "chain": ("Chain", "Цепь"),
    "knife": ("Knife", "Нож"),
}

game_language = 1


def get_string(key: str) -> str:
    result = STRINGS.get(key, "Missing text asset")
    if isinstance(result, tuple):
        return result[game_language]
    else:
        return result

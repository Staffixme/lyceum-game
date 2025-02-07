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
    "recover_desc": (
    "Recover a large amount of HP to one ally", "Восстанавливает большое количество ОЗ одному союзнику"),
    "absolute_heal": ("Absolute heal", "Абсолютное исцеление"),
    "absolute_heal_desc": (
    "Recover a large amount of HP to one ally", "Восстанавливает огромное количество ОЗ всей команде"),
    "Samurai": ("Samurai", "Самурай"),
    "Kunoichi": ("Kunoichi", "Киноичи"),
    "Archer": ("Archer", "Лучник"),
    "Wizard": ("Wizard", "Маг"),
    "Magma": ("Magma", "Магма"),
    "katana": ("Katana", "Катана"),
    "bow": ("Bow", "Лук"),
    "chain": ("Chain", "Цепь"),
    "knife": ("Knife", "Нож"),
    "heal": ("Heal", "Исцеление"),
    "heal_desc": ("Recover a small amount of HP to one ally", "Восстанавливает малое количество ОЗ одному союзнику"),
    "aid": ("Aid", "Аптечка"),
    "aid_desc": ("Recover a small amount of HP to one ally", "Восстанавливает малое количество ОЗ одному союзнику"),
    "heal_poison": ("Heal poison", "Зелье здоровья"),
    "heal_poison_desc": ("Recover a medium amount of HP to one ally",
                           "Восстанавливает среднее количество ОЗ одному союзнику"),
    "charm_of_light": ("Charm of light", "Амулет света"),
    "charm_of_light_desc": ("Recover a large amount of HP to all team",
                            "Восстанавливает большое количество ОЗ всей команде"),
    "poison": ("Poison", "Яд"),
    "poison_desc": (
    "deals large amount of damage to a one enemy", "Наносит большое количество урона одному врагу"),
    "slash": ("Slash", "Разрез"),
    "slash_desc": (
        "deals medium amount of damage to all team", "Наносит среднее количество урона всей команде"),
    "fireball": ("Fireball", "Огненный шар"),
    "fireball_desc": (
        "deals large amount of damage to all team", "Наносит большое количество урона одному врагу"),

}

game_language = 1


def change_language():
    global game_language
    if game_language == 1:
        game_language = 0
    else:
        game_language = 1


def get_string(key: str) -> str:
    result = STRINGS.get(key, "Missing text asset")
    if isinstance(result, tuple):
        return result[game_language]
    else:
        return result

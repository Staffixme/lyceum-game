STRINGS = {
    "dummy": ("Dummy", "Манекен"),
    "dialogue_ex": ("This is dialogue example.", "Это пример диалога."),
    "new_game": ("New game", "Новая игра"),
    "load": ("Load game", "Загрузить"),
    "settings": ("Settings", "Настройки"),
    "quit": ("Quit", "Выйти"),
    "attack": ("Melee", "Ближний бой"),
    "skill": ("Skill", "Навык"),
    "item": ("Item", "Предмет"),
    "defense": ("Defense", "Защита"),
    "escape": ("Escape", "Побег"),
    "use_skill": ("Use skill", "Использовать навык"),
    "use_item": ("Use item", "Использовать предмет"),
    "select_target": ("Select target", "Выберите цель"),
    "target_selection": ("target selection", "Выбор цели"),
    "action_selection": ("Action selection", "Выбор действия"),
    "navigation": ("Navigation", "Навигация"),
    "select": ("Select", "Выбрать"),
    "back": ("Back", "Назад"),
    "hp": ("HP", "ОЗ"),
    "mp": ("MP", "ОД"),
    "recover": ("Recover", "Восстановление"),
    "recover_desc": ("Recover a large amount of HP to one ally", "Восстанавливает большое количество ОЗ одному союзнику"),
    "absolute_heal": ("Absolute heal", "Абсолютное исцеление"),
    "absolute_heal_desc": ("Recover a large amount of HP to one ally", "Восстанавливает огромное количество ОЗ всей команде"),
    "Magma": ("Magma", "Магма"),
    "Slime": ("Slime", "Слизь"),
}

game_language = 1


def get_string(key: str) -> str:
    result = STRINGS.get(key, "Missing text asset")
    if isinstance(result, tuple):
        return result[game_language]
    return result

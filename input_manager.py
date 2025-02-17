import pygame

MENU_LAYOUT = {
    pygame.K_SPACE: "Attack"
}

BATTLE_LAYOUT = {
    pygame.K_SPACE: "Select",
    pygame.K_a: "Prev",
    pygame.K_d: "Next",
    pygame.K_q: "Left",
    pygame.K_e: "Right",
    pygame.K_ESCAPE: "Back",
}

MOVEMENT_LAYOUT = {
    pygame.K_w: "Forward",
    pygame.K_a: "Left",
    pygame.K_d: "Right",
    pygame.K_s: "Back",
    pygame.K_h: "Save",
    pygame.K_TAB: "Menu",
}

UI_LAYOUT = {
    pygame.K_w: "Up",
    pygame.K_s: "Down",
    pygame.K_a: "Left",
    pygame.K_d: "Right",
    pygame.K_SPACE: "Confirm",
    pygame.K_KP_ENTER: "Confirm",
    pygame.K_ESCAPE: "Back"
}

INPUT_LAYOUTS = {
    "menu": MENU_LAYOUT,
    "battle": BATTLE_LAYOUT,
    "ui": UI_LAYOUT,
    "movement": MOVEMENT_LAYOUT
}


class InputManager:
    current_input = INPUT_LAYOUTS["menu"]
    current_key = None

    @staticmethod
    def listen(key):
        InputManager.current_key = key

    @staticmethod
    def reset_key():
        InputManager.current_key = None

    @staticmethod
    def change_layout(layout: str):
        InputManager.current_input = INPUT_LAYOUTS[layout]

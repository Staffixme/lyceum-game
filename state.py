from sys import getrefcount


class StateManager:
    current_state = None

    @staticmethod
    def change_state(new_state):
        if StateManager.current_state is not None:
            StateManager.current_state.exit()
        # del StateManager.current_state
        print(1, getrefcount(StateManager.current_state))
        StateManager.current_state = new_state
        print(2, getrefcount(StateManager.current_state))

    @staticmethod
    def update(event):
        if StateManager.current_state is not None:
            StateManager.current_state.update(event)

    @staticmethod
    def draw(screen):
        if StateManager.current_state is not None:
            StateManager.current_state.draw(screen)


class State:
    def __init__(self):
        self.input_layout = None

    def exit(self):
        pass

    def update(self, event):
        pass

    def draw(self, screen):
        pass

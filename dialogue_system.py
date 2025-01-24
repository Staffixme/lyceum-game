import pygame


def show_dialogue(text: str, character: str, portrait=None):
    surface = pygame.surface.Surface((1920, 1080), pygame.SRCALPHA, 32)
    bubble = pygame.draw.rect(surface, "#EEEEEE", (438, 700, 1156, 299), 0, 25)
    name = pygame.font.Font(None, 62)
    surface.blit(name.render(character, True, "blue"), (bubble.x + 32, bubble.y + 32))

    phrase = pygame.font.Font(None, 42)

    text_surface = pygame.surface.Surface((bubble.width, bubble.height), pygame.SRCALPHA, 32)
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = phrase.size(' ')[0] + 5  # The width of a space.
    max_width, max_height = bubble.size
    x, y = 0, 0
    for line in words:
        for word in line:
            word_surface = phrase.render(word, True, "black")
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width - 32:
                x = 0  # Reset the x.
                y += word_height + 5  # Start on new row.
            text_surface.blit(word_surface, (x, y))
            x += word_width + space
        x = 0  # Reset the x.
        y += word_height

    surface.blit(text_surface, (bubble.x + 32, bubble.y + 82))
    return surface

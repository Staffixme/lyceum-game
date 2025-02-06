from pygame.mixer import music
from game_resources import load_audio


class MusicManager:
    volume = 0.5

    @staticmethod
    def play_music(audio, is_loop=False):
        if is_loop:
            loop_count = -1
        else:
            loop_count = 1

        music.load(load_audio(audio))
        music.set_volume(MusicManager.volume)
        music.play(loop_count)

    @staticmethod
    def stop_music():
        music.stop()

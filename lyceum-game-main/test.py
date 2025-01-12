N = 7
PITCHES = ["до", "ре", "ми", "фа", "соль", "ля", "си"]
LONG_PITCHES = ["до-о", "ре-э", "ми-и", "фа-а", "со-оль", "ля-а", "си-и"]
INTERVALS = ["прима", "секунда", "терция", "кварта", "квинта", "секста", "септима"]


class Note:
    def __init__(self, name, is_long=False):
        if name.lower() not in PITCHES:
            raise ValueError(f"Неверная нота: {name}")
        self.name = name.lower()
        self.is_long = is_long

    def __str__(self):
        if self.is_long:
            return LONG_PITCHES[PITCHES.index(self.name)]
        return self.name


class Melody:
    def __init__(self, notes=None):
        self.notes = notes if notes else []

    def __str__(self):
        if not self.notes:
            return ""
        result = []
        first_note_str = str(self.notes[0])
        if first_note_str:
            first_note_str = first_note_str[0].upper() + first_note_str[1:]
        result.append(first_note_str)
        for note in self.notes[1:]:
            result.append(str(note))
        return ", ".join(result)

    def append(self, note):
        self.notes.append(note)

    def replace_last(self, note):
        self.notes[-1] = note

    def remove_last(self):
        if self.notes:
            self.notes.pop()

    def clear(self):
        self.notes.clear()

    def len(self):
        return len(self.notes)

    def transpose(self, shift, direction):
        new_notes = []
        for note in self.notes:
            idx = PITCHES.index(note.name)
            if direction == 'up':
                new_idx = idx + shift
                if new_idx >= N:
                    return Melody(self.notes.copy())
            elif direction == 'down':
                new_idx = idx - shift
                if new_idx < 0:
                    return Melody(self.notes.copy())
            else:
                raise ValueError("Направление должно быть 'up' или 'down'")
            new_notes.append(Note(PITCHES[new_idx], note.is_long))
        return Melody(new_notes)

    def rshift(self, shift):
        return self.transpose(shift, 'up')

    def lshift(self, shift):
        return self.transpose(shift, 'down')

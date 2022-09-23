class MoodVec:

    def __init__(self,
                 energy: float = 0.0,
                 valence: float = 0.0):
        self.energy = energy,
        self.valence = valence

    def __repr__(self):
        return f'<energy: {self.energy} | valence: {self.valence}>'

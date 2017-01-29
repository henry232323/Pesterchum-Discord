class Moods(object):
    moods = ["chummy", "rancorous", "offline", "pleasant", "distraught",
             "pranky", "smooth", "ecstatic", "relaxed", "discontent",
             "devious", "sleek", "detestful", "mirthful", "manipulative",
             "vigorous", "perky", "acceptant", "protective", "mystified",
             "amazed", "insolent", "bemused"]

    def __init__(self):
        self.usermoods = dict()
        self.value = 0

    @staticmethod
    def getMood(name):
        name = "offline" if name.lower() == "abscond" else name
        return Moods.moods.index(name.lower())

    @staticmethod
    def getName(index):
        return Moods.moods[index]


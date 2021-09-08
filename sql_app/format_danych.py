from datetime import datetime


class FormatDaty:
    def obecny_czas(self):
        return str(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
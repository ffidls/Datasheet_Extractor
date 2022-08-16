# from translate import Translator (?)
import parsing_pdf


class Trash:
    def __init__(self):
        self.cleaning = parsing_pdf.CleanPDF()

    def sort_trash(self, word):
        self.text = self.cleaning.del_trash(word)
        return self.find_problems()

    def find_problems(self):
        flag = True
        if len(self.text) < 6:
            return False
        try:  # check text on float numbers (with ".")
            _ = int(self.text)
            flag = False
        except Exception:
            pass

        if self.text.isalpha():
            return False
        try:
            if int(self.text) and float(self.text):
                return True
        except Exception:
            pass
        return flag

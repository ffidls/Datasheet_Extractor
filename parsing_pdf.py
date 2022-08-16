import PyPDF2


class Parsing:
    def __init__(self):
        pass

    def read_pdf(self, fail):
        try:
            pdfFileObj = open(fail, 'rb')
        except Exception:
            return None
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        lenn = pdfReader.numPages
        cleaning = CleanPDF()
        lst = []

        # read text pdf
        for i in range(lenn):
            pageObj = pdfReader.getPage(i)
            str1 = pageObj.extractText()
            lst.append(str1)
        pdfFileObj.close()

        lst2 = []
        for i in lst:
            a = i.split('\n')
            for n in a:
                if n == '' or n == ' ':
                    continue
                elif ' ' in n:
                    lst2 = cleaning.split_text(n, lst2)
                    continue
                else:
                    new_el = cleaning.del_trash(n)
                    if new_el is not None:
                        lst2.append(new_el)
                    continue
        return lst2


class CleanPDF:
    def __init__(self):
        pass

    def del_trash(self, text):  # for first
        trigger, text = self.find_signs(text)
        if trigger is not None:
            if trigger == '*':
                return None
        return text

    def split_text(self, text, list_for_text):
        copy_text = text.split(' ')
        for el in copy_text:
            clear_el = self.del_trash(el)
            if clear_el == '' or clear_el == ' ':
                continue
            elif clear_el is not None:
                list_for_text.append(clear_el)

        return list_for_text

    def find_signs(self, text):  # for second
        sign = None
        lst_signs = ['/', '�', '\xa0', '(', ',', ')', '’', '‘', '.', ':', '®', ';']
        if '+' in text or '=' in text or '±' in text:
            sign = '*'
            return sign, text

        for el in lst_signs:
            if el in text:
                text = text.replace(el, '')
        return sign, text

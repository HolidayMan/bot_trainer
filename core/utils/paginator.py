def build_pages(seq, step) -> list:
    pages = []
    page = []

    for i in range(len(seq)):
        if len(page) < step:
            page.append(seq[i])
        else:
            pages.append(page)
            page = [seq[i]]
    pages.append(page)
    return pages


class Page:
    previous_page = None
    next_page = None
    previous_page_number = None
    next_page_number = None
    def __init__(self, data, num, paginator):
        self.data = data
        self.number = num
        self.paginator = paginator


    def has_next(self):
        return bool(self.next_page)

    
    def has_previous(self):
        return bool(self.previous_page)


    def __repr__(self):
        return f"<Page %d of %d>" % (self.number, len(self.paginator.pages))


class Paginator:
    def __init__(self, sequence, step):
        self.pages = []
        for num, page in enumerate(build_pages(sequence, step), 1):
            new_page = Page(page, num, self)
            self.pages.append(new_page)
            if num == 1:
                previous_page = new_page
                continue
            previous_page.next_page = new_page
            previous_page.next_page_number = new_page.number
            new_page.previous_page = previous_page
            new_page.previous_page_number = previous_page.number
            previous_page = new_page
        self.num_pages = len(self.pages)


    def page(self,number):
        if number < 1 or number > len(self.pages):
            raise ValueError("invalid page number")
        return self.pages[number-1]

    
    def __getitem__(self, key):
        if key < -1 or key > len(self.pages) - 1:
            raise StopIteration
        return self.pages[key]

    
    
    
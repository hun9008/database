import numpy as np
import pandas as pd

# xlsx read
all_books = pd.read_excel("export_20220513133122.xlsx")
# print(all_books.head())
list_depts = \
    ["Philosophy", "religion", "social science", "natural science", "technological science", "art", "language", "literature", "history", "etc", "digital"]


dict_books = {}

# ISBN열을 book_new.txt에 저장 ISBN만 저장.
with open("book_new.txt", "w", encoding="utf-8") as f:
    f.write("book_id\tISBN\ttitle\tCategory\tAuthor\tPublisher\tPublication_date\n")
    for isbn in all_books["ISBN"]:
        isbn = str(isbn)
        isbn_num = dict_books.get(isbn)
        title = str(all_books[all_books["ISBN"] == isbn]["서명"].values[0])
        category = np.random.choice(list_depts, 1)[0]
        author = str(all_books[all_books["ISBN"] == isbn]["저자"].values[0])
        publisher = str(all_books[all_books["ISBN"] == isbn]["발행처"].values[0])
        publication_date = str(all_books[all_books["ISBN"] == isbn]["발행연도"].values[0])
        if isbn_num is None:
            dict_books[isbn] = 1
            isbn_num = 1
            # isbn + 001 저장. (같은 ISBN이 1개이기 때문)
            temp_str = str(isbn)
            if len(temp_str) == 13:
                f.write(isbn + "{:03d}\t".format(isbn_num))
                f.write(isbn + "\t")
                f.write(title + "\t" + category + "\t" + author + "\t" + publisher + "\t" + publication_date + "\n")
        else:
            dict_books[isbn] += 1
            isbn_num = dict_books[isbn]
            # isbn + 001 저장. (같은 ISBN이 2개 이상일 때)
            temp_str = str(isbn)
            if len(temp_str) == 13:
                f.write(isbn + "{:03d}\t".format(isbn_num))
                f.write(isbn + "\t")
                f.write(title + "\t" + category + "\t" + author + "\t" + publisher + "\t" + publication_date + "\n")
        



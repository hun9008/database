import numpy as np
import pandas as pd

# xlsx read
all_books = pd.read_excel("digital_book.xlsx")
# print(all_books.head())
list_depts = \
    ["PDF" ,"EPUB", "JPEG", "MOBI"]


dict_books = {}

# ISBN열을 book_new.txt에 저장 ISBN만 저장.
with open("book_digital.txt", "w", encoding="utf-8") as f:
    f.write("digital_id\ttitle\tdata_format\tCategory\tAuthor\tPublisher\tPublication_date\n")
    idx = 1
    for isbn in all_books["ISBN"]:
        isbn_num = dict_books.get(isbn)
        title = str(all_books[all_books["ISBN"] == isbn]["서명"].values[0])
        format = np.random.choice(list_depts, 1)[0]
        category = "Digital"
        author = str(all_books[all_books["ISBN"] == isbn]["저자"].values[0])
        publisher = str(all_books[all_books["ISBN"] == isbn]["발행처"].values[0])
        publication_date = str(all_books[all_books["ISBN"] == isbn]["발행연도"].values[0])

        f.write("{:06d}\t".format(idx))   
        idx += 1
        f.write(title + "\t" + format + "\t" + category + "\t" + author + "\t" + publisher + "\t" + publication_date + "\n")

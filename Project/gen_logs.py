from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

def read_books(path_book):
    list_books = []
    with open(path_book, "r", encoding="utf-8") as f:
        f.readline()
        for line in f:
            list_books.append(line.strip())
    return list_books

def read_users(path_user):
    list_users = []
    with open(path_user, "r", encoding="utf-8") as f:
        f.readline()
        for line in f:
            words = line.strip().split("\t")
            user_id = words[0]
            list_users.append(user_id)
    return list_users

def gen_logs(
    path_book:str="book_new.txt", path_user:str="student.tsv", 
    s_date:str="2021-01-01", e_date:str="2021-12-31", 
    num_candidates_mu:float=300.0, num_candidates_sigma:float=50.0,
    max_borrow_item=5,
    p_borrow_mu:float=0.3, p_borrow_sigma:float=0.01,
    p_return_mu:float=0.2, p_return_sigma:float=0.0025):
    '''
    This method generates log file from book id and student file.
    During start date ~ end date,
    1) every user will return the item with the probability p_return
    and
    1) every user will borrow the item from the candidates
        with the probabiltiy p_borrow

    Every user can have their own
        num_candidates: number of candidates (user preference)
        p_borrow: probability of borrow item
        p_return: probability of return item
    
    Args:
        s_date: start date of the log
        e_date: end date of the log
        num_candidates_mu/sigma: mean, standard deviation
             of the number of candidates.
        max_borrow_item: maximum number of borrowable items
        p_borrow_mu/sigma: mean, standard deviation
            of probability of borrow item
        p_return_mu/sigma: mean, standard deviation
            of probability of return item
    '''

    temp_list_items = read_books(path_book)
    for i in range(len(temp_list_items)):
        temp_list_items[i] = temp_list_items[i].split("\t")[0]
    list_items = temp_list_items
    # print(list_items[0])
    list_users = read_users(path_user)
    print(len(list_users))
    
    start_date = datetime.strptime(s_date, "%Y-%m-%d")
    end_date = datetime.strptime(e_date, "%Y-%m-%d")

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    
    # initialize
    np.random.seed(2)
    itemid2borrowed_userid = dict()
    userid2num_borrowed = defaultdict(int)

    # sampling candidate items, p_borrow, p_return
    userid2candidate_ids = defaultdict(list)
    userid2p_borrow = dict()
    userid2p_return = dict()
    list_num_candis = np.random.normal(num_candidates_mu, num_candidates_sigma, len(list_users))
    list_p_borrow = np.random.normal(p_borrow_mu, p_borrow_sigma, len(list_users))
    list_p_return = np.random.normal(p_return_mu, p_return_sigma, len(list_users))
    for i in range(len(list_users)):
        userid = list_users[i]
        num_candi = min(round(list_num_candis[i]), len(list_items))
        num_candi = max(num_candi, 0)
        list_candidate_ids = np.random.choice(list_items, num_candi, replace=False)
        userid2candidate_ids[userid] = list_candidate_ids
        p_borrow = min(list_p_borrow[i], 1.0)
        p_borrow = max(p_borrow, 0)
        p_return = min(list_p_return[i], 1.0)
        p_return = max(p_return, 0)
        userid2p_borrow[userid] = p_borrow
        userid2p_return[userid] = p_return
    # initialize end

    # everyday
    with open("logs.tsv", "w", encoding="utf-8") as f:
        # f.write("date\tuserid\titemid\ttype\n")
        f.write("book_id\tuser_id\tborrowed_date\treturned_date\n")
        for day in range(days_between_dates):
            if day % 50 == 0:
                print(day)
            dt = start_date + timedelta(day)
            day_diff = np.random.randint(1, 21)
            dt_borrow = dt - timedelta(day_diff)
            # print("dt : ", dt)
            # return first
            returned_items = []
            list_print = []
            for itemid, userid in itemid2borrowed_userid.items():
                rv = np.random.rand()
                if rv < userid2p_return[userid]:
                    returned_items.append(itemid)
                    dt_return = dt.replace(
                        hour=np.random.randint(9,12), 
                        minute=np.random.randint(60),
                        second=np.random.randint(60))
                    if (len(itemid) == 16):
                        list_print.append("{}\t{}\t{}\t{}\n".format(itemid, userid, dt_borrow, dt_return))
            # print("returned_items: ", len(returned_items))
            for del_itemid in returned_items:
                itemid2borrowed_userid.pop(del_itemid)
                # itemid2borrowed_userid.replace(del_itemid, "Null")
            list_print.sort()
            for line in list_print:
                f.write(line)

            # borrow item
            list_print.clear()
            for userid in list_users:
                num_remain = max_borrow_item - userid2num_borrowed[userid]
                list_candidate_ids = userid2candidate_ids[userid]
                target_itemids = np.random.choice(list_candidate_ids, num_remain, replace=False)
                for itemid in target_itemids:
                    # already borrowed by other user
                    if itemid in itemid2borrowed_userid:
                        continue
                    rv = np.random.rand()
                    if rv < userid2p_borrow[userid]:
                        itemid2borrowed_userid[itemid] = userid
                        dt_borrow = dt.replace(
                            hour=np.random.randint(12,18), 
                            minute=np.random.randint(60),
                            second=np.random.randint(60))
                        if(len(itemid) == 16):
                            list_print.append("{}\t{}\t{}\n".format(itemid, userid, dt_borrow))
            list_print.sort()
            for line in list_print:
                f.write(line)


        


    
gen_logs()


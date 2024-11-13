import numpy as np
import datetime

list_depts = \
    ["Philosophy", "religion", "social science", "natural science", "technological science", "art", "language", "literature", "history", "etc", "digital"]


list_addr = \
    ["Seoul", "Busan", "Daegu", "Incheon", "Gwangju", "Daejeon", "Ulsan", "Suwon"]

list_tier = \
    ["Gold", "Silver", "Bronze", "Iron"]

list_genders = ["Male", "Female"]
list_names = [
    [
        "James","Robert","John","Michael","David","William",
        "Richard","Joseph","Thomas","Charles","Christopher",
        "Daniel","Matthew","Anthony","Mark","Donald","Steven",
        "Paul","Andrew","Joshua","Kenneth","Kevin","Brian",
        "George","Timothy","Ronald","Edward","Jason","Jeffrey","Ryan",
        "Minjoon","Seojoon","Doyoon","Yejoon","Siu","Hajoon","Joowon",
        "Jiho","Jihoo","Joonwoo","Joonseo","Geonwoo","Dohyun"
    ],
    [
        "Mary","Patricia","Jennifer","Linda","Elizabeth","Barbara",
        "Susan","Jessica","Sarah","Karen","Lisa","Nancy","Betty",
        "Margaret","Sandra","Ashley","Kimberly","Emily","Donna",
        "Michelle","Carol","Amanda","Dorothy","Melissa","Deborah",
        "Stephanie","Rebecca","Sharon","Laura","Cynthia",
        "Seoyeon","Seoyoon","Jiwoo","Seohyun","Haeun","Hayoon","Minseo",
        "Jiyoo","Yoonseo","Jimin","Chaewon","Sua","Jia"
    ]
]
list_fnames = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", 
    "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
    "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez",
    "Moore", "Martin", "Jackson", "Thompson", "White",
    "Lopez", "Lee", "Gonzalez", "Harris", "Clark"
    "Lewis", "Robinson", "Walker", "Perez", "Hall",
    "Kim", "Park", "Choi", "Kang", "Cho", "Min", "Hong", "Jeong",
    "Sim", "Rho", "Song", "Yu", "Ha", "Han", "Heo",
    "Nguyen", "Bottier", "Rochette", "Bacha", "Dereskeviciute"
]
list_stu_year = range(2016,2020)

list_faculty_class = ["Staff", "Professor", "TA"]
list_faculty_year = range(1990,2020)

def gen_bdate(byear):
    start_date = datetime.date(byear,1,1)
    end_date = datetime.date(byear,12,31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = np.random.randint(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def gen_assign_date(current_date):
    # 오늘날짜로부터 이전 1년 이내의 날짜를 랜덤으로 생성
    start_date = current_date - datetime.timedelta(days=365)
    end_date = current_date
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = np.random.randint(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def gen_last_non_return_date(current_date):
    # 오늘날짜로부터 6개월 이내의 날짜를 랜덤으로 생성
    start_date = current_date - datetime.timedelta(days=180)
    end_date = current_date
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = np.random.randint(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date



def gen_stu(num):
    np.random.seed(2)
    with open("student.tsv", "w", encoding="utf-8") as f:
        header = "user_id\tname\t"
        header += "gender\tdept_id\tdept\t"
        header += "bdate\temail\tphone\ttier\tassign_date\tlast_non_return_date\n"
        f.write(header)
        for i in range(num):
            year = np.random.choice(list_stu_year,1)[0]
            sid = "{}{:04d}".format(1, i)
            gender_type = np.random.randint(2)
            gender = list_genders[gender_type]
            # dept_id = np.random.randint(len(list_depts))
            # dept = list_depts[dept_id]
            address_id = np.random.randint(len(list_addr))
            address = list_addr[address_id]
            name = np.random.choice(list_names[gender_type],1)[0]
            # fname = np.random.choice(list_fnames,1)[0]
            byear = year - 15
            bdate = gen_bdate(byear)
            age = 2024 - byear
            email = "{}_{}{}@ajou.ac.kr".format(name.lower(),str(byear)[2:4],name[0].lower())
            phone = "010-{:04d}".format(np.random.randint(10000))
            phone += "-{:04d}".format(np.random.randint(10000))
            tier = np.random.choice(list_tier,1)[0]
            current_date = datetime.date.today()
            one_years_ago = current_date - datetime.timedelta(days=365) 
            assign_date = gen_assign_date(one_years_ago)
            last_non_return_date = gen_last_non_return_date(datetime.date.today())

            line = "{}\t{}\t".format(sid, name)
            line += "{}\t{}\t".format(gender, address)
            line += "{}\t{}\t{}\t{}\t{}\t{}\n".format(age,email,phone,tier, assign_date, last_non_return_date)
            f.write(line)
    
        
def gen_faculty(num):
    np.random.seed(3)
    with open("employ.tsv", "w", encoding="utf-8") as f:
        header = "employ_id\tname\t"
        header += "dept_id\tphone\n"
        # header += "bdate\temail\tphone\n"
        f.write(header)
        for i in range(num):
            year = np.random.choice(list_faculty_year,1)[0]
            fid = "{}{:04d}".format(2, i)
            gender_type = np.random.randint(2)
            gender = list_genders[gender_type]
            dept_id = np.random.randint(len(list_depts))
            dept = list_depts[dept_id]
            name = np.random.choice(list_names[gender_type],1)[0]
            fname = np.random.choice(list_fnames,1)[0]
            fclass = np.random.choice(list_faculty_class,1)[0]
            byear = year - 25
            bdate = gen_bdate(byear)
            email = "{}_{}{}@ajou.ac.kr".format(name.lower(),str(byear)[2:4],fname[0].lower())
            phone = "010-{:04d}".format(np.random.randint(10000))
            phone += "-{:04d}".format(np.random.randint(10000))
            line = "{}\t{}\t{}\t{}\n".format(fid, name, dept_id, phone)
            # line += "{}\t{}\t{}\t".format(gender, dept_id, dept)
            # line += "{}\t{}\t{}\n".format(bdate,email,phone)
            f.write(line)
        gender_type = np.random.randint(2)
        name = np.random.choice(list_names[gender_type], 1)[0]
        phone = "010-{:04d}".format(np.random.randint(10000))
        phone += "-{:04d}".format(np.random.randint(10000))

        owner = "{}\t{}\t{}\t{}\n".format("21000", name, 11, phone)
        f.write(owner)

def gen_dept():
    with open("dept.tsv", "w", encoding="utf-8") as f:
        header = "dept\tdept_id\tmanager_eid\tmanager_start_date\n"
        f.write(header)
        for i in range(len(list_depts)):
            dept_id = i
            dept = list_depts[i]
            # employ.tsv에서 dept_id가 dept와 일치하는 사람을 찾아서 manager로 지정
            manager_eid = 20000
            with open("employ.tsv", "r", encoding="utf-8") as employ_file:
                employ_lines = employ_file.readlines()
                # print("read\n")
                for line in employ_lines:
                    # print("write\n")
                    employ_data = line.split("\t")
                    # print(employ_data[2])
                    dept_id_str = str(dept_id)
                    if employ_data[2] == dept_id_str:
                        manager_eid = employ_data[0]
                        # print("heat\n")
                        break
            # manager_eid = "2{:04d}".format(mana)
            manager_start_date = gen_assign_date(datetime.date.today())
            line = "{}\t{}\t{}\t{}\n".format(dept, dept_id, manager_eid, manager_start_date)
            f.write(line)

if __name__ == "__main__":
    gen_stu(1000)
    gen_faculty(1000)
    gen_dept()
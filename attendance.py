import redis
import random


def set_present(r, day, id):
    r.setbit(day, id, True)

#Can be used to query for no of users instantly
def get_present_for_day_so_far(r, day):
    return r.bitcount(day)

#Initializes all attendance to false
def initialze_database(r, days):
    for day in days:
        for i in range(100):
            r.setbit(day, i, False)

#Generates keys which are used as keys on redis itself
def generate_key(day):
    return "day" + str(day)

#Populates with random attendances
def populate_with_random_data(r, keys):
    for key in keys:
        for i in range(100):
            if random.choice([True, False]):
                set_present(r, key, i)

#Find present ids for a given day
def find_present(r, day):
    day = bytearray(r.get(day))
    present_ids = []
    for i in range(12):
        for shift in range(8):
            if ((day[i] >> shift) & 1) == 1:
                present_ids.append((8 * i) + (8 - shift - 1))

    final = day[-1]
    final = final >> 4
    for shift in range(4):
        if((final >> shift) & 1) == 1:
            present_ids.append(96 + shift)
    return sorted(present_ids)

#Find absent id's for a givent day
def find_absents(r, day):
    present = set(find_present(r, day))
    absent = set(range(100)) - present
    return list(absent)

#Find present on both days
def find_present_both_days(r, day1, day2):
    present_1 = set(find_present(r, day1))
    present_2 = set(find_present(r, day2))
    return list(present_1 & present_2)

#Find absent on both days
def find_absent_both_days(r, day1, day2):
    absent_1 = set(find_absents(r, day1))
    absent_2 = set(find_absents(r, day2))
    return list(absent_1 & absent_2)

def problem(r, no_of_days):
    keys = [generate_key(i + 1) for i in range(no_of_days)]
    print("Initializing database.....")
    initialze_database(r, keys)
    print("Populating Random Values.........")
    populate_with_random_data(r, keys)

    #This is done to limit the number of calls to the database else calls have to made in each function
    #All the functions are just passed the byte arrays
    print("==============PER DAY===============")
    for key in keys:
        print("Present on " + str(key))
        ids = find_present(r, key)
        print("Count:" + str(get_present_for_day_so_far(r, key)))
        print("Ids:" + str(ids))
        print("##################")
        print("Absent on " + key)
        ids = find_absents(r, key)
        print("Count:" + str(100 - get_present_for_day_so_far(r, key)))
        print("Ids:" + str(ids))
        print("##################")
    
    print("===========CONSECUTIVE DAYS===========")
    i = 0
    j = 1
    while(j < no_of_days):
        print("Present on both " + keys[i] + " and " + keys[j])
        ids = find_present_both_days(r, keys[i], keys[j])
        print("Count:" + str(len(ids)))
        print("Ids:" + str(ids))
        print("##################")
        print("Absent on both " + keys[i] + " and " + keys[j])
        ids = find_absent_both_days(r, keys[i], keys[j])
        print("Count:" + str(len(ids)))
        print("Ids:" + str(ids))
        print("##################")
        i += 1
        j += 1


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379)
    problem(r, 5)
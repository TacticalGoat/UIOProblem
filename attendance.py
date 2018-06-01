import redis
import struct
import random

def set_present(r, day, id):
    r.setbit(day, id, True)

def get_present_for_day_so_far(r, day):
    return r.bitcount(day)

def initialze_database(r, days):
    for day in days:
        for i in range(100):
            r.setbit(day, i, False)

def generate_key(day):
    return "day" + str(day)

def populate_with_random_data(r, keys):
    for key in keys:
        for i in range(100):
            if random.choice([True, False]):
                set_present(r, key, i)

def present_on_day(day):
    present_ids = []
    for i in range(12):
        for shift in range(8):
            if ((day[i] >> shift) & 1) == 1:
                present_ids.append((8 * i) + (8 - shift - 1))

    final = day[-1]
    final = final >> 4
    for shift in range(5):
        if((final >> shift) & 1) == 1:
            present_ids.append(96 + shift)

    return len(present_ids) , sorted(present_ids)

def absent_on_day(day):
    count = 0
    absent_ids = []
    for i in range(12):
        for shift in range(8):
            if ((day[i] >> shift) & 1) == 0:
                count += 1
                absent_ids.append((8 * i) + (8 - shift - 1))

    final = day[-1]
    final = final >> 4
    for shift in range(5):
        if((final >> shift) & 1) == 0:
            absent_ids.append(96 + shift)

    return len(absent_ids) , sorted(absent_ids)

def present_both_days(day1, day2):
    present_ids = []
    for i in range(12):
        common = day1[i] & day2[i]
        for shift in range(8):
            if ((common >> shift) & 1)== 1:
                present_ids.append((8 * i) +(8 - shift - 1))

    common = day1[-1] & day2[-1]
    common = common >> 4
    for shift in range(5):
        if((common >> shift) & 1 == 1):
            present_ids.append(96 + shift)

    return len(present_ids), present_ids

def absent_both_days(day1, day2):
    absent_ids = []
    for i in range(12):
        common = day1[i] | day2[i]
        for shift in range(8):
            if ((common >> shift) & 1) == 0:
                absent_ids.append((8 * i) +(8 - shift - 1))

    common = day1[-1] | day2[-1]
    common = common >> 4
    for shift in range(5):
        if((common >> shift) & 1 == 0):
            absent_ids.append(96 + shift)

    return len(absent_ids), absent_ids


def problem(r, no_of_days):
    keys = [generate_key(i + 1) for i in range(no_of_days)]
    print("Initializing database.....")
    initialze_database(r, keys)
    print("Populating Random Values.........")
    populate_with_random_data(r, keys)
    days = [bytearray(r.get(key)) for key in keys]
    print("==============PER DAY===============")
    for index , key in enumerate(keys):
        print("Present on " + key)
        count, ids = present_on_day(days[index])
        print("Count:" + str(count))
        print("Ids:" + str(ids))
        print("##################")
        print("Absent on " + key)
        count, ids = absent_on_day(days[index])
        print("Count:" + str(count))
        print("Ids:" + str(ids))
        print("##################")
    
    print("===========CONSECUTIVE DAYS===========")
    i = 0
    j = 1
    while(j < no_of_days):
        print("Present on both " + keys[i] + " and " + keys[j])
        count, ids = present_both_days(days[i], days[j])
        print("Count:" + str(count))
        print("Ids:" + str(ids))
        print("##################")
        print("Absent on both " + keys[i] + " and " + keys[j])
        count, ids = absent_both_days(days[i], days[j])
        print("Count:" + str(count))
        print("Ids:" + str(ids))
        print("##################")
        i += 1
        j += 1


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379)
    problem(r, 5)
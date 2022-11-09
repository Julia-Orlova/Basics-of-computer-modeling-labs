# MSS (Mass Service System) - система масового обслуговування
import random


class MSS1():
    mu = 5
    processors = 2
    average_l = 0
    average_mu = 1 / mu
    items = 0
    items_in_queue = 0
    availability_p1 = True
    availability_p2 = True
    queue = []

    def push(self, claim):
        MSS1.queue.append(claim)
        time_in_queue1[claim] = time
        MSS1.items_in_queue += 1


class MSS2():
    mu = 3
    l = 8
    processors = 2
    average_l = 0
    average_mu = 1 / mu
    items = 0
    items_in_queue = 0
    availability_p1 = True
    availability_p2 = True
    block = False
    queue = []

    def push(self, claim):
        if len(MSS2.queue) < 8:
            MSS2.queue.append(claim)
            time_in_queue2[claim] = time
            MSS2.items_in_queue += 1
            MSS2.block = False
        else:
            MSS2.block = True


MSS1 = MSS1()
MSS2 = MSS2()

time = 0
claims = [random.uniform(0, 0.4) for i in range(1000)]
time_in_queue1 = {}
time_in_queue2 = {}


def event_MSS1(claim, time, t1, t2):
    event_time = 0
    if MSS1.availability_p1:
        event_time += random.uniform(0, 2 * MSS1.average_mu)
        MSS1.items += 1
        MSS1.availability_p1 = False
        t1 = [time, time + event_time]
    elif MSS1.availability_p2:
        event_time += random.uniform(0, 2 * MSS1.average_mu)
        MSS1.items += 1
        t2 = [time, time + event_time]
        MSS1.availability_p2 = False
    else:
        MSS1.push(claim)

    if t1[0] > time or time > t1[1]:
        MSS1.availability_p1 = True
    if t2[0] > time or time > t2[1]:
        MSS1.availability_p2 = True

    return event_time, t1, t2


def event_MSS2(claim, time, t1, t2):
    event_time = 0
    if MSS2.availability_p1:
        event_time += random.uniform(0, 2 * MSS2.average_mu)
        MSS2.items += 1
        t1 = [time, time + event_time]
        MSS2.availability_p1 = False
    elif MSS2.availability_p2:
        event_time += random.uniform(0, 2 * MSS2.average_mu)
        MSS2.items += 1
        t2 = [time, time + event_time]
        MSS2.availability_p2 = False
    else:
        MSS2.push(claim)

    if t1[0] > time or time > t1[1]:
        MSS2.availability_p1 = True
    if t2[0] > time or time > t2[1]:
        MSS2.availability_p2 = True

    return event_time, t1, t2


average_time = 0
av_queue_len_MSS1 = 0
av_queue_len_MSS2 = 0
av_time_in_queue1 = 0
av_time_in_queue2 = 0

t1 = [0, 0]; t2 = [0, 0]
for claim in claims:
    av_queue_len_MSS1 += MSS1.items_in_queue
    if MSS1.items_in_queue > 0:
        MSS1.queue.append(claim)
        time_in_queue1[claim] = time
        MSS1.items_in_queue += 1
        if not MSS2.block:
            claim = MSS1.queue[0]
            MSS1.queue.remove(claim)
            av_time_in_queue1 += time - time_in_queue1[claim]
            MSS1.items_in_queue -= 1

    if not MSS2.block:
        event1 = event_MSS1(claim, time, t1, t2)
        average_time += event1[0]
        t1 = event1[1]
        t2 = event1[2]
        time += claim

    av_queue_len_MSS2 += MSS2.items_in_queue
    if MSS2.items_in_queue > 0:
        MSS2.queue.append(claim)
        time_in_queue2[claim] = time
        claim = MSS2.queue[0]
        MSS2.queue.remove(claim)
        av_time_in_queue2 += time - time_in_queue2[claim]

    event2 = event_MSS2(claim, time, t1, t2)
    average_time += event2[0]
    t1 = event2[1]
    t2 = event2[2]
    time += claim

a = 0
while MSS1.items_in_queue > 0:
    for i in MSS1.queue:
        if not MSS2.block:
            item = MSS1.queue[0]
            MSS1.queue.remove(item)
            av_time_in_queue1 += time - time_in_queue1[item]
            MSS1.items_in_queue -= 1
            event1 = event_MSS1(item, time, t1, t2)
            average_time += event1[0]
            t1 = event1[1]
            t2 = event1[2]
            time += item

            if MSS2.items_in_queue < 8:
                MSS2.queue.append(item)
                time_in_queue2[item] = time
                MSS2.items_in_queue += 1
            else:
                MSS2.block = True

        a += 1
        av_queue_len_MSS2 += MSS2.items_in_queue
        if MSS2.items_in_queue > 0:
            item = MSS2.queue[0]
            MSS2.queue.remove(item)
            av_time_in_queue2 += time - time_in_queue2[item]
            MSS2.items_in_queue -= 1
            event2 = event_MSS2(item, time, t1, t2)
            average_time += event2[0]
            t1 = event2[1]
            t2 = event2[2]
            time += item

# середній час проходження вимоги
average_time /= len(claims)
print('Середній час проходження вимоги =', round(average_time, 3))
print('')

# середня довжина черги СММ1
av_queue_len_MSS1 /= len(claims)
print('Середня довжина черги СММ1 =', round(av_queue_len_MSS1, 3))

# середня довжина черги СММ1
av_queue_len_MSS2 /= (len(claims) + a)
print('Середня довжина черги СММ2 =', round(av_queue_len_MSS2, 3))
print('')

# середній час очікування черзі СММ1
av_time_in_queue1 /= len(claims)
print('Середній час очікування черзі СММ1 =', round(av_time_in_queue1, 3))

# середній час очікування черзі СММ2
av_time_in_queue2 /= len(claims)
print('Середній час очікування черзі СММ2 =', round(av_time_in_queue2, 3))

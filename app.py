import random

queues = [
    "AKS&BM",
    "VM",
    "Integration",
    "Apps",
    "Dev",
    "Networking",
    "AME",
    "ASMS"
]

queue_need = {
    "AKS&BM":1,
    "VM":1,
    "Integration":1,
    "Apps":1,
    "Dev":1,
    "Networking":1,
    "AME":1,
    "ASMS":2
}

people = {
"Varun":["AKS&BM","VM","Integration","Dev","AME","ASMS"],
"Afnas":["AKS&BM","VM","Integration","Apps","AME","ASMS"],
"Ravi":["AKS&BM","Networking","VM","Apps","Dev","AME","ASMS"],
"Madhu":["ASMS"],
"Shaikh":["Networking","Apps","Dev"],
"Yash":["Networking","AKS&BM","VM","Integration","Dev","Apps"],
"Lovely":["Networking","AKS&BM","ASMS","Dev","Apps"],
"Noor":["Integration","Networking","VM","AKS&BM","Apps","Dev"],
"Aishwary":["AKS&BM","VM","Apps","Dev","AME","Integration"],
"Christina":["AKS&BM","VM","Networking","Dev","Apps","Integration"]
}

leave_input = input("Enter names on leave separated by comma: ")
leave = [x.strip() for x in leave_input.split(",") if x.strip()]

available = {p:q for p,q in people.items() if p not in leave}

assignments = {q:[] for q in queues}
person_duty = {p:[] for p in available}

people_list = list(available.keys())
random.shuffle(people_list)

MAX_DUTY = 2

# -------- ASMS first --------

asms_candidates = [p for p in people_list if "ASMS" in available[p]]
random.shuffle(asms_candidates)

for p in asms_candidates:

    if len(assignments["ASMS"]) == 2:
        break

    if len(person_duty[p]) < MAX_DUTY:
        assignments["ASMS"].append(p)
        person_duty[p].append("ASMS")

# -------- Networking --------

net_candidates = [
p for p in people_list
if "Networking" in available[p]
and len(person_duty[p]) == 0
]

if not net_candidates:
    net_candidates = [p for p in people_list if "Networking" in available[p]]

for p in net_candidates:

    if len(person_duty[p]) < MAX_DUTY:
        assignments["Networking"].append(p)
        person_duty[p].append("Networking")
        break

# -------- Remaining queues --------

for queue in queues:

    if queue in ["ASMS","Networking"]:
        continue

    candidates = [p for p in people_list if queue in available[p]]
    random.shuffle(candidates)

    chosen = None

    # Prefer unused people
    for p in candidates:

        if len(person_duty[p]) == 0:
            chosen = p
            break

    # allow double duty if needed
    if chosen is None:

        for p in candidates:

            if len(person_duty[p]) >= MAX_DUTY:
                continue

            if "ASMS" in person_duty[p]:
                continue

            if "Networking" in person_duty[p]:
                continue

            chosen = p
            break

    if chosen:
        assignments[queue].append(chosen)
        person_duty[chosen].append(queue)

# -------- Output --------

print("\nDuty Allocation:\n")

for q in queues:
    print(f"{q}: {', '.join(assignments[q])}")

extras = [p for p in person_duty if len(person_duty[p]) == 0]

if extras:
    print("\nExtra People:", ", ".join(extras))

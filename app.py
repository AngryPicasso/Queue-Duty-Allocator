import streamlit as st
import random

st.title("Duty Allocation Tool")

# -------- Queue Groups --------

core_queues = ["AKS&BM", "VM", "Networking"]
das_queues = ["Apps", "Dev", "Integration", "AME"]
asms_queue = ["ASMS"]

queues = core_queues + das_queues + asms_queue

# -------- People --------

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

# -------- User Controls --------

leave_input = st.text_input("Enter names on leave (comma separated)")
generate = st.button("Generate Duty Allocation")

# -------- Queue Structure (shown before generation) --------

st.subheader("Queue Structure")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Core")
    for q in core_queues:
        st.write(q)

with col2:
    st.markdown("### DAS")
    for q in das_queues:
        st.write(q)

with col3:
    st.markdown("### ASMS")
    st.write("ASMS")

# -------- Generate Duties --------

if generate:

    leave = [x.strip() for x in leave_input.split(",") if x.strip()]
    available = {p:q for p,q in people.items() if p not in leave}

    assignments = {q:[] for q in queues}
    person_duty = {p:[] for p in available}

    people_list = list(available.keys())
    random.shuffle(people_list)

    MAX_DUTY = 2

    # -------- ASMS --------

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

    # -------- Remaining Queues --------

    for queue in queues:

        if queue in ["ASMS","Networking"]:
            continue

        candidates = [p for p in people_list if queue in available[p]]
        random.shuffle(candidates)

        chosen = None

        for p in candidates:
            if len(person_duty[p]) == 0:
                chosen = p
                break

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

    # -------- Display Results --------

    st.subheader("Duty Allocation")

    st.markdown("### Core")
    for q in core_queues:
        st.write(f"{q}: {', '.join(assignments[q])}")

    st.markdown("### DAS")
    for q in das_queues:
        st.write(f"{q}: {', '.join(assignments[q])}")

    st.markdown("### ASMS")
    st.write(f"ASMS: {', '.join(assignments['ASMS'])}")

    extras = [p for p in person_duty if len(person_duty[p]) == 0]

    if extras:
        st.write("Extra People:", ", ".join(extras))

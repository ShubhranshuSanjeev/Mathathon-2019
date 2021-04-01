class Graph:
    def __init__(self):
        self.V = []
        self.E = []

# Slot Course realtion graph
def buildGraph(G, course_info):
    for course, s in course_info.items():
        G.V.append(course)
        for slot_set in s:
            G.V.append(slot_set)
            G.E.append((course, slot_set))
    G.V = list(set(G.V))
    G.E = list(set(G.E))
    return G

def heuristic(htype, G):
    state_table = {x: '' for x in range(31, 61)}
    slot_prio_table = {x: 5 for x in range(31, 61)}
    course_prio_table = [(1.5, 'MAT2002'), (1.5, 'CSE2003'), (1.4, 'CSE1003'), (1.3, 'CSE1002'), (1.2, 'CHY1701'), (1.2, 'ENG1011'), (1.0, 'CSE1004')]
    
    if htype == 0:  # Prefer lesser classes as we approach weekend
        slot_prio_table[31] = 5
        slot_prio_table[32] = 5
        slot_prio_table[33] = 4
        slot_prio_table[34] = 4
        slot_prio_table[35] = 3
        slot_prio_table[36] = 3
        slot_prio_table[37] = 5
        slot_prio_table[38] = 5
        slot_prio_table[39] = 4
        slot_prio_table[40] = 4
        slot_prio_table[41] = 3
        slot_prio_table[42] = 3
        slot_prio_table[43] = 4
        slot_prio_table[44] = 4
        slot_prio_table[45] = 3
        slot_prio_table[46] = 3
        slot_prio_table[47] = 1
        slot_prio_table[48] = 1
        slot_prio_table[49] = 3
        slot_prio_table[50] = 3
        slot_prio_table[51] = 2
        slot_prio_table[52] = 2
        slot_prio_table[53] = 1
        slot_prio_table[54] = 1
        slot_prio_table[55] = 1
        slot_prio_table[56] = 1
        slot_prio_table[57] = 1
        slot_prio_table[58] = 1
        slot_prio_table[59] = 1
        slot_prio_table[60] = 1

    if htype == 1:  # Prefer earlier classes
        for slot, prio in slot_prio_table.items():
            if slot % 6 == 0 or slot % 6 == 5:
                slot_prio_table[slot] = 3
            elif slot % 6 == 3 or slot % 6 == 4:
                slot_prio_table[slot] = 4
    
    if htype == 2:  # Friday free
        for slot, prio in slot_prio_table.items():
            if (slot % 6 == 0 or slot % 6 == 5) and slot > 54:
                slot_prio_table[slot] = 2
            elif slot % 6 == 0 or slot % 6 == 5:
                slot_prio_table[slot] = 4
            elif slot > 54:
                slot_prio_table[slot] = 3

    if htype == 3:  # Prefer late classes
        for slot, prio in slot_prio_table.items():
            if slot % 6 == 1 or slot % 6 == 2:
                slot_prio_table[slot] = 3
            elif slot % 6 == 3 or slot % 6 == 4:
                slot_prio_table[slot] = 4
    s2 = slot_prio_table.copy()
    solutions = None
    count = min(s2.values())

# Try to find solutions using only priority 5 slots, if none found then increase priority of all
# other slots by 1 and retry with the new set of priority 5 slots until the point where all
# slots have priority 5 or a solution is found.

    while not solutions and count != 5:
        f = False
        new_state_table = {}
        for slot, prio in s2.items():
            if prio == 5:
                new_state_table.update({slot: ''})
        for slot, prio in s2.items():
            if prio < 5:
                s2[slot] += 1
                f = True
        if f: count += 1
        solutions = buildSolution(G, new_state_table, s2, course_prio_table)
    
    return solutions, slot_prio_table

def buildSolution(G, state_table, slot_prio_table, course_prio_table):
    if len(course_prio_table) == 0:
        return [state_table]
    
    solutions = []
    
    course = course_prio_table[-1][1]
    
    for slot_set in [x[1] for x in G.E if x[0] == course]:
        new_state_table = state_table.copy()
        new_cpt = course_prio_table.copy()
        new_cpt.pop()
        
        slots = [int(x[1:]) for x in slot_set.split('+')]
        
        slots_available = True
        for slot in slots:
            if state_table.get(slot, 1):
                slots_available = False
        
        if not slots_available:
            continue
        for slot in slots:
            new_state_table[slot] = course
        
        t = buildSolution(G, new_state_table, slot_prio_table, new_cpt)
        solutions = solutions + t
    
    return solutions
    
Courses = {'CSE1003': ('L39+L40', 'L43+L44', 'L41+L42', 'L51+L52', 'L45+L46', 'L57+L58', 'L31+L32',
                       'L53+L54', 'L35+L36', 'L55+L56', 'L37+L38', 'L47+L48'),
           'MAT2002': ('L45+L46', 'L59+L60', 'L35+L36', 'L51+L52', 'L31+L32', 'L37+L38', 'L33+L34',
                       'L53+L54', 'L39+L40', 'L47+L48', 'L49+L50'),
            'CHY1701': ('L33+L34', 'L39+L40', 'L47+L48', 'L43+L44', 'L49+L50', 'L35+L36', 'L31+L32',
                        'L53+L54', 'L59+L60', 'L51+L52', 'L45+L46', 'L41+L42', 'L55+L56', 'L37+L38', 'L57+L58'),
           'CSE2003': ('L53+L54', 'L45+L46', 'L55+L56', 'L49+L50', 'L35+L36', 'L31+L32', 'L39+L40',
                        'L33+L34', 'L41+L42', 'L59+L60', 'L43+L44'),
           'CSE1004': ('L51+L52', 'L39+L40', 'L53+L54', 'L31+L32', 'L45+L46', 'L57+L58', 'L41+L42', 
                        'L55+L56', 'L37+L38', 'L43+L44'),
           'CSE1002': ('L41+L42+L49+L50+L57+L58', 'L33+L34+L43+L44+L59+L60',
                        'L37+L38+L45+L46+L53+L54', 'L35+L36+L37+L38+L51+L52',
                        'L37+L38+L53+L54+L57+L58', 'L39+L40+L45+L46+L53+L54',
                        'L41+L42+L51+L52+L57+L58', 'L35+L36+L43+L44+L57+L58',
                        'L41+L42+L51+L52+L55+L56', 'L31+L32+L45+L46+L57+L58',
                        'L35+L36+L45+L46+L51+L52', 'L33+L34+L37+L38+L53+L54',
                        'L39+L40+L45+L46+L57+L58', 'L31+L32+L39+L40+L53+L54',
                        'L39+L40+L47+L48+L49+L50', 'L33+L34+L49+L50+L59+L60',
                        'L35+L36+L39+L40+L55+L56', 'L33+L34+L41+L42+L43+L44',
                        'L31+L32+L45+L46+L59+L60'),

           'ENG1011': ('L37+L38+L55+L56', 'L33+L34+L47+L48', 'L35+L36+L53+L54',
                        'L41+L42+L51+L52', 'L43+L44+L49+L50', 'L49+L50+L59+L60', 
                        'L33+L34+L37+L38', 'L37+L38+L49+L50', 'L37+L38+L53+L54',
                        'L35+L36+L57+L58', 'L41+L42+L59+L60', 'L39+L40+L53+L54',
                        'L43+L44+L57+L58', 'L43+L44+L59+L60', 'L45+L46+L57+L58',
                        'L47+L48+L57+L58', 'L39+L40+L49+L50', 'L39+L40+L51+L52',
                        'L31+L32+L43+L44', 'L31+L32+L45+L46', 'L39+L40+L47+L48',
                        'L35+L36+L45+L46', 'L37+L38+L57+L58')}

G = buildGraph(Graph(), Courses)
solutions, slot_prio_table = heuristic(2, G)

c2 = {'CSE1003': 3, 'CHY1701': 5, 'MAT2002': 1, 'CSE2003': 2, 'CSE1004': 7, 'CSE1002': 4, 'ENG1011': 6}
c3 = {'CSE1003': 1.4, 'CHY1701': 1.2, 'MAT2002': 1.5, 'CSE2003': 1.5, 'CSE1004': 1.0, 'CSE1002': 1.3, 'ENG1011': 1.2}

if not solutions:
    print('No solutions')
else:
    d = {}

    mscore = 0
    for sol in solutions:
        score = 0
        count = 0
        for x in range(31, 61):
            if sol.get(x, None):
                score += slot_prio_table[x]*c3[sol[x]]
            else:
                pass
            count += 1
            if count == 6:
                count = 0

        if score > mscore:
            mscore = score
        d.update({score: d.get(score, []) + [sol]})
    
    for sol in d[mscore]:
        count = 0
        for x in range(31, 61):
            if sol.get(x, None):
                print(c2[sol[x]], end='')
            else:
                print('-', end='')
            count += 1
            if count == 6:
                print()
                count = 0
        print()

    print("MAT2002: 1, CSE2003: 2, CSE1003: 3, CSE1002: 4, CHY1701: 5, ENG1011: 6, CSE1004:7")
    print()
    print('Total number of solutions found:', len(solutions))
    print('Highest score amongst all solutions:', mscore)
    print('Number of solutions with the highest score:', len(d[mscore]))

from inference import *

drones = ["Belhino", "Motomiya", "Suzutake", "Zarobitchi"]
heights = ["350ft", "475ft", "650ft", "1000ft"]
#prices = ["450$", "525$", "600$", "675$"] n^3


symbols = []


knowledge = And()


for drone in drones:
    for height in heights:
            symbols.append(Symbol(f"{drone}{height}"))

#Each drone has a height
for drone in drones:
    knowledge.add(Or(
        Symbol(f"{drone}350ft"),
        Symbol(f"{drone}475ft"),
        Symbol(f"{drone}650ft"),
        Symbol(f"{drone}1000ft")
    ))

#Only one drone per height
for drone in drones:
    for h1 in heights:
        for h2 in heights:
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{drone}{h1}"), Not(Symbol(f"{drone}{h2}")))
                )


#Only one height per drone
for height in heights:
     for d1 in drones:
        for d2 in drones:
            if d1 != d2:
                knowledge.add(
                    Implication(Symbol(f"{d1}{height}"), Not(Symbol(f"{d2}{height}")))
                )


knowledge.add(
    Not(And(Symbol("Zaraobitchi350ft"), 
            Symbol("Zarobitchi650ft"), 
            Symbol("Zarobitchi1000ft")))
)

knowledge.add(
    And(Symbol("Motomiya1000ft"),
        Not(And(Symbol("Belhino1000ft"), 
                Symbol("Suzutake1000ft"),
                Symbol("Zarobitchi1000ft"))))
)

knowledge.add(
    Or(Symbol("Belhino350ft"), Symbol("Belhino650ft"))
)

knowledge.add(
    Or(Symbol("Suzutake350ft"), Symbol("Suzutake650ft"))
)

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)

"""Study 2c case builder (deterministic; no randomness, no model calls).

24 obligations x 2 structures (POINT, SCOPE) x 4 variants (CLEAN, COMMISSION, OMISSION, ADD).
Target rule r01 is conjunctive: "must DO(A), and must not DO(B)".
  CLEAN       : DO(A) occurs, DO(B) does not.          oracle: no violation
  COMMISSION  : DO(B) occurs in the target slot, DO(A) absent.   violation (contrary evidence + absence)
  OMISSION    : neutral action in the target slot.      violation (absence only)
  ADD         : DO(A) at the target slot plus DO(B) in a later slot. violation (contrary evidence only)
Two background rules r02, r03 are simple event requirements satisfied by an explicit beat in every variant.
No evaluative wording in any scene line; no explicit absence statement in OMISSION.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "study2c_cases.jsonl"

# (scene, actor, checkpoint, type, do_inf, do_3sg, A, B, bg1_inf, bg1_3sg, bg2_inf, bg2_3sg, f1, f2, f3, f4)
S = []


def add(*a):
    S.append(a)


# ---- T1: give to ----
add("a courier at a front desk", "courier", "front desk", "give",
    "give a stamped form to {Z}", "gives a stamped form to {Z}", "Dana", "Omar",
    "switch off the desk lamp", "switches off the desk lamp", "sign the delivery log", "signs the delivery log",
    "sorts the mail", "checks the clock", "wipes the counter", "adjusts the chair")
add("a librarian at a lending counter", "librarian", "lending counter", "give",
    "give a library card to {Z}", "gives a library card to {Z}", "Mei", "Tom",
    "stamp the return slip", "stamps the return slip", "close the cash drawer", "closes the cash drawer",
    "shelves a book", "straightens the pens", "reads the notice board", "dusts the monitor")
add("a teacher beside a classroom door", "teacher", "classroom door", "give",
    "give a worksheet to {Z}", "gives a worksheet to {Z}", "Priya", "Jonas",
    "erase the board", "erases the board", "open the window", "opens the window",
    "collects a folder", "taps the bell", "straightens a desk", "checks the roster")
add("a pharmacist at a pickup window", "pharmacist", "pickup window", "give",
    "give a printed leaflet to {Z}", "gives a printed leaflet to {Z}", "Ruth", "Colin",
    "lock the storage cabinet", "locks the storage cabinet", "log the temperature", "logs the temperature",
    "counts the trays", "refills the tape", "wipes the scale", "stacks the bags")
add("a porter in a hotel lobby", "porter", "lobby desk", "give",
    "give a room key to {Z}", "gives a room key to {Z}", "Elena", "Marcus",
    "ring the service bell", "rings the service bell", "fold the luggage cart", "folds the luggage cart",
    "adjusts a cushion", "waters a plant", "checks the lift panel", "sweeps the mat")
add("a chef at a serving pass", "chef", "serving pass", "give",
    "give a tasting spoon to {Z}", "gives a tasting spoon to {Z}", "Hana", "Luis",
    "turn off the burner", "turns off the burner", "wipe the knife", "wipes the knife",
    "stirs the pot", "slices a lemon", "rinses a bowl", "reads the order board")
add("a mechanic at a workshop counter", "mechanic", "workshop counter", "give",
    "give a service tag to {Z}", "gives a service tag to {Z}", "Ines", "Victor",
    "hang the wrench", "hangs the wrench", "switch off the compressor", "switches off the compressor",
    "wipes his hands", "checks a tyre", "sweeps the floor", "oils a hinge")
add("a guide at a museum entrance", "guide", "entrance hall", "give",
    "give a brochure to {Z}", "gives a brochure to {Z}", "Nora", "Felix",
    "unclip the rope", "unclips the rope", "turn on the audio panel", "turns on the audio panel",
    "straightens a sign", "checks the map", "adjusts a lamp", "counts the pamphlets")
# ---- T2: place on ----
add("a nurse at a prep table", "nurse", "prep table", "place",
    "place a red tag on {Z}", "places a red tag on {Z}", "the green tray", "the grey tray",
    "wash her hands", "washes her hands", "record the pulse", "records the pulse",
    "opens a drawer", "sets out gauze", "checks the chart", "wipes the trolley")
add("a baker at a cooling station", "baker", "cooling station", "place",
    "place a paper label on {Z}", "places a paper label on {Z}", "the left rack", "the right rack",
    "dust the flour", "dusts the flour", "set the timer", "sets the timer",
    "turns a tray", "opens the oven door", "wipes the board", "folds a cloth")
add("a gardener in a greenhouse", "gardener", "potting bench", "place",
    "place a stake marker in {Z}", "places a stake marker in {Z}", "the north bed", "the south bed",
    "close the vent", "closes the vent", "coil the hose", "coils the hose",
    "pulls a weed", "checks a leaf", "moves a pot", "brushes the soil")
add("a tailor at a fitting room", "tailor", "fitting room", "place",
    "place a chalk mark on {Z}", "places a chalk mark on {Z}", "the blue sleeve", "the black sleeve",
    "hang the tape measure", "hangs the tape measure", "fold the spare cloth", "folds the spare cloth",
    "threads a needle", "smooths a seam", "checks a button", "sorts the pins")
add("a lab technician at an analysis bench", "technician", "analysis bench", "place",
    "place a sample sticker on {Z}", "places a sample sticker on {Z}", "the amber vial", "the clear vial",
    "close the fume hood", "closes the fume hood", "record the humidity", "records the humidity",
    "wipes a pipette", "checks the rack", "labels a notebook", "adjusts the stool")
add("a dock worker at a loading bay", "dock worker", "loading bay", "place",
    "place a seal on {Z}", "places a seal on {Z}", "crate nine", "crate ten",
    "sweep the ramp", "sweeps the ramp", "switch off the floodlight", "switches off the floodlight",
    "stacks a pallet", "checks a strap", "moves a cone", "reads the manifest")
add("a farmer in a milking shed", "farmer", "milking shed", "place",
    "place an ear tag on {Z}", "places an ear tag on {Z}", "the brown cow", "the white cow",
    "rinse the bucket", "rinses the bucket", "latch the gate", "latches the gate",
    "fills a trough", "checks the hay", "brushes a stool", "counts the pails")
add("a carpenter at a sawing table", "carpenter", "sawing table", "place",
    "place a pencil mark on {Z}", "places a pencil mark on {Z}", "the oak plank", "the pine plank",
    "unplug the saw", "unplugs the saw", "sweep the shavings", "sweeps the shavings",
    "tests a clamp", "sands an edge", "checks the level", "stacks a board")
# ---- T3: write name ----
add("a clerk at a returns counter", "clerk", "returns counter", "write",
    "write the name {Z} on the receipt", "writes the name {Z} on the receipt", "Anil Rao", "Kofi Mensah",
    "stamp the form", "stamps the form", "lock the till", "locks the till",
    "opens the ledger", "sorts the coins", "straightens the bags", "checks the printer")
add("a radio host in a studio", "host", "studio desk", "write",
    "write the name {Z} on the schedule", "writes the name {Z} on the schedule", "Leila Haddad", "Piotr Nowak",
    "mute the microphone", "mutes the microphone", "pour a glass of water", "pours a glass of water",
    "adjusts the headphones", "checks the playlist", "taps the console", "clears the desk")
add("an auditor at a records table", "auditor", "records table", "write",
    "write the name {Z} on the audit sheet", "writes the name {Z} on the audit sheet", "Sofia Lund", "Daniel Okoye",
    "close the binder", "closes the binder", "initial the cover page", "initials the cover page",
    "opens a folder", "checks a total", "sharpens a pencil", "aligns the stack")
add("a florist at a wrapping bench", "florist", "wrapping bench", "write",
    "write the name {Z} on the gift card", "writes the name {Z} on the gift card", "Yuki Tanaka", "Samir Qadir",
    "tie the ribbon", "ties the ribbon", "trim the stems", "trims the stems",
    "sweeps a leaf", "fills a vase", "checks the cooler", "wipes the bench")
add("a locksmith at a service counter", "locksmith", "service counter", "write",
    "write the name {Z} on the work order", "writes the name {Z} on the work order", "Greta Voss", "Emeka Obi",
    "file the key blank", "files the key blank", "close the toolbox", "closes the toolbox",
    "tests a lock", "oils a cylinder", "sorts the keys", "sweeps the shavings")
add("a ranger at a park kiosk", "ranger", "park kiosk", "write",
    "write the name {Z} on the permit", "writes the name {Z} on the permit", "Mateo Silva", "Ingrid Berg",
    "raise the flag", "raises the flag", "lock the supply box", "locks the supply box",
    "checks the radio", "reads the weather board", "folds a map", "wipes the window")
add("a stagehand at a lighting rail", "stagehand", "lighting rail", "write",
    "write the name {Z} on the cue sheet", "writes the name {Z} on the cue sheet", "Chloe Martin", "Rashid Khan",
    "switch off the work light", "switches off the work light", "coil the cable", "coils the cable",
    "tests a lamp", "tapes a mark", "checks a gel", "moves a ladder")
add("a pilot at a dispatch window", "pilot", "dispatch window", "write",
    "write the name {Z} on the flight slip", "writes the name {Z} on the flight slip", "Anders Holm", "Tariq Aziz",
    "fold the chart", "folds the chart", "zip the flight bag", "zips the flight bag",
    "checks the fuel gauge", "adjusts a strap", "reads the wind sock", "taps the logbook")

assert len(S) == 24, len(S)
TARGET_SLOTS = [1, 4, 6, 2, 5, 3]  # cycled by obligation index: early/mid/late balanced


def cap(x):
    return x[0].upper() + x[1:]


def build():
    cases = []
    for i, sp in enumerate(S):
        (scene, actor, cp, typ, do_inf, do_3, A, B, b1i, b1s, b2i, b2s, f1, f2, f3, f4) = sp
        t = TARGET_SLOTS[i % 6]
        oid = "o%02d" % (i + 1)
        for structure in ("point", "scope"):
            if structure == "point":
                r1 = "at the %s, the %s must %s, and must not %s" % (cp, actor, do_inf.format(Z=A), do_inf.format(Z=B))
                pre = "At the %s, the " % cp
            else:
                r1 = "at some point in the scene, the %s must %s, and must never %s" % (actor, do_inf.format(Z=A), do_inf.format(Z=B))
                pre = "The "
            rules = {"r01": r1,
                     "r02": "the %s must %s at some point in the scene" % (actor, b1i),
                     "r03": "the %s must %s at some point in the scene" % (actor, b2i)}
            beatA = pre + "%s %s." % (actor, do_3.format(Z=A))
            beatB = pre + "%s %s." % (actor, do_3.format(Z=B))
            neu = lambda x: "The %s %s." % (actor, x)
            bg1, bg2 = neu(b1s), neu(b2s)
            fill = [neu(f1), neu(f2), neu(f3)]
            order = [p for p in range(1, 7) if p != t]
            slots = dict(zip(order, [bg1, fill[0], bg2, fill[1], fill[2]]))
            f1_slot = order[1]

            def render(target_text, add_b=False):
                s_ = dict(slots); s_[t] = target_text
                if add_b: s_[f1_slot] = beatB
                return [s_[p] for p in range(1, 7)]
            variants = {
                "CLEAN": (render(beatA), False, ["A"]),
                "COMMISSION": (render(beatB), True, ["B"]),
                "OMISSION": (render(neu(f4)), True, []),
                "ADD": (render(beatA, add_b=True), True, ["A", "B"]),
            }
            setup = ("Scene: %s. The briefing lists three rules: (r01) %s (r02) %s (r03) %s. "
                     "No events occur outside the described beats.") % (
                scene, r1, rules["r02"], rules["r03"])
            # NOTE: rules are joined like Study 2b: "(r01) text (r02) text (r03) text"
            for cond, (beats, label, evs) in variants.items():
                script = "\n".join("L%d: %s" % (k + 1, b) for k, b in enumerate(beats))
                cases.append({
                    "base_case_id": "%s%s" % (oid, "P" if structure == "point" else "S"),
                    "obligation_id": oid, "structure": structure, "condition": cond,
                    "rule_id": "r01", "rule_family": "give_to" if typ == "give" else ("place_on" if typ == "place" else "write_name"),
                    "setup": setup, "script": script, "rules": rules,
                    "target_requirement": r1,
                    "expected_event": "ev_A", "incompatible_events": ["ev_B"],
                    "observed_events": ["ev_" + e for e in evs] + ["ev_bg1", "ev_bg2"],
                    "oracle_label": label, "target_position": t,
                    "target_position_class": "early" if t <= 2 else ("middle" if t <= 4 else "late"),
                    "word_count": len(script.split()) , "beats": beats,
                    "A": A, "B": B,
                })
    return cases


if __name__ == "__main__":
    cs = build()
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for c in cs:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(len(cs), "variants written to", OUT)

"""
game.py — Core game logic for "Everyone is a Detective"
========================================================
All game state, rules, and persistence live here in Python.
Flask (app.py) and the browser UI just call into this module.

REQUIRED PYTHON CONCEPTS — all demonstrated:
  * conditionals          -> if/elif/else throughout
  * containers            -> dict, list, tuple, set
  * loops                 -> for and while loops
  * flow and function     -> many functions with parameters/return values
  * classes and objects   -> Player, Suspect, Notebook, GameSession
  * flow control          -> break, continue, return, raise
  * file input/output     -> Notebook reads/writes notebook_<id>.txt
  * recursion             -> recursive name validator + recursive scoring
  * multi-dimensional     -> 2D suspect-vs-clue investigation matrix
"""

import os
import re
import uuid
from datetime import datetime

from plot import (
    CASE_TITLE, PROLOGUE, TRUE_CULPRIT, KEY_EVIDENCE,
    SUSPECTS, SCENE_ITEMS, WATSON_INTRO,
    ENDING_SUCCESS, ENDING_FAILURE,
)

# ============================================================
# CONSTANTS (containers: tuple)
# ============================================================
VALID_GENDERS = ("Mr.", "Miss", "Detective")
NOTEBOOK_DIR = "notebooks"
MAX_NAME_LEN = 20


# ============================================================
# Recursive name validator (RECURSION REQUIREMENT #1)
# ============================================================
def validate_name(name, attempts=0):
    """
    Recursively clean & validate the player's name.
    - Strips whitespace and collapses doubled spaces
    - Raises ValueError after 5 attempts or if invalid characters remain
    """
    if attempts >= 5:                                  # base case (failure)
        raise ValueError("Name could not be validated.")   # raise

    cleaned = name.strip()
    # Collapse doubled internal whitespace via recursion
    if "  " in cleaned:
        return validate_name(cleaned.replace("  ", " "), attempts + 1)  # recursion

    if len(cleaned) == 0 or len(cleaned) > MAX_NAME_LEN:
        raise ValueError(f"Name must be 1-{MAX_NAME_LEN} characters.")
    if not re.match(r"^[A-Za-z\s\.'-]+$", cleaned):
        raise ValueError("Name must contain only letters, spaces, ., ', or -.")

    return cleaned.title()                             # base case (success)


# ============================================================
# CLASSES (classes and objects requirement)
# ============================================================
class Player:
    """The player-detective."""

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def full_title(self):
        return f"Detective {self.name}"

    def to_dict(self):
        return {"name": self.name, "gender": self.gender,
                "title": self.full_title()}


class Suspect:
    """One suspect, built from plot.py data."""

    def __init__(self, name, data):
        self.name = name
        self.image = data["image"]
        self.description = data["description"]
        self.questions = dict(data["questions"])
        self.questioned = set()                        # container: set

    def ask(self, question):
        """Return the suspect's answer, or raise KeyError if unknown."""
        if question not in self.questions:
            raise KeyError(f"Unknown question for {self.name}: {question}")
        self.questioned.add(question)
        return self.questions[question]

    def question_list(self):
        return [(q, q in self.questioned) for q in self.questions.keys()]


class Notebook:
    """
    The Notebook — stores entries in memory AND persists to disk
    (FILE I/O REQUIREMENT).
    """

    def __init__(self, session_id, owner_name):
        os.makedirs(NOTEBOOK_DIR, exist_ok=True)
        self.session_id = session_id
        self.owner_name = owner_name
        self.filepath = os.path.join(NOTEBOOK_DIR, f"notebook_{session_id}.txt")
        self.entries = []                              # container: list

        with open(self.filepath, "w", encoding="utf-8") as f:    # file output
            f.write(f"Detective {owner_name}'s Notebook\n")
            f.write(f"Case: {CASE_TITLE}\n")
            f.write(f"Started: {datetime.now():%Y-%m-%d %H:%M}\n")
            f.write("=" * 50 + "\n\n")

    def add_entry(self, category, text):
        entry = {
            "category": category,
            "text": text,
            "time": datetime.now().strftime("%H:%M"),
        }
        self.entries.append(entry)
        with open(self.filepath, "a", encoding="utf-8") as f:    # file output
            f.write(f"[{entry['time']}] [{category}] {text}\n")

    def add_personal_thought(self, thought):
        thought = thought.strip()
        if not thought:
            return False
        if len(thought) > 500:
            thought = thought[:500] + "..."
        self.add_entry("THOUGHT", thought)
        return True

    def read_from_file(self):
        """Read the notebook back from disk (FILE INPUT REQUIREMENT)."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:    # file input
                return f.read()
        except FileNotFoundError:
            return "(Notebook file not yet created.)"

    def to_list(self):
        return list(self.entries)


# ============================================================
# Multi-dimensional list: suspect-vs-clue deduction matrix
# (MULTI-DIMENSIONAL LIST REQUIREMENT)
# ============================================================
def build_deduction_matrix(suspects, examined_items):
    """
    Returns a 2D list (rows = suspects, columns = scene items + question column).
    Each cell: 'X' (fully done), '~' (partial), '.' (not yet).
    """
    item_names = list(SCENE_ITEMS.keys())
    suspect_names = list(suspects.keys())

    rows = []
    for sname in suspect_names:                        # outer loop -> rows
        row = []
        for item in item_names:                        # inner loop -> cols
            if item in examined_items:
                row.append("X")
            else:
                row.append(".")
        # Final column: questioning thoroughness
        total = len(suspects[sname].questions)
        asked = len(suspects[sname].questioned)
        if asked == 0:
            row.append(".")
        elif asked < total:
            row.append("~")
        else:
            row.append("X")
        rows.append(row)

    short_items = [it.replace("the ", "").split()[0].title()
                   for it in item_names]
    return {
        "headers": short_items + ["Questioned"],
        "suspects": suspect_names,
        "rows": rows,                                  # ← 2D list
    }


# ============================================================
# Recursion #2 — recursive scoring of investigation progress
# ============================================================
def investigation_score(items, examined, index=0):
    """Recursively count how many items in `items` have been examined."""
    if index >= len(items):                            # base case
        return 0                                       # return
    contribution = 1 if items[index] in examined else 0
    return contribution + investigation_score(items, examined, index + 1)


# ============================================================
# GameSession — one playthrough
# ============================================================
class GameSession:
    """All state for one player's game."""

    _sessions = {}                                     # class-level registry

    @classmethod
    def get(cls, session_id):
        if session_id not in cls._sessions:
            raise KeyError(f"No session with id {session_id}")    # raise
        return cls._sessions[session_id]

    @classmethod
    def create(cls, raw_name, gender):
        name = validate_name(raw_name)
        if gender not in VALID_GENDERS:                # conditional
            raise ValueError(f"Invalid gender: {gender}")   # raise
        session = cls(name, gender)
        cls._sessions[session.id] = session
        return session

    def __init__(self, name, gender):
        self.id = uuid.uuid4().hex[:12]
        self.player = Player(name, gender)
        self.notebook = Notebook(self.id, name)
        self.suspects = {n: Suspect(n, d) for n, d in SUSPECTS.items()}
        self.examined_items = set()                    # container: set
        self.finished = False
        self.result = None
        self.ending_text = []

        self.notebook.add_entry("INFO", f"Detective {name} took the case.")
        self.notebook.add_entry("INFO", f"Case: {CASE_TITLE}")

    # ---- Player actions ----

    def ask_suspect(self, suspect_name, question):
        if suspect_name not in self.suspects:
            raise KeyError(f"No such suspect: {suspect_name}")
        suspect = self.suspects[suspect_name]
        answer = suspect.ask(question)
        self.notebook.add_entry(
            f"Q&A: {suspect_name}", f"Q: {question}  ->  A: {answer}"
        )
        return answer

    def examine_item(self, item_name):
        if item_name not in SCENE_ITEMS:
            raise KeyError(f"No such item: {item_name}")
        item = SCENE_ITEMS[item_name]
        self.examined_items.add(item_name)
        self.notebook.add_entry("CLUE", item["notebook_hint"])
        return item

    def add_thought(self, text):
        return self.notebook.add_personal_thought(text)

    def get_state(self):
        """Snapshot for the frontend."""
        suspect_state = []
        for sname, sobj in self.suspects.items():
            suspect_state.append({
                "name": sname,
                "image": sobj.image,
                "description": sobj.description,
                "questions": [
                    {"text": q, "asked": asked}
                    for q, asked in sobj.question_list()
                ],
            })

        item_state = []
        for iname, idata in SCENE_ITEMS.items():
            item_state.append({
                "name": iname,
                "short": idata["short"],
                "image": idata["image"],
                "examined": iname in self.examined_items,
            })

        # Recursion-based progress score
        score = investigation_score(list(SCENE_ITEMS.keys()), self.examined_items)
        questions_asked = sum(len(s.questioned) for s in self.suspects.values())
        questions_total = sum(len(s.questions) for s in self.suspects.values())
        matrix = build_deduction_matrix(self.suspects, self.examined_items)

        return {
            "session_id": self.id,
            "player": self.player.to_dict(),
            "case_title": CASE_TITLE,
            "suspects": suspect_state,
            "items": item_state,
            "items_examined": score,
            "items_total": len(SCENE_ITEMS),
            "questions_asked": questions_asked,
            "questions_total": questions_total,
            "matrix": matrix,
            "notebook_entries": self.notebook.to_list(),
            "finished": self.finished,
            "result": self.result,
            "ending_text": self.ending_text,
        }

    def get_prologue(self):
        return {
            "case_title": CASE_TITLE,
            "prologue": self._format_lines(PROLOGUE),
            "watson_intro": self._format_lines(WATSON_INTRO),
        }

    def _format_lines(self, lines):
        out = []
        for line in lines:                             # for loop
            if "{name}" in line or "{name_upper}" in line:    # conditional
                line = line.format(
                    name=self.player.name,
                    name_upper=self.player.name.upper(),
                )
            out.append(line)
        return out

    # ---- Final accusation ----

    def make_accusation(self, accused_culprit, accused_evidence):
        if self.finished:
            raise RuntimeError("This case is already closed.")
        if accused_culprit not in self.suspects:
            raise KeyError(f"Unknown suspect: {accused_culprit}")
        if accused_evidence not in SCENE_ITEMS:
            raise KeyError(f"Unknown evidence: {accused_evidence}")

        self.notebook.add_entry(
            "ACCUSATION",
            f"Accused {accused_culprit}; key evidence: {accused_evidence}",
        )

        culprit_ok = (accused_culprit == TRUE_CULPRIT)
        evidence_ok = (accused_evidence == KEY_EVIDENCE)

        # Demonstrate break/continue in flow control
        feedback = []
        check_pairs = [("culprit", culprit_ok), ("evidence", evidence_ok)]
        for kind, ok in check_pairs:                   # for loop
            if ok:
                continue                               # continue
            if kind == "culprit":
                feedback.append("The wrong person was accused.")
            else:
                feedback.append("The chosen evidence is not what convicts the killer.")
            break                                      # break

        if culprit_ok and evidence_ok:
            self.result = "win"
            self.ending_text = self._format_lines(ENDING_SUCCESS)
            self.notebook.add_entry("RESULT", "Case solved!")
        else:
            self.result = "lose"
            self.ending_text = self._format_lines(ENDING_FAILURE) + [""] + feedback
            self.notebook.add_entry(
                "RESULT", f"Case failed. {' '.join(feedback)}"
            )

        self.finished = True
        return self.result

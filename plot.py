"""
plot.py — Plot data for "Everyone is a Detective"
==================================================
All story content. Edit this file freely — the engine in game.py reads from
it without needing any code changes.

CASE: "The Ravenwood Manor Mystery"
"""

# ============================================================
# CASE BACKGROUND
# ============================================================
CASE_TITLE = "The Ravenwood Manor Mystery"

PROLOGUE = [
    "London, autumn of 1889. A thick fog rolls over the cobbled streets.",
    "",
    "Lord Edmund Ravenwood, a wealthy collector of rare antiquities, was found",
    "dead in the locked study of his country manor at precisely 11:47 PM last night.",
    "",
    "Cause of death: a single blow to the back of the head from a heavy object.",
    "No weapon has yet been located. The study window was open, but the ground",
    "below shows no footprints in the soft, rain-soaked earth.",
    "",
    "Three guests were staying at Ravenwood Manor that night:",
    "  • Miss Clara Hartwell, the deceased's young niece and sole heir",
    "  • Dr. Nigel Pembroke, an old friend and physician to Lord Ravenwood",
    "  • Mr. Silas Crowe, a rival antiquities dealer with a long-standing feud",
    "",
    "Inspector Lestrade of Scotland Yard has called upon you to assist. Your",
    "loyal partner Dr. Watson awaits you at the manor, notebook in hand.",
    "",
    "The fire crackles. The clock strikes midnight. The game is afoot."
]

# ============================================================
# TRUE SOLUTION
# ============================================================
TRUE_CULPRIT = "Dr. Nigel Pembroke"
KEY_EVIDENCE = "the doctor's medical bag"

# ============================================================
# SUSPECTS
# ============================================================
SUSPECTS = {
    "Miss Clara Hartwell": {
        "image": "clara.jpg",
        "description": (
            "A pale young woman in a black mourning dress. Her hands tremble "
            "slightly as she speaks. As sole heir, she stands to inherit the "
            "entire Ravenwood fortune — a fact she seems acutely aware of."
        ),
        "questions": {
            "Where were you at 11:47 PM last night?": (
                "“In the library, I believe. The fire had burned quite low by then, "
                "and I remember losing track of the hour entirely."
                "The butler brought me tea sometime after half past eleven — chamomile, "
                "though I scarcely touched it. I was attempting to read, but my thoughts "
                "were elsewhere."
                "I heard no cry. No struggle. Only the old house settling around me... "
                "and then, at midnight, the scream.”"
            ),
            "What was your relationship with Lord Ravenwood?": (
                "“Uncle Edmund could be difficult. Proud men often are."
                "After my parents died, this house became my entire world. "
                "He provided for me, educated me, protected me in his own stern fashion. "
                "But affection was never something he expressed easily."
                "Lately... we argued more than we once did. He disapproved of nearly everyone I trusted. "
                "Still, I never imagined...”\n\n"
                
                "She lowers her eyes."
                "“I never imagined the house without him in it.”"
            ),
            "Did you see anyone near the study?": (
                "“Dr. Pembroke passed through the corridor earlier in the evening. I remember hearing "
                "the clasp of his medical bag strike against the banister as he walked."
                "He said Uncle Edmund was having difficulty sleeping again."
                "After that... I’m less certain. At some point I thought I heard movement on the back staircase, "
                "slow footsteps, as though someone was trying not to be heard. "
                "But old houses create strange echoes at night.”"
            ),
            "Do you suspect anyone?": (
                "“Mr. Crowe argued bitterly with Uncle just last week over a Ming vase. "
                "I heard him shout, 'You'll regret this, Edmund!' But murder? I "
                "cannot say. Dr. Pembroke is so very calm — perhaps too calm.”"
            )
        }
    },
    "Dr. Nigel Pembroke": {
        "image": "pembroke.jpg",
        "description": (
            "A distinguished gentleman in his sixties with silver hair and the "
            "calm, measured manner of an experienced physician. He carries a "
            "worn leather medical bag and speaks with deliberate care."
        ),
        "questions": {
            "Where were you at 11:47 PM last night?": (
                "“At my age, Detective, one develops rather predictable habits. "
                "I retired shortly after eleven."
                "Edmund had requested a sleeping draught — nothing unusual, I assure you. "
                "He suffered dreadful insomnia whenever financial matters troubled him."
                "I spent perhaps half an hour reading in my room. Some medical journals, "
                "if memory serves. After that, I extinguished the lamp and slept rather poorly.”"
            ),
            "What was your relationship with Lord Ravenwood?": (
                "“Thirty years of friendship cannot be summarized in a sentence."
                "We travelled Egypt together as young men. We buried mutual friends. "
                "We survived scandals neither of us cared to speak of publicly."
                "Edmund was stubborn, reckless with money, and incapable of admitting weakness,"
                "but he was still my friend. Whatever others may imply.”"
            ),
            "Did you see anyone near the study?": (
                "“No one. The hallway was quite empty when I left Edmund's study "
                "at 11:15. Though I did notice that Miss Hartwell's library door "
                "was ajar — a small detail, perhaps.”"
            ),
            "May I examine your medical bag?": (
                "“My medical bag?”\n\n"
                "For the first time, the doctor pauses before answering.\n\n"
                "“Certainly, if procedure requires it. "
                "Though I confess I find the request rather peculiar. "
                "A physician’s bag contains little of interest to anyone outside the profession. "
                "Bottles, instruments, powders... the ordinary paraphernalia of a long career.”\n\n"
                "He adjusts his gloves carefully before continuing.\n\n"
                "“Still, I have nothing whatsoever to hide.”"
            )
        }
    },
    "Mr. Silas Crowe": {
        "image": "crowe.jpg",
        "description": (
            "A sharp-eyed man with a thin moustache and an expensive but "
            "ill-fitting suit. He smells faintly of tobacco and resentment, "
            "and his fingers drum impatiently on the chair arm."
        ),
        "questions": {
            "Where were you at 11:47 PM last night?": (
                "“In the garden, smoking a cigar — a habit Edmund would never "
                "permit indoors. I came in through the kitchen door at midnight "
                "and heard Miss Hartwell screaming. The cook saw me enter, if you "
                "doubt my word.”"
            ),
            "What was your relationship with Lord Ravenwood?": (
                "“Business rivals, nothing more. He outbid me on a Ming vase last "
                "week by spiteful means. I shouted some words I regret — but I do "
                "not kill men over porcelain, Detective. There are easier ways.”"
            ),
            "Did you see anyone near the study?": (
                "“From the garden I saw a light in the study window until about "
                "11:40, then it went out. A shadow moved across the curtain "
                "shortly before. I thought nothing of it at the time.”"
            ),
            "Why are you really here at the manor?": (
                "“Edmund invited me to discuss a truce. He owed money all over "
                "London and wished to settle our quarrel — ask Pembroke about the "
                "loan, if you don't believe me. Edmund was in worse straits than "
                "anyone knew.”"
            )
        }
    }
}

# ============================================================
# CRIME SCENE ITEMS — multiple ambiguous clues, not one obvious one
# ============================================================
SCENE_ITEMS = {
    "the heavy brass candlestick": {
        "image": "candlestick.jpg",
        "short": "A heavy brass candlestick stands on the desk.",
        "description": (
            "The brass candlestick is heavy enough to fracture bone if swung with force.\n\n"
            "Its polished surface gleams unnaturally brightly compared to the dustier objects nearby. "
            "Near the base is a dull reddish mark, thin as dried varnish. "
            "In dim light, it could almost be mistaken for blood.\n\n"
            "Yet the stain flakes beneath the fingernail like brittle sealing wax.\n\n"
            "Curiously, however, someone appears to have cleaned the candlestick very recently."
        ),
        "notebook_hint": (
            "Brass candlestick: heavy enough and has red smear. "
            "Recently polished — almost too clean. Suspicious."
        )
    },
    "the open study window": {
        "image": "window.jpg",
        "short": "The study window stands open to the night air.",
        "description": (
            "The window is open about a foot. The latch is undamaged — it was "
            "opened from the inside. The earth below is soft from rain, yet "
            "there are NO footprints whatsoever. No drag marks, no broken "
            "branches, nothing.\n\n"
            "Whoever 'escaped' through this window never touched the ground. "
            "This was almost certainly staged from within. Worth recording."
        ),
        "notebook_hint": (
            "Open window: NO footprints below despite soft earth. "
            "Latch opened from inside. The 'intruder' theory is staged — "
            "the killer is someone INSIDE the manor."
        )
    },
    "the half-finished letter on the desk": {
        "image": "letter.jpg",
        "short": "A half-finished letter lies on the desk, ink still wet.",
        "description": (
            "The handwriting grows increasingly uneven toward the final lines, "
            "as though Lord Ravenwood had been interrupted mid-thought:\n\n"
            "‘My dear Thornley — I have recently uncovered certain irregularities "
            "concerning the £5,000 claimed by Dr. P—. "
            "Matters are more troubling than I first believed. "
            "I fear the signature attached to the document may not be entirely genuine. "
            "I shall need to—’\n\n"
            "The sentence ends abruptly.\n\n"
            "Whether Ravenwood intended accusation, reconciliation, or something else "
            "entirely remains uncertain."
        ),
        "notebook_hint": (
            "Letter: Lord Ravenwood discovered Dr. Pembroke might FORGED his "
            "signature on a £5,000 loan. He was about to inform his solicitor. "
            "This might be Pembroke's motivation."
        )
    },
    "the antique letter-opener on the floor": {
        "image": "opener.jpg",
        "short": "A silver letter-opener lies on the rug near the desk.",
        "description": (
            "An ornate silver letter-opener, lying about three feet from the "
            "desk on the patterned rug. The tip is sharp. Most strikingly, "
            "there is a dark reddish stain along the blade, "
            "it looks like blood.\n\n"
            "But Lord Ravenwood did not die from a stab wound. He died from "
            "blunt-force trauma to the back of the head. And under closer "
            "inspection, the 'blood' is too brown, too thin, too uniform. "
            "These may not be real blood, these might be..."
            "The opener may have just been knocked off the desk during the struggle.\n\n"
            "May be a red herring, worth noting."
        ),
        "notebook_hint": (
            "Letter-opener: The 'blood' on the blade doesn't look like real blood. "
            "What could it be? "
            "Victim was BLUDGEONED, not stabbed. This is NOT the weapon. "
            "This might be a false lead."
        )
    },
    "the doctor's medical bag": {
        "image": "medbag.jpg",
        "short": "Dr. Pembroke's worn leather medical bag, taken from his room.",
        "description": (
            "Dr. Pembroke’s medical bag rests heavily upon the table, "
            "the dark leather softened and cracked by decades of use. "
            "A faint scent of antiseptic and tobacco clings to it.\n\n"
            "Inside are the expected tools of a country physician: "
            "folded bandages, neatly labelled vials, surgical scissors, "
            "and a small brass mortar and pestle tucked carefully beneath a cloth.\n\n"
            "The mortar is surprisingly weighty when lifted. Its polished "
            "surface reflects the firelight unevenly, interrupted here and "
            "there by darker discolorations lodged deep within the engraved seams, "
            "perhaps residue untouched by hurried cleaning, or perhaps merely tarnish from age.\n\n"
            "Nearby lies an empty vial labelled Chloral Hydrate. "
            "The dosage seems unusually strong for a simple sleeping draught, "
            "though whether this reflects desperation, carelessness, or routine medical "
            "practice is difficult to say.\n\n"
            "Nothing here proves violence. "
            "Yet something about the arrangement feels... recently disturbed."
        ),
        "notebook_hint": (
            "Medical bag: brass mortar is heavy, "
            "and has dark flecks in the seams (washed but not perfectly). "
            "Handkerchief faintly stained. Chloral hydrate vial empty — "
        )
    },
    "the muddy boots by the kitchen door": {
        "image": "boots.jpg",
        "short": "A pair of muddy gentlemen's boots stand by the kitchen door.",
        "description": (
            "A pair of muddy gentlemen's boots — Mr. Crowe's, by the size and "
            "make. The mud is fresh and consistent with the wet garden earth. "
            "There is a small reddish smear on the right boot, but this "
            "doesn't look much like bloodstains.\n\n"
            "The cook confirms Mr. Crowe entered through the kitchen at "
            "midnight, just after the discovery of the body. He could not "
            "easily have been in the study at 11:47 — but he was certainly "
            "outside, where he claims. A useful piece of corroboration."
        ),
        "notebook_hint": (
            "Crowe's boots: muddy, consistent with garden. Red smear might be "
            "BRICK DUST, not blood. His alibi (in the garden) is "
            "corroborated by the cook. Crowe is likely INNOCENT."
        )
    },
    "the empty teacup in the library": {
        "image": "teacup.jpg",
        "short": "An empty teacup sits on the library table beside a book.",
        "description": (
            "Miss Hartwell's teacup, half-drunk and now cold. The book beside "
            "it is open at page 142 — a volume of romantic poetry. The butler "
            "confirms he brought the tea at 11:30 and Miss Hartwell was "
            "reading when he left.\n\n"
            "The cup itself is unremarkable. A small dark drop on the saucer "
            "is, on testing with a damp cloth, simply spilt tea. Nothing "
            "incriminating here — if anything, it supports her story that "
            "she was in the library at the time of the murder."
        ),
        "notebook_hint": (
            "Library teacup: tea was indeed brought at 11:30 as Clara said. "
            "Butler corroborates. Dark drop on saucer is just spilt tea. "
            "Supports Clara's alibi."
        )
    }
}

# ============================================================
# WATSON INTRO & ENDINGS
# ============================================================
WATSON_INTRO = [
    "Dr. Watson greets you at the door of Ravenwood Manor.",
    "",
    "'Thank heavens you've arrived, Detective {name}! Inspector Lestrade is",
    "quite at a loss. The three suspects are gathered in the drawing room.",
    "The body has been left untouched in the study for your examination.'",
    "",
    "'Where shall we begin? You may question the suspects in any order, and",
    "examine each item at the crime scene. Use your notebook well — the truth",
    "is hidden in the details, and the details are many.'"
]

ENDING_SUCCESS = [
    "Dr. Watson stares in amazement.",
    "",
    "'Astounding, Detective {name}! You have unmasked the killer!'",
    "",
    "Dr. Pembroke's shoulders sag. 'Yes... yes, it was I. Edmund discovered",
    "I had forged his signature to take the £5,000 loan for myself. He was",
    "about to write to his solicitor and ruin me. I gave him a strong dose",
    "of chloral hydrate in the sleeping draught, then returned at 11:40 and",
    "struck him with the mortar from my own bag. I opened the window to feign",
    "an intruder, but I am no athlete — I never could have made it look real.'",
    "",
    "'Thirty years of friendship, destroyed by one moment of greed.'",
    "",
    "Inspector Lestrade claps his hands. 'A brilliant deduction, Detective {name}!'",
    "",
    "** CONGRATULATIONS DETECTIVE {name_upper}, CASE SOLVED! **"
]

ENDING_FAILURE = [
    "Dr. Watson lowers his eyes.",
    "",
    "'I'm afraid the evidence does not support that accusation, Detective {name}.'",
    "",
    "The true culprit slips quietly out the door into the London fog,",
    "never to be brought to justice.",
    "",
    "** CASE FAILED — THE CULPRIT ESCAPED! **"
]

# ============================================================
# ASSET MAPS — filenames in static/
# ============================================================
IMAGE_MAP = {
    "prologue":  "scenes/manor_exterior.jpg",
    "manor":     "scenes/manor_exterior.jpg",
    "study":     "scenes/study.jpg",
    "drawing":   "scenes/drawing_room.jpg",
}

AUDIO_MAP = {
    "ambient":   "ambient.wav",
    "click":     "click.wav",
    "page":      "page.wav",
    "discovery": "discovery.wav",
    "success":   "success.wav",
    "failure":   "failure.wav",
}

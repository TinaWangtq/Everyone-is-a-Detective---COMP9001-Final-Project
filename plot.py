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
                "I was in the library, reading by the fire. The butler brought me "
                "tea at 11:30. I heard nothing unusual until the scream at midnight. "
                "Though... I suppose no one can vouch for me after the tea arrived."
            ),
            "What was your relationship with Lord Ravenwood?": (
                "Uncle Edmund raised me after my parents died. We had our quarrels — "
                "he disapproved of my engagement to a man without fortune — but I "
                "loved him dearly. The inheritance means little compared to that."
            ),
            "Did you see anyone near the study?": (
                "I saw Dr. Pembroke in the hallway around 11:15, carrying his "
                "medical bag. He said Uncle Edmund had asked for a sleeping draught. "
                "Later, near midnight, I thought I heard footsteps on the back stairs."
            ),
            "Do you suspect anyone?": (
                "Mr. Crowe argued bitterly with Uncle just last week over a Ming vase. "
                "I heard him shout, 'You'll regret this, Edmund!' But murder? I "
                "cannot say. Dr. Pembroke is so very calm — perhaps too calm."
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
                "I retired to my guest room at 11 o'clock after delivering a "
                "sleeping draught to Edmund. I read for some time before sleeping. "
                "Of course, no one saw me — but a physician learns the value of rest."
            ),
            "What was your relationship with Lord Ravenwood?": (
                "We were the dearest of friends for thirty years. Why, only last "
                "month I lent him a considerable sum — a private matter between "
                "gentlemen. I see no reason to dwell on it now."
            ),
            "Did you see anyone near the study?": (
                "No one. The hallway was quite empty when I left Edmund's study "
                "at 11:15. Though I did notice that Miss Hartwell's library door "
                "was ajar — a small detail, perhaps."
            ),
            "May I examine your medical bag?": (
                "My bag? Whatever for? It contains only the usual instruments of "
                "my profession. I... I left it in my room. If you must, you must, "
                "but I think you waste your time on an old man's possessions."
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
                "In the garden, smoking a cigar — a habit Edmund would never "
                "permit indoors. I came in through the kitchen door at midnight "
                "and heard Miss Hartwell screaming. The cook saw me enter, if you "
                "doubt my word."
            ),
            "What was your relationship with Lord Ravenwood?": (
                "Business rivals, nothing more. He outbid me on a Ming vase last "
                "week by spiteful means. I shouted some words I regret — but I do "
                "not kill men over porcelain, Detective. There are easier ways."
            ),
            "Did you see anyone near the study?": (
                "From the garden I saw a light in the study window until about "
                "11:40, then it went out. A shadow moved across the curtain "
                "shortly before. I thought nothing of it at the time."
            ),
            "Why are you really here at the manor?": (
                "Edmund invited me to discuss a truce. He owed money all over "
                "London and wished to settle our quarrel — ask Pembroke about the "
                "loan, if you don't believe me. Edmund was in worse straits than "
                "anyone knew."
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
            "A solid brass candlestick on the desk. Heavy enough to be a weapon. "
            "Looking closely, you notice a faint reddish smear near its base — "
            "but on closer inspection, it appears to be old sealing wax, not "
            "blood. The candlestick is otherwise spotless, almost suspiciously "
            "so. A servant may have polished it this very morning.\n\n"
            "It may be worth noting in your book."
        ),
        "notebook_hint": (
            "Brass candlestick: red smear is OLD SEALING WAX, not blood. "
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
            "Lord Ravenwood was writing to his solicitor, Mr. Thornley. The ink "
            "trails off mid-sentence as if the writer were interrupted:\n\n"
            "  'My dear Thornley — I have decided to alter my will at once. The "
            "  matter of the £5,000 lent to me by Dr. P— has come to light in "
            "  a most disturbing way. I find that the signature on the loan "
            "  document is not mine, but a clever forgery. I shall need to —'\n\n"
            "The letter stops there. Whatever Lord Ravenwood was about to do "
            "regarding Dr. Pembroke, he never finished writing it.\n\n"
            "This letter is plainly important — record it carefully."
        ),
        "notebook_hint": (
            "Letter: Lord Ravenwood discovered Dr. Pembroke FORGED his "
            "signature on a £5,000 loan. He was about to inform his solicitor. "
            "MOTIVE for Pembroke — exposure and ruin."
        )
    },
    "the antique letter-opener on the floor": {
        "image": "opener.jpg",
        "short": "A silver letter-opener lies on the rug near the desk.",
        "description": (
            "An ornate silver letter-opener, lying about three feet from the "
            "desk on the patterned rug. The tip is sharp. Most strikingly, "
            "there is a dark reddish stain along the blade — at first glance, "
            "it looks like blood.\n\n"
            "But Lord Ravenwood did not die from a stab wound. He died from "
            "blunt-force trauma to the back of the head. And under closer "
            "inspection, the 'blood' is too brown, too thin, too uniform. "
            "It is red ink — the same ink Ravenwood used in his correspondence. "
            "The opener was simply knocked from the desk during the struggle.\n\n"
            "A red herring, but worth noting."
        ),
        "notebook_hint": (
            "Letter-opener: 'blood' on blade is actually RED INK. "
            "Victim was BLUDGEONED, not stabbed. This is NOT the weapon. "
            "A false lead."
        )
    },
    "the doctor's medical bag": {
        "image": "medbag.jpg",
        "short": "Dr. Pembroke's worn leather medical bag, taken from his room.",
        "description": (
            "With the constable's permission, you retrieve Dr. Pembroke's "
            "medical bag from his guest room. The leather is well-worn from "
            "years of use. Inside you find the usual implements: stethoscope, "
            "small glass vials, bandages, a brass mortar and pestle.\n\n"
            "The brass mortar is heavy — roughly the right shape and weight "
            "to cause the wound on Lord Ravenwood's head. Its base appears "
            "freshly washed, but the seams of the metalwork still hold a few "
            "dark flecks that water alone could not reach. The handkerchief "
            "wrapped around it bears a faint brown stain.\n\n"
            "There is also a small empty vial labelled 'Chloral hydrate' — a "
            "sleeping draught, in a dose far beyond what is medically wise.\n\n"
            "This may prove a very significant find. Record every detail."
        ),
        "notebook_hint": (
            "Medical bag: brass mortar is heavy, right shape for the wound, "
            "and has dark flecks in the seams (washed but not perfectly). "
            "Handkerchief faintly stained. Chloral hydrate vial empty — "
            "victim may have been drugged before the blow."
        )
    },
    "the muddy boots by the kitchen door": {
        "image": "boots.jpg",
        "short": "A pair of muddy gentlemen's boots stand by the kitchen door.",
        "description": (
            "A pair of muddy gentlemen's boots — Mr. Crowe's, by the size and "
            "make. The mud is fresh and consistent with the wet garden earth. "
            "There is a small reddish smear on the right boot, but it appears "
            "to be brick-dust from the garden path, not blood.\n\n"
            "The cook confirms Mr. Crowe entered through the kitchen at "
            "midnight, just after the discovery of the body. He could not "
            "easily have been in the study at 11:47 — but he was certainly "
            "outside, where he claims. A useful piece of corroboration."
        ),
        "notebook_hint": (
            "Crowe's boots: muddy, consistent with garden. Red smear is "
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

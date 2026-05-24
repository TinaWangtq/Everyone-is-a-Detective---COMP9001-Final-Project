# Everyone is a Detective

### Author: Tianqi Wang  |  Tutor: Niousha Nizomi

## Project Introduction

*Everyone is a Detective* is an interactive single-case mystery game. You play as a detective summoned to Ravenwood Manor on the night of a murder. You will question three suspects, examine evidence at the crime scene, record observations in your notebook, and ultimately deliver a final accusation naming both the killer and the one piece of evidence that conclusively convicts them.

The game is designed around classic deduction: not every suspicious detail is meaningful, and not every clue points to the truth. Some evidence is a red herring (red ink that looks like blood, behavior with an innocent explanation). The notebook records only what your detective observes — never the answer — so you must reason from the clues yourself.

---

## How to Run the Game

### Requirements

- Python 3.8 or newer
- A modern web browser (Chrome, Firefox, Edge, Safari)

### Start the Game
Download the zip file from GitHub, unzip it on the desktop or in the terminal, and use PyCharm or another compiler to open the folder.

Enter the following in the terminal to start the game:
```bash
pip install flask pillow numpy
python app.py                 # ← starts the game server
```

Then open **http://localhost:5000** in your browser.

---
## General Game Flow

💡 Tips: You can turn on the music to get a better immersive experience!

The game proceeds through these phases:

**1. Prologue.** You arrive at Ravenwood Manor. The opening sets the scene: Lord Edmund Ravenwood has been found dead in his study, and you have been called to investigate. You enter your detective name and choose a title (Mr., Miss, or Detective).

**2. Investigation.** This is the main phase, which you can explore freely:

- **Examine the crime scene.** Click any item at the scene to inspect it. Each examined item is added to your notebook.
- **Question the suspects.** Visit each of the three suspects and ask them from a list of available questions. Their answers go straight into your notebook, attributed to whoever you asked.
- **Record personal thoughts.** At any point you can write your own notes into the notebook (theories, suspicions, connections you've noticed).
- **Read your notebook.** Review every entry recorded so far — questions, answers, clues, and your own thoughts — to plan your next move.
- **Check the deduction matrix.** See at a glance who you still need to question and which evidence you still need to examine.

**3. Accusation.** When you feel ready, make your final accusation. You must name **two** things:

- **The culprit** — which of the three suspects committed the murder.
- **The key evidence** — the one item from the crime scene that conclusively proves their guilt.

**4. Ending.** If both choices are correct, you win and see the success ending. If either choice is wrong, you fail — and the game tells you whether you accused the wrong person, chose the wrong evidence, or both.






---
## Project structure

```
final_deject_game/
├── app.py                  # Flask server (thin HTTP layer)
├── game.py                 # Python game logic — all required concepts
├── plot.py                 # Story data — EDIT to change the case
├── requirements.txt
├── README.md
├── notebooks/              # Auto-generated per-game notebook .txt files
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    ├── js/app.js
    ├── images/
    │   ├── scenes/         # ← background scenes
    │   ├── suspects/       # ← suspect portraits
    │   └── items/          # ← evidence illustrations
    └── audio/              # ← music + sound effects
```

---

## About the case

You investigate the murder of Lord Edmund Ravenwood in his country
manor, autumn of 1889. Three suspects, seven items at the crime scene,
multiple red herrings.

To win, you must identify **both** the killer **and** the one piece of
evidence that conclusively convicts them. Try to spot the difference
between misleading details (red ink that looks like blood, suspicious
behavior that turns out to have an innocent explanation) and the truth.

The notebook records some observations, you must reason from the clues
yourself — the game won't tell you the answer.

Good luck, detective. The game is afoot. 🕵️

---

## COMP9001 Concepts Used
- Variables, Data Types and Interactive Programs
- Conditionals
- Containers
- Loops
- Functions
- Classes & objects 
- Flow Control (break/continue/return/raise) 
- File I/O
- Recursion
- Multi-dimensional list

### The main applications of advanced concepts
| Flow Control | All four in `make_accusation` |

| File I/O | `Notebook.__init__`, `add_entry`, `read_from_file` |

| Recursion | `validate_name` (recursive cleaner) + `investigation_score` |

| Multi-dimensional list | `build_deduction_matrix` returns 3×8 list |

---

### Usage of AI

When completing this task, I used Claude and ChatGPT as artificial intelligence assistants for modifying project code and resolving bugs; Use Dou Bao to generate various images.
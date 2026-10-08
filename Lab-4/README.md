# Software Engineering Lab 4 — Space Invaders Submission
**Student Name:** Samrudh Patil  
**SRN:** PES1UG24CS417  
**Course:** Software Engineering (Sem 5)  

## 📌 Deliverable Links
- **Before Video (10s Bug Demo):** [Google Drive Link](https://drive.google.com/file/d/1R_IrPNGwi9eg_aFYdjUfJbezwhTbwlVu/view?usp=sharing)
- **After Video (10s Full Features):** [Google Drive Link](https://drive.google.com/file/d/1jJZSjnTkJWDD3AQW97pUZ67wQdE-Kwy0/view?usp=sharing)
- **Submission Report PDF:** [Lab4_PES1UG24CS417.pdf](./Lab4_PES1UG24CS417.pdf)

## 📋 Task Commit History
| Task | Commit Hash | Message | Description |
| :--- | :---: | :--- | :--- |
| **Task 1** | [`5e2575a`](https://github.com/Samrudh7-0045/SE-Labs-PES1UG24CS417/commit/5e2575a) | `Task 1: Fix bullet collision detection via shallow copy iteration` | Solved list mutation bug during iteration using `self.player_bullets[:]` |
| **Task 2** | [`632e242`](https://github.com/Samrudh7-0045/SE-Labs-PES1UG24CS417/commit/632e242) | `Task 2: Implement graphical Game Over screen and final score display` | Added translucent modal dialog, GAME OVER title, and score display |
| **Task 3** | [`ff39973`](https://github.com/Samrudh7-0045/SE-Labs-PES1UG24CS417/commit/ff39973) | `Task 3: Add replay options with Easy, Medium, and Hard difficulty presets` | Added difficulty presets (Easy, Medium, Hard), HUD badge, and replay hotkeys |
| **Task 4** | [`ee8e464`](https://github.com/Samrudh7-0045/SE-Labs-PES1UG24CS417/commit/ee8e464) | `Task 4: Add retro 8-bit sound effects for shooting, enemy destroy, and game over` | Added synthesized 8-bit audio effects for firing, explosions, and game over |

---

# Original Space Invaders Game Description

## What’s Provided

A partially working version of a Space Invaders game with:

- A player-controlled ship that moves and shoots
- A grid of enemies that marches side to side and drops down at the edges
- Enemies that occasionally return fire
- Score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> Bullets sometimes pass straight through enemies without registering a hit, especially when firing rapidly or when two enemies are hit close together. Investigate and enhance collision accuracy.


### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the player is hit or the enemies reach the bottom of the screen, then gracefully waits for input instead of just printing to the console.



### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard enemy speed/fire rate), or exit.



### Task 4: Add Sound Feedback

> Add basic sound effects for firing, an enemy being destroyed, and the game-over moment.


---

## Expected Behavior

- Smooth player movement using `Left`/`Right` or `A`/`D`, and shooting with `Space`
- Enemy grid marches side to side and drops down whenever it reaches a screen edge
- Enemies occasionally fire back at the player
- Score increases each time an enemy is destroyed
- Game ends when the player is hit by an enemy bullet or the enemy grid reaches the bottom of the screen

---

## Folder Structure

```
space-invaders-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── player.py
│   ├── enemy.py
│   └── bullet.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history

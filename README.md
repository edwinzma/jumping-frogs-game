# jumping-frogs-game
A fun math puzzle game about jumping frogs, where n frogs jump n lily pads. The goal of the game is to get all frogs onto the same lily pad


# Jumping Frogs

A small and fun puzzle game built in Python with Pygame.

🎮 **Play it in your browser:**
https://edwinzma.github.io/jumping-frogs-game/

This is still an early prototype, so the visuals and interface are deliberately simple.

## How to Play

You will see a row of frogs standing on lily pads, represented by green platforms.

Your goal is to move all frogs onto a single lily pad.

To move frogs:

1. Move the arrow above the group of frogs you want to select.
2. Press **Down** to select them.
3. Press **Left** or **Right** to move them.

You may only move onto a lily pad that already contains at least one frog. You cannot land on an empty lily pad.

Once all frogs are gathered on a single lily pad, the next level starts automatically.

## Movement Rules

The number of frogs you select determines how far they move:

* 1 frog → 1 lily pad
* 2 frogs → 3 lily pads
* 3 frogs → 5 lily pads
* 4 frogs → 7 lily pads
* and so on

In general, a group of **n frogs moves 2n − 1 lily pads**.

## Controls

* **Left Arrow** — Move the selector one lily pad left
* **Right Arrow** — Move the selector one lily pad right
* **Down Arrow** — Select frog(s)
* **Up Arrow** — Deselect
* **Z** — Undo your last movement
* **R** — Restart the current level

## What I learned from this project

-How to use git and gitHub. How add, commit and push work. What branching is.
-How to use Pygame
-How to build a webapp using pygbag and asyncio.

## Next steps in this project

-Replace the lily pads with an image
-Show a win screen
- Put up a home screen
- Add different levels with special rules, such as a final lily pad. Or levels where some lily pads are empty at the start of the level etc.



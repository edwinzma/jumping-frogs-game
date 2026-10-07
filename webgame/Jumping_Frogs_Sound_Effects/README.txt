JUMPING FROGS — SOUND EFFECTS

14 original synthesized effects for a friendly cartoon pond.
Format: OGG Vorbis, 44.1 kHz, mono. Short one-shot effects, not loops.
Designed to accompany Lily Pad Hop; no recorded or sampled animal audio.

CONTENTS / PREVIEW ORDER
01. select_01.ogg (0.41s) — A short questioning ribbit for selecting a frog group.
02. select_02.ogg (0.39s) — A slightly lower variation of the selection ribbit.
03. jump_01.ogg (0.29s) — A springy boip and soft swish; variation 1.
04. jump_02.ogg (0.31s) — A springy boip and soft swish; variation 2.
05. jump_03.ogg (0.32s) — A springy boip and soft swish; variation 3.
06. land_small.ogg (0.35s) — A soft watery landing plop; small frog group, deeper at larger sizes.
07. land_medium.ogg (0.39s) — A soft watery landing plop; medium frog group, deeper at larger sizes.
08. land_large.ogg (0.42s) — A soft watery landing plop; large frog group, deeper at larger sizes.
09. merge_small.ogg (0.47s) — A happy double croak after groups merge.
10. merge_large.ogg (0.50s) — A deeper happy croak for a larger merged group.
11. invalid_move.ogg (0.30s) — A gentle descending rrup for an unavailable move.
12. undo.ogg (0.37s) — An upward sliding bubble for reversing a move.
13. menu_click.ogg (0.17s) — A tiny bubble pop for menu buttons.
14. level_complete.ogg (1.95s) — Two happy croaks and a C-major bell flourish to match Lily Pad Hop.

SUGGESTED USE
Choose select_01 or select_02 randomly. Do the same for the three jumps.
Use land_small, land_medium, or land_large for increasing group sizes.
Play jump on takeoff and land when the frogs touch the pad.
Use merge sparingly; a croak on every landing may become repetitive.
Play level_complete once, when the win condition becomes true.
Start effects around 0.5 volume and music around 0.2; adjust to taste.
Music and effects have separate volume controls in Pygame.

BASIC PYGAME USAGE
After pygame.init():
    jump_sound = pygame.mixer.Sound("sounds/jump_01.ogg")
    jump_sound.set_volume(0.5)
When a valid jump starts:
    jump_sound.play()

Load effects once during setup, not inside the frame loop.
These effects use Sound; keep mixer.music for the background music.

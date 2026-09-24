import pygame as pg

class HowToPlay:
    """Three tutorial pages, drawn with text and the game's existing sprites."""

    def __init__(self, pond, frog, lilypad):
        self.pond = pond
        # Scale once, rather than resizing images on every frame.
        self.frog = pg.transform.smoothscale(frog, (76, 76))
        self.lilypad = pg.transform.smoothscale(lilypad, (132, 46))
        self.title_font = pg.font.Font(None, 56)
        self.body_font = pg.font.Font(None, 34)
        self.small_font = pg.font.Font(None, 27)
        self.menu_rect = pg.Rect(64, 624, 200, 54)
        self.back_rect = pg.Rect(824, 624, 170, 54)
        self.next_rect = pg.Rect(1010, 624, 206, 54)
        self.reset()

    def reset(self):
        self.page = 0
        self.example_step = 0

    def advance(self):
        if self.page < 2:
            self.page += 1
        elif self.example_step < 3:
            self.example_step += 1
        else:
            return "home"
        return None

    def back(self):
        if self.page == 2 and self.example_step > 0:
            self.example_step -= 1
        elif self.page > 0:
            self.page -= 1

    def handle_event(self, event):
        # Return a new game state only when leaving the tutorial.
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_ESCAPE, pg.K_m):
                return "home"
            if event.key == pg.K_LEFT:
                self.back()
            elif event.key in (pg.K_RIGHT, pg.K_SPACE, pg.K_RETURN):
                return self.advance()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_rect.collidepoint(event.pos):
                return "home"
            if self.back_rect.collidepoint(event.pos):
                self.back()
            elif self.next_rect.collidepoint(event.pos):
                return self.advance()
        return None

    def text(self, screen, message, center, small=False, title=False,
             color=(31, 65, 43)):
        font = self.title_font if title else self.small_font if small else self.body_font
        surface = font.render(message, True, color)
        screen.blit(surface, surface.get_rect(center=center))

    def button(self, screen, rect, label, enabled=True):
        hovered = rect.collidepoint(pg.mouse.get_pos())
        color = (61, 126, 70) if hovered else (37, 91, 53)
        if not enabled:
            color = (139, 150, 133)
        pg.draw.rect(screen, color, rect, border_radius=14)
        self.text(screen, label, rect.center, color=(255, 250, 226))

    def board(self, screen, counts, centers, y, selected=None, targets=()):
        """Draw a small example without changing the real game's board."""
        for index, (count, x) in enumerate(zip(counts, centers)):
            if index in targets:
                pg.draw.ellipse(screen, (39, 164, 219), (x-77, y-29, 154, 58), 4)
                pg.draw.ellipse(screen, (128, 216, 242), (x-85, y-35, 170, 70), 2)
            screen.blit(self.lilypad, self.lilypad.get_rect(center=(x, y)))
            for height in range(count-1, -1, -1):
                rect = self.frog.get_rect(midbottom=(x, y-5-height*30))
                screen.blit(self.frog, rect)
            self.text(screen, str(count), (x, y+43), small=True)
            if index == selected:
                tip_y = y-92-max(0, count-1)*30
                pg.draw.line(screen, (35, 64, 42), (x, tip_y-26), (x, tip_y-7), 5)
                pg.draw.polygon(screen, (35, 64, 42),
                                [(x-10, tip_y-12), (x+10, tip_y-12), (x, tip_y)])

    def draw(self, screen):
        screen.blit(self.pond, (0, 0))
        pg.draw.rect(screen, (255, 249, 222), (40, 28, 1200, 578), border_radius=24)
        pg.draw.rect(screen, (77, 119, 59), (40, 28, 1200, 578), 3, border_radius=24)
        titles = ["Your goal", "How far can frogs jump?", "A four-frog example"]
        self.text(screen, titles[self.page], (640, 78), title=True)
        self.text(screen, f"HOW TO PLAY  |  {self.page+1} / 3", (640, 120), small=True)

        if self.page == 0:
            self.text(screen, "Get all frogs onto one lily pad.", (640, 172))
            self.board(screen, [1, 1, 1, 1], [145, 285, 425, 565], 372)
            self.board(screen, [4, 0, 0, 0], [735, 875, 1015, 1155], 372)
            pg.draw.line(screen, (37, 91, 53), (627, 329), (662, 329), 5)
            pg.draw.polygon(screen, (37, 91, 53), [(652, 319), (669, 329), (652, 339)])
            self.text(screen, "Start: frogs on separate pads", (355, 448))
            self.text(screen, "Goal: all frogs together", (945, 448))
            self.text(screen, "Move the selector with Left / Right. Press Down to select frogs.", (640, 514))
            self.text(screen, "Then press Left / Right to jump. Press Up to deselect.", (640, 552))

        elif self.page == 1:
            self.text(screen, "All frogs on the selected pad jump together.", (640, 170))
            self.board(screen, [1, 2, 3], [275, 640, 1005], 350)
            for x, label in zip([275, 640, 1005],
                                ["1 frog: 1 space", "2 frogs: 3 spaces", "3 frogs: 5 spaces"]):
                self.text(screen, label, (x, 422))
            self.text(screen, "The rule: n frogs jump exactly 2n - 1 spaces, left or right.", (640, 466))
            pg.draw.rect(screen, (255, 222, 135), (95, 499, 1090, 82), border_radius=14)
            self.text(screen, "Only land on a pad that already contains a frog.", (640, 524))
            self.text(screen, "Count every space, including empty pads you jump over.", (640, 555), small=True)

        else:
            states = [[1, 1, 1, 1], [1, 1, 0, 2], [3, 1, 0, 0], [4, 0, 0, 0]]
            captions = ["Select the third frog. Jump 1 space to the right.",
                        "Now select the pair on the right. Jump 3 spaces to the left.",
                        "Select the last single frog. Jump 1 space to the left.",
                        "All four frogs are together. You win!"]
            selected = [2, 3, 1, None][self.example_step]
            targets = [(1, 3), (0,), (0,), ()][self.example_step]
            self.text(screen, captions[self.example_step], (640, 178))
            self.board(screen, states[self.example_step], [295, 525, 755, 985],
                       402, selected=selected, targets=targets)
            self.text(screen, "Blue ripples show the possible landing pads.", (640, 481), small=True)
            self.text(screen, "Click Next move to see what happens." if self.example_step < 3
                      else "Ready to try it in the game?", (640, 516))
            self.text(screen, "In the game: Z = undo    R = restart    M = main menu", (640, 560), small=True)

        self.button(screen, self.menu_rect, "Main menu")
        self.button(screen, self.back_rect, "Back", self.page > 0)
        label = "Next page" if self.page < 2 else "Next move" if self.example_step < 3 else "Done"
        self.button(screen, self.next_rect, label)
        self.text(screen, "Left / Right: browse   |   Esc: menu", (543, 651), small=True,
                  color=(255, 255, 255))
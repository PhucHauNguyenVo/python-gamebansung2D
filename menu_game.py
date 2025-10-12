# menu_game.py
import pygame

class MenuTroChoi:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.state = "menu"  # menu | playing | gameover

        self.start_button = pygame.Rect(300, 220, 200, 60)
        self.retry_button = pygame.Rect(300, 300, 200, 60)

    def ve_menu(self):
        self.screen.fill((20, 20, 30))
        title = self.font.render("HOLDING OUT - DEMO", True, (255, 255, 255))
        self.screen.blit(title, (220, 140))

        pygame.draw.rect(self.screen, (50, 200, 50), self.start_button)
        t = self.font.render("START", True, (0, 0, 0))
        self.screen.blit(t, (self.start_button.x + 60, self.start_button.y + 12))

        # Quit hint
        hint = self.font.render("ESC to quit", True, (180,180,180))
        self.screen.blit(hint, (300, 320))

    def ve_thua_cuoc(self):
        self.screen.fill((40, 10, 10))
        title = self.font.render("GAME OVER", True, (255, 80, 80))
        self.screen.blit(title, (300, 140))

        pygame.draw.rect(self.screen, (220, 200, 0), self.retry_button)
        t = self.font.render("PLAY AGAIN", True, (0, 0, 0))
        self.screen.blit(t, (self.retry_button.x + 20, self.retry_button.y + 12))

    def xu_ly_click(self, pos):
        if self.state == "menu":
            if self.start_button.collidepoint(pos):
                self.state = "playing"
        elif self.state == "gameover":
            if self.retry_button.collidepoint(pos):
                self.state = "playing"

    # Alias tiếng Anh để tương thích với mã hiện có
    draw_menu = ve_menu
    draw_gameover = ve_thua_cuoc
    handle_click = xu_ly_click

# Alias tên lớp để tương thích với import cũ
GameMenu = MenuTroChoi

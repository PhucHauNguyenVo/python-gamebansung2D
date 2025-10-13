import pygame
from typing import List, Tuple
from . import items

class ItemManager:
	def __init__(self):
		self.items: List[items.Item] = []
		# lazy font will be created on first draw to avoid requiring pygame.font.init() here
		self._font = None

	def spawn(self, kind: str, pos: Tuple[int,int], **kwargs):
		# kind: "health", "shield", or custom class name
		if kind == "health":
			# ensure health potions restore exactly 1 and don't increase max
			kwargs.setdefault("amount", 1)
			it = items.HealthPotion(pos, **kwargs)
		elif kind == "shield":
			it = items.ShieldItem(pos, **kwargs)
		else:
			# try to resolve from items module
			cls = getattr(items, kind, None)
			if cls:
				it = cls(pos, **kwargs)
			else:
				raise ValueError(f"Unknown item kind: {kind}")
		self.items.append(it)
		return it

	def update(self, dt: float):
		for it in list(self.items):
			it.update(dt)
			# optional lifetime removal if flagged picked
			if getattr(it, "picked", False):
				try:
					self.items.remove(it)
				except ValueError:
					pass

	def draw(self, surface: pygame.Surface):
		# create font lazily
		if self._font is None:
			# default size; items may override via item.label_size
			try:
				self._font = pygame.font.Font(None, 16)
			except Exception:
				# fallback to SysFont
				self._font = pygame.font.SysFont(None, 16)

		for it in self.items:
			it.draw(surface)

			# determine label to draw (explicit label property preferred)
			label = getattr(it, "label", None)
			if label is None:
				# default labels for common items
				if isinstance(it, items.HealthPotion):
					label = f"+{getattr(it, 'amount', 1)}"
				elif isinstance(it, items.ShieldItem):
					label = "Shield"
			if not label:
				continue

			# allow custom size/color per item
			label_size = getattr(it, "label_size", None)
			if label_size:
				try:
					font = pygame.font.Font(None, label_size)
				except Exception:
					font = pygame.font.SysFont(None, label_size)
			else:
				font = self._font

			color = getattr(it, "label_color", (255,255,255))
			# render with a thin shadow for readability
			text_surf = font.render(str(label), True, color)
			shadow = font.render(str(label), True, (0,0,0))
			# center text on item rect
			rect = text_surf.get_rect(center=it.rect.center)
			shadow_rect = shadow.get_rect(center=(it.rect.centerx+1, it.rect.centery+1))
			surface.blit(shadow, shadow_rect)
			surface.blit(text_surf, rect)

	def check_pickups(self, player) -> List[items.Item]:
		"""
		Gọi trong loop: nếu va chạm với player.rect -> apply_to và trả về list đã pickup.
		Yêu cầu player có thuộc tính rect (pygame.Rect).
		"""
		picked = []
		if not hasattr(player, "rect"):
			return picked
		for it in list(self.items):
			if it.rect.colliderect(player.rect):
				# special handling for HealthPotion: only consume if player below base health
				if isinstance(it, items.HealthPotion):
					# base health priority: player.base_health -> player.max_health -> default 3
					base = getattr(player, "base_health", getattr(player, "max_health", 3))
					cur = getattr(player, "health", None)

					if cur is None:
						# try heal method if present
						if hasattr(player, "heal") and callable(player.heal):
							player.heal(1)
							it.picked = True
							picked.append(it)
							try: self.items.remove(it)
							except ValueError: pass
						else:
							# set health attribute to min(base,1)
							setattr(player, "health", min(base, 1))
							it.picked = True
							picked.append(it)
							try: self.items.remove(it)
							except ValueError: pass
					else:
						if cur < base:
							# heal exactly 1, not exceeding base
							if hasattr(player, "heal") and callable(player.heal):
								player.heal(1)
							else:
								player.health = min(base, cur + 1)
							it.picked = True
							picked.append(it)
							try: self.items.remove(it)
							except ValueError: pass
						else:
							# player already at base/max health -> do not consume potion
							pass
				else:
					# default behavior for other items
					it.apply_to(player)
					it.picked = True
					picked.append(it)
					try:
						self.items.remove(it)
					except ValueError:
						pass
		return picked
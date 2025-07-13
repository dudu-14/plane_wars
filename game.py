#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""游戏主逻辑模块。

本模块包含游戏的核心逻辑，包括游戏状态管理、事件处理、
碰撞检测、渲染等功能。Game类是整个游戏的控制中心。

典型用法示例:
    game = Game()
    game.run()  # 开始游戏主循环
"""

import pygame
import random
import sys
from typing import List, Optional
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, GREEN, YELLOW,
    PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_SPAWN_RATE,
    ENEMY_SMALL_WIDTH, ENEMY_MEDIUM_WIDTH, AUTO_FIRE,
    SOUND_ENABLED, SOUND_VOLUME, SHOOT_SOUND_INTERVAL
)
from player import Player
from enemy import Enemy, EnemyType
from bullet import Bullet
from sound_manager import SoundManager


class Game:
    """游戏主类。

    负责管理整个游戏的运行，包括初始化、事件处理、游戏逻辑更新、
    渲染等核心功能。这是游戏的控制中心。

    Attributes:
        screen (pygame.Surface): 游戏主窗口表面
        clock (pygame.time.Clock): 游戏时钟，用于控制帧率
        running (bool): 游戏是否正在运行
        game_over (bool): 游戏是否结束
        score (int): 玩家当前分数
        player (Player): 玩家飞机对象
        enemies (List[Enemy]): 敌机列表
        player_bullets (List[Bullet]): 玩家子弹列表
        enemy_bullets (List[Bullet]): 敌机子弹列表
        font (pygame.font.Font): 普通字体
        big_font (pygame.font.Font): 大号字体
    """

    def __init__(self) -> None:
        """初始化游戏。

        设置游戏窗口、初始化游戏状态、创建玩家对象和各种游戏对象列表。
        """
        # 创建游戏窗口
        self.screen: pygame.Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption("飞机大战")

        # 创建时钟对象用于控制帧率
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # 游戏状态变量
        self.running: bool = True
        self.game_over: bool = False
        self.score: int = 0
        self.shoot_sound_counter: int = 0  # 射击音效计数器

        # 创建玩家飞机（位于屏幕底部中央）
        player_x: int = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        player_y: int = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.player: Player = Player(player_x, player_y)

        # 初始化游戏对象列表
        self.enemies: List[Enemy] = []
        self.player_bullets: List[Bullet] = []
        self.enemy_bullets: List[Bullet] = []

        # 初始化字体对象（使用最兼容的方法）
        pygame.font.init()  # 确保字体模块已初始化

        # 尝试多种字体，找到可用的
        self.font = None
        self.big_font = None

        # 字体候选列表
        font_candidates = [
            lambda: pygame.font.SysFont('arial', 36),
            lambda: pygame.font.SysFont('helvetica', 36),
            lambda: pygame.font.SysFont('calibri', 36),
            lambda: pygame.font.SysFont('verdana', 36),
            lambda: pygame.font.Font(None, 36),
        ]

        big_font_candidates = [
            lambda: pygame.font.SysFont('arial', 72),
            lambda: pygame.font.SysFont('helvetica', 72),
            lambda: pygame.font.SysFont('calibri', 72),
            lambda: pygame.font.SysFont('verdana', 72),
            lambda: pygame.font.Font(None, 72),
        ]

        # 尝试找到可用的普通字体
        for font_func in font_candidates:
            try:
                test_font = font_func()
                # 测试渲染
                test_surface = test_font.render("Test", True, WHITE)
                self.font = test_font
                break
            except:
                continue

        # 尝试找到可用的大字体
        for font_func in big_font_candidates:
            try:
                test_font = font_func()
                # 测试渲染
                test_surface = test_font.render("Test", True, WHITE)
                self.big_font = test_font
                break
            except:
                continue

        # 如果所有字体都失败，设置为None（将使用图形替代）
        if self.font is None:
            print("Warning: No fonts available, using graphics fallback")
        if self.big_font is None:
            print("Warning: No big fonts available, using graphics fallback")

        # 初始化音效管理器
        self.sound_manager: SoundManager = SoundManager(
            enabled=SOUND_ENABLED,
            volume=SOUND_VOLUME
        )

    def handle_events(self) -> None:
        """处理游戏事件。

        处理用户输入和系统事件，包括退出游戏、发射子弹、重新开始等。
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 用户点击关闭按钮
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and not AUTO_FIRE:
                    # 空格键发射子弹（仅在非自动发射模式且游戏进行中）
                    self._handle_player_shoot()
                elif event.key == pygame.K_r and self.game_over:
                    # R键重新开始游戏（仅在游戏结束时）
                    self.restart_game()

    def _handle_player_shoot(self) -> None:
        """处理玩家发射子弹。

        检查玩家是否可以发射子弹，如果可以则创建新的子弹对象并播放音效。
        """
        bullet_pos: Optional[tuple[int, int]] = self.player.shoot()
        if bullet_pos:
            bullet: Bullet = Bullet(bullet_pos[0], bullet_pos[1], "player")
            self.player_bullets.append(bullet)

            # 播放射击音效（每隔几发播放一次，避免音效过于密集）
            self.shoot_sound_counter += 1
            if self.shoot_sound_counter >= SHOOT_SOUND_INTERVAL:
                self.sound_manager.play_shoot()
                self.shoot_sound_counter = 0

    def spawn_enemies(self) -> None:
        """生成敌机。

        根据设定的概率随机生成敌机。敌机类型和位置都是随机的，
        小型敌机的生成概率比中型敌机更高。
        """
        if random.random() < ENEMY_SPAWN_RATE:
            # 随机选择敌机类型（70%概率生成小型敌机）
            enemy_type: EnemyType = "small" if random.random() < 0.7 else "medium"

            # 根据敌机类型随机生成x坐标
            if enemy_type == "small":
                max_x: int = SCREEN_WIDTH - ENEMY_SMALL_WIDTH
            else:
                max_x = SCREEN_WIDTH - ENEMY_MEDIUM_WIDTH

            enemy_x: int = random.randint(0, max_x)

            # 创建敌机（从屏幕上方进入）
            enemy: Enemy = Enemy(enemy_x, -50, enemy_type)
            self.enemies.append(enemy)

            # 播放敌机出现音效
            self.sound_manager.play_enemy_spawn()

    def update_bullets(self) -> None:
        """更新所有子弹。

        更新玩家子弹和敌机子弹的位置，移除飞出屏幕的子弹以节省内存。
        使用切片副本遍历列表，避免在遍历过程中修改列表导致的问题。
        """
        # 更新玩家子弹
        for bullet in self.player_bullets[:]:  # 使用切片副本
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)

        # 更新敌机子弹
        for bullet in self.enemy_bullets[:]:  # 使用切片副本
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)

    def update_enemies(self) -> None:
        """更新所有敌机。

        更新敌机位置，处理敌机发射子弹，移除飞出屏幕的敌机。
        当敌机飞出屏幕时，玩家会失去一条生命。
        """
        for enemy in self.enemies[:]:  # 使用切片副本
            enemy.update()

            # 检查敌机是否飞出屏幕
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
                # 敌机逃脱，玩家失去一条生命
                self.player.take_damage()
                continue

            # 处理敌机发射子弹
            self._handle_enemy_shoot(enemy)

    def _handle_enemy_shoot(self, enemy: Enemy) -> None:
        """处理敌机发射子弹。

        检查敌机是否发射子弹，如果发射则创建新的敌机子弹对象。

        Args:
            enemy (Enemy): 要检查的敌机对象
        """
        bullet_pos: Optional[tuple[int, int]] = enemy.shoot()
        if bullet_pos:
            bullet: Bullet = Bullet(bullet_pos[0], bullet_pos[1], "enemy")
            self.enemy_bullets.append(bullet)

    def check_collisions(self) -> None:
        """检查所有碰撞。

        检查玩家子弹与敌机、敌机子弹与玩家、敌机与玩家之间的碰撞，
        并处理相应的游戏逻辑（伤害、得分、对象移除等）。
        """
        self._check_player_bullet_enemy_collision()
        self._check_enemy_bullet_player_collision()
        self._check_enemy_player_collision()

    def _check_player_bullet_enemy_collision(self) -> None:
        """检查玩家子弹与敌机的碰撞。

        当玩家子弹击中敌机时，子弹消失，敌机受伤。
        如果敌机生命值归零，则敌机被摧毁，玩家获得分数。
        """
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    # 移除子弹
                    self.player_bullets.remove(bullet)
                    # 敌机受伤
                    enemy.take_damage()
                    if not enemy.is_alive():
                        # 敌机被摧毁，增加分数并移除敌机
                        self.score += enemy.score
                        self.enemies.remove(enemy)
                        # 播放击杀音效
                        self.sound_manager.play_enemy_kill()
                    break  # 子弹已被移除，跳出内层循环

    def _check_enemy_bullet_player_collision(self) -> None:
        """检查敌机子弹与玩家的碰撞。

        当敌机子弹击中玩家时，子弹消失，玩家受伤。
        """
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(bullet)
                self.player.take_damage()
                break  # 只处理一颗子弹的碰撞

    def _check_enemy_player_collision(self) -> None:
        """检查敌机与玩家的碰撞。

        当敌机直接撞击玩家时，敌机消失，玩家受伤。
        """
        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.player.rect):
                self.enemies.remove(enemy)
                self.player.take_damage()
                break  # 只处理一个敌机的碰撞

    def update_game(self) -> None:
        """更新游戏状态。

        在游戏进行中时，更新所有游戏对象的状态，包括玩家、敌机、子弹等。
        检查碰撞并处理游戏结束条件。
        """
        if not self.game_over:
            # 获取当前按键状态
            keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

            # 更新玩家状态
            self.player.update(keys_pressed)

            # 自动发射子弹（如果启用）
            if AUTO_FIRE:
                self._handle_player_shoot()

            # 生成新的敌机
            self.spawn_enemies()

            # 更新所有游戏对象
            self.update_bullets()
            self.update_enemies()

            # 检查所有碰撞
            self.check_collisions()

            # 检查游戏结束条件
            if not self.player.is_alive():
                self.game_over = True

    def draw_ui(self) -> None:
        """绘制用户界面。

        在屏幕上绘制分数、生命值和操作提示等UI元素。
        """
        if self.font is not None:
            try:
                # 绘制当前分数
                score_text: pygame.Surface = self.font.render(
                    f"Score: {self.score}", True, WHITE
                )
                self.screen.blit(score_text, (10, 10))

                # 绘制剩余生命值（如果生命值很大，显示为无敌模式）
                if self.player.lives >= 999999999:
                    lives_text: pygame.Surface = self.font.render(
                        "Lives: ∞ (INVINCIBLE)", True, WHITE
                    )
                else:
                    lives_text: pygame.Surface = self.font.render(
                        f"Lives: {self.player.lives}", True, WHITE
                    )
                self.screen.blit(lives_text, (10, 50))

                # 绘制操作提示（仅在游戏进行中显示）
                if not self.game_over:
                    if AUTO_FIRE:
                        hint_text: pygame.Surface = self.font.render(
                            "Arrow keys to move, Auto-firing 1000 bullets/sec", True, WHITE
                        )
                    else:
                        hint_text: pygame.Surface = self.font.render(
                            "Arrow keys to move, Space to shoot", True, WHITE
                        )
                    self.screen.blit(hint_text, (10, SCREEN_HEIGHT - 30))
            except Exception as e:
                # 字体渲染失败，使用图形替代
                self._draw_ui_fallback()
        else:
            # 没有可用字体，使用图形替代
            self._draw_ui_fallback()

    def _draw_ui_fallback(self) -> None:
        """当字体不可用时的UI绘制替代方案。"""
        # 绘制分数区域（白色矩形）
        pygame.draw.rect(self.screen, WHITE, (10, 10, 150, 25))
        pygame.draw.rect(self.screen, BLACK, (12, 12, 146, 21))

        # 用小矩形表示分数（每10分一个小矩形）
        score_rects = min(self.score // 10, 14)  # 最多14个矩形
        for i in range(score_rects):
            pygame.draw.rect(self.screen, WHITE, (15 + i * 10, 15, 8, 15))

        # 绘制生命值区域
        if self.player.lives >= 9999999999:
            # 无敌模式显示
            pygame.draw.rect(self.screen, WHITE, (10, 50, 180, 25))
            pygame.draw.rect(self.screen, BLACK, (12, 52, 176, 21))
            # 绘制无敌符号（金色矩形）
            pygame.draw.rect(self.screen, YELLOW, (15, 55, 170, 15))
        else:
            pygame.draw.rect(self.screen, WHITE, (10, 50, 120, 25))
            pygame.draw.rect(self.screen, BLACK, (12, 52, 116, 21))
            # 用心形（小矩形）表示生命值（最多显示10个）
            lives_to_show = min(self.player.lives, 10)
            for i in range(lives_to_show):
                pygame.draw.rect(self.screen, RED, (15 + i * 10, 55, 8, 15))

        # 绘制操作提示区域（仅在游戏进行中）
        if not self.game_over:
            if AUTO_FIRE:
                pygame.draw.rect(self.screen, WHITE, (10, SCREEN_HEIGHT - 35, 400, 25))
                pygame.draw.rect(self.screen, BLACK, (12, SCREEN_HEIGHT - 33, 396, 21))
            else:
                pygame.draw.rect(self.screen, WHITE, (10, SCREEN_HEIGHT - 35, 300, 25))
                pygame.draw.rect(self.screen, BLACK, (12, SCREEN_HEIGHT - 33, 296, 21))

    def draw_game_over(self) -> None:
        """绘制游戏结束界面。

        在游戏结束时显示半透明遮罩、最终分数和重新开始提示。
        """
        # 创建半透明黑色遮罩
        overlay: pygame.Surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # 设置透明度
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        if self.big_font is not None and self.font is not None:
            try:
                # 绘制"游戏结束"标题
                game_over_text: pygame.Surface = self.big_font.render(
                    "GAME OVER", True, WHITE
                )
                text_rect: pygame.Rect = game_over_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                )
                self.screen.blit(game_over_text, text_rect)

                # 绘制最终分数
                final_score_text: pygame.Surface = self.font.render(
                    f"Final Score: {self.score}", True, WHITE
                )
                score_rect: pygame.Rect = final_score_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                )
                self.screen.blit(final_score_text, score_rect)

                # 绘制重新开始提示
                restart_text: pygame.Surface = self.font.render(
                    "Press R to Restart", True, WHITE
                )
                restart_rect: pygame.Rect = restart_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                )
                self.screen.blit(restart_text, restart_rect)
            except Exception as e:
                # 字体渲染失败，使用图形替代
                self._draw_game_over_fallback()
        else:
            # 没有可用字体，使用图形替代
            self._draw_game_over_fallback()

    def _draw_game_over_fallback(self) -> None:
        """当字体不可用时的游戏结束界面替代方案。"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        # 绘制"GAME OVER"（用大矩形表示）
        pygame.draw.rect(self.screen, WHITE, (center_x - 150, center_y - 70, 300, 50))
        pygame.draw.rect(self.screen, RED, (center_x - 145, center_y - 65, 290, 40))

        # 绘制分数区域
        pygame.draw.rect(self.screen, WHITE, (center_x - 100, center_y - 10, 200, 30))
        pygame.draw.rect(self.screen, BLACK, (center_x - 95, center_y - 5, 190, 20))

        # 用小矩形表示分数
        score_rects = min(self.score // 10, 18)  # 最多18个矩形
        for i in range(score_rects):
            pygame.draw.rect(self.screen, WHITE, (center_x - 90 + i * 10, center_y - 2, 8, 14))

        # 绘制重新开始提示区域
        pygame.draw.rect(self.screen, WHITE, (center_x - 120, center_y + 40, 240, 30))
        pygame.draw.rect(self.screen, GREEN, (center_x - 115, center_y + 45, 230, 20))

    def restart_game(self) -> None:
        """重新开始游戏。

        重置所有游戏状态，包括分数、玩家状态和所有游戏对象列表。
        """
        # 重置游戏状态
        self.game_over = False
        self.score = 0

        # 重新创建玩家对象
        player_x: int = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        player_y: int = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.player = Player(player_x, player_y)

        # 清空所有游戏对象列表
        self.enemies.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()

    def draw(self) -> None:
        """绘制游戏画面。

        清空屏幕并绘制所有游戏对象，包括玩家、敌机、子弹和UI元素。
        如果游戏结束，还会绘制游戏结束界面。
        """
        # 用黑色清空屏幕
        self.screen.fill(BLACK)

        # 仅在游戏进行中绘制游戏对象
        if not self.game_over:
            self._draw_game_objects()

        # 绘制用户界面
        self.draw_ui()

        # 如果游戏结束，绘制游戏结束界面
        if self.game_over:
            self.draw_game_over()

        # 更新显示缓冲区到屏幕
        pygame.display.flip()

    def _draw_game_objects(self) -> None:
        """绘制所有游戏对象。

        绘制玩家飞机、所有敌机和所有子弹。
        """
        # 绘制玩家飞机
        self.player.draw(self.screen)

        # 绘制所有敌机
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # 绘制所有子弹
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)

    def run(self) -> None:
        """运行游戏主循环。

        这是游戏的核心循环，持续处理事件、更新游戏状态和绘制画面，
        直到用户退出游戏。循环的每次迭代代表游戏的一帧。
        """
        while self.running:
            # 处理用户输入和系统事件
            self.handle_events()

            # 更新游戏逻辑和对象状态
            self.update_game()

            # 绘制当前帧的画面
            self.draw()

            # 控制游戏帧率
            self.clock.tick(FPS)

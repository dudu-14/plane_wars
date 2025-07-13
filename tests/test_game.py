#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏功能测试脚本
用于验证游戏的各个组件是否正常工作
"""

import pygame
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from config import *

def test_game_components():
    """测试游戏各个组件"""
    pygame.init()
    
    # 创建窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("游戏组件测试")
    
    clock = pygame.time.Clock()
    
    # 创建测试对象
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    enemy_small = Enemy(100, 50, "small")
    enemy_medium = Enemy(300, 50, "medium")
    player_bullet = Bullet(player.x + player.width // 2, player.y, "player")
    enemy_bullet = Bullet(enemy_small.x + enemy_small.width // 2, enemy_small.y + enemy_small.height, "enemy")
    
    running = True
    test_phase = 0
    frame_count = 0
    
    print("游戏组件测试开始...")
    print("测试阶段 0: 显示所有对象")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    test_phase = (test_phase + 1) % 4
                    print(f"切换到测试阶段 {test_phase}")
                    
        # 清空屏幕
        screen.fill(BLACK)
        
        # 根据测试阶段显示不同内容
        if test_phase == 0:
            # 显示所有对象
            player.draw(screen)
            enemy_small.draw(screen)
            enemy_medium.draw(screen)
            player_bullet.draw(screen)
            enemy_bullet.draw(screen)
            
        elif test_phase == 1:
            # 测试移动
            keys = pygame.key.get_pressed()
            player.update(keys)
            enemy_small.update()
            enemy_medium.update()
            player_bullet.update()
            enemy_bullet.update()
            
            player.draw(screen)
            enemy_small.draw(screen)
            enemy_medium.draw(screen)
            player_bullet.draw(screen)
            enemy_bullet.draw(screen)
            
        elif test_phase == 2:
            # 测试碰撞检测
            player.draw(screen)
            enemy_small.draw(screen)
            
            # 检查碰撞
            if player.rect.colliderect(enemy_small.rect):
                pygame.draw.rect(screen, RED, player.rect, 3)
                pygame.draw.rect(screen, RED, enemy_small.rect, 3)
            else:
                pygame.draw.rect(screen, GREEN, player.rect, 2)
                pygame.draw.rect(screen, GREEN, enemy_small.rect, 2)
                
        elif test_phase == 3:
            # 测试射击
            keys = pygame.key.get_pressed()
            player.update(keys)
            
            if keys[pygame.K_SPACE]:
                bullet_pos = player.shoot()
                if bullet_pos:
                    new_bullet = Bullet(bullet_pos[0], bullet_pos[1], "player")
                    new_bullet.draw(screen)
                    
            player.draw(screen)
            
        # 绘制测试信息
        info_y = 10
        test_info = [
            "按空格键切换测试阶段",
            f"当前阶段: {test_phase}",
            "阶段0: 显示对象",
            "阶段1: 测试移动",
            "阶段2: 测试碰撞",
            "阶段3: 测试射击"
        ]
        
        for info in test_info:
            # 绘制简单的文字替代（白色矩形）
            pygame.draw.rect(screen, WHITE, (10, info_y, len(info) * 8, 20))
            pygame.draw.rect(screen, BLACK, (12, info_y + 2, len(info) * 8 - 4, 16))
            info_y += 25
            
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
        
    pygame.quit()
    print("测试完成")

if __name__ == "__main__":
    test_game_components()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体测试程序
用于测试pygame字体渲染是否正常工作
"""

import pygame
import sys

def test_fonts():
    """测试不同的字体渲染方式"""
    pygame.init()
    
    # 创建窗口
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("字体测试")
    
    # 测试不同的字体
    fonts_to_test = [
        ("Default Font", pygame.font.Font(None, 36)),
        ("Arial SysFont", pygame.font.SysFont('arial', 36)),
        ("Times SysFont", pygame.font.SysFont('times', 36)),
        ("Courier SysFont", pygame.font.SysFont('courier', 36)),
    ]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # 清空屏幕
        screen.fill((0, 0, 0))
        
        # 测试渲染不同字体
        y_pos = 50
        for font_name, font_obj in fonts_to_test:
            try:
                text = font_obj.render(f"{font_name}: Hello World! 123", True, (255, 255, 255))
                screen.blit(text, (50, y_pos))
                y_pos += 50
            except Exception as e:
                # 如果字体失败，绘制一个矩形
                pygame.draw.rect(screen, (255, 0, 0), (50, y_pos, 300, 30))
                y_pos += 50
                
        # 绘制一些基本图形确保pygame工作正常
        pygame.draw.rect(screen, (0, 255, 0), (50, 400, 100, 50))
        pygame.draw.circle(screen, (0, 0, 255), (250, 425), 25)
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_fonts()

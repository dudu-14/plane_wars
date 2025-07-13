#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞机大战游戏主程序。

这是一个使用Python和Pygame开发的2D射击游戏。
玩家控制飞机与敌机战斗，通过击毁敌机获得分数。

游戏特性:
    - 玩家可以使用方向键控制飞机移动
    - 按空格键发射子弹攻击敌机
    - 不同类型的敌机具有不同的属性和分数
    - 玩家有生命值系统，受到伤害会减少生命
    - 游戏结束后可以重新开始

运行要求:
    - Python 3.8+
    - Pygame 2.0+

使用方法:
    python main.py

作者: AI Assistant
版本: 1.0
"""

import pygame
import sys
from typing import NoReturn
from game import Game


def main() -> NoReturn:
    """游戏主函数。

    初始化Pygame库，创建游戏实例并运行游戏主循环。
    当游戏结束时，清理资源并退出程序。

    Raises:
        SystemExit: 当游戏正常结束时退出程序
    """
    try:
        # 初始化Pygame库
        pygame.init()

        # 创建游戏实例
        game = Game()

        # 运行游戏主循环
        game.run()

    except Exception as e:
        # 如果发生错误，打印错误信息
        print(f"游戏运行时发生错误: {e}")

    finally:
        # 确保Pygame资源被正确清理
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()

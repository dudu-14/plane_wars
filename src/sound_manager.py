#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""音效管理模块。

本模块负责管理游戏中的所有音效，包括射击、击杀、爆炸等音效。
支持音效的加载、播放和音量控制。

典型用法示例:
    sound_manager = SoundManager()
    sound_manager.play_shoot()
    sound_manager.play_enemy_kill()
"""

import pygame
import os
from typing import Dict, Optional
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class SoundManager:
    """音效管理器类。
    
    负责管理游戏中的所有音效，包括加载、播放和控制音效。
    支持程序生成的音效，无需外部音频文件。
    
    Attributes:
        enabled (bool): 是否启用音效
        volume (float): 音效音量 (0.0 - 1.0)
        sounds (Dict): 存储所有音效的字典
    """
    
    def __init__(self, enabled: bool = True, volume: float = 0.7) -> None:
        """初始化音效管理器。

        Args:
            enabled (bool): 是否启用音效，默认为True
            volume (float): 音效音量，范围0.0-1.0，默认为0.7（按需求1.1.0）
        """
        self.enabled: bool = enabled
        self.volume: float = max(0.0, min(1.0, volume))
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        # 初始化pygame音频模块
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._generate_sounds()
        except pygame.error as e:
            print(f"Warning: Could not initialize sound system: {e}")
            self.enabled = False
            
    def _generate_sounds(self) -> None:
        """生成程序化音效。
        
        使用pygame生成简单的音效，无需外部音频文件。
        """
        try:
            # 1.1.0 需求音效
            # 玩家操作音效
            self.sounds['shot'] = self._create_shoot_sound()  # 发射子弹音效

            # 战斗音效
            self.sounds['hit_small'] = self._create_hit_small_sound()  # 小型敌机被击中
            self.sounds['hit_medium'] = self._create_hit_medium_sound()  # 中型敌机被击中
            self.sounds['explosion'] = self._create_explosion_sound()  # 敌机爆炸
            self.sounds['player_hit'] = self._create_player_hit_sound()  # 玩家被击中

            # 道具音效
            self.sounds['item_pick'] = self._create_item_pick_sound()  # 道具拾取

            # 状态音效
            self.sounds['start'] = self._create_start_sound()  # 游戏开始
            self.sounds['game_over'] = self._create_game_over_sound()  # 游戏结束

            # 保持兼容性的旧音效名称
            self.sounds['shoot'] = self.sounds['shot']
            self.sounds['enemy_kill'] = self.sounds['explosion']
            self.sounds['enemy_spawn'] = self._create_spawn_sound()

        except Exception as e:
            print(f"Warning: Could not generate sounds: {e}")
            self.enabled = False
            
    def _create_shoot_sound(self) -> pygame.mixer.Sound:
        """创建射击音效。
        
        Returns:
            pygame.mixer.Sound: 射击音效对象
        """
        # 创建短促的射击声
        duration = 0.1  # 0.1秒
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # 生成音频数据
        import numpy as np
        
        # 高频噪音模拟射击声
        frequency = 800  # 800Hz
        t = np.linspace(0, duration, frames, False)
        
        # 基础正弦波
        wave = np.sin(frequency * 2 * np.pi * t)
        
        # 添加噪音
        noise = np.random.normal(0, 0.3, frames)
        wave = wave + noise
        
        # 应用包络（快速衰减）
        envelope = np.exp(-t * 20)
        wave = wave * envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.3)  # 射击声音较小
        
        return sound
        
    def _create_explosion_sound(self) -> pygame.mixer.Sound:
        """创建爆炸音效。
        
        Returns:
            pygame.mixer.Sound: 爆炸音效对象
        """
        # 创建爆炸声
        duration = 0.3  # 0.3秒
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        import numpy as np
        
        t = np.linspace(0, duration, frames, False)
        
        # 低频爆炸声
        frequency1 = 100  # 100Hz
        frequency2 = 200  # 200Hz
        
        wave1 = np.sin(frequency1 * 2 * np.pi * t)
        wave2 = np.sin(frequency2 * 2 * np.pi * t)
        
        # 添加大量噪音模拟爆炸
        noise = np.random.normal(0, 0.8, frames)
        wave = (wave1 + wave2) * 0.3 + noise
        
        # 应用包络（中等衰减）
        envelope = np.exp(-t * 5)
        wave = wave * envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.6)  # 爆炸声音较大
        
        return sound
        
    def _create_hit_sound(self) -> pygame.mixer.Sound:
        """创建受击音效。
        
        Returns:
            pygame.mixer.Sound: 受击音效对象
        """
        # 创建受击声
        duration = 0.2  # 0.2秒
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        import numpy as np
        
        t = np.linspace(0, duration, frames, False)
        
        # 中频警告声
        frequency = 400  # 400Hz
        wave = np.sin(frequency * 2 * np.pi * t)
        
        # 添加失真效果
        wave = np.sign(wave) * np.power(np.abs(wave), 0.5)
        
        # 应用包络
        envelope = np.exp(-t * 8)
        wave = wave * envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.4)
        
        return sound
        
    def _create_spawn_sound(self) -> pygame.mixer.Sound:
        """创建敌机出现音效。
        
        Returns:
            pygame.mixer.Sound: 敌机出现音效对象
        """
        # 创建敌机出现声
        duration = 0.15  # 0.15秒
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        import numpy as np
        
        t = np.linspace(0, duration, frames, False)
        
        # 上升音调
        frequency_start = 200
        frequency_end = 600
        frequency = frequency_start + (frequency_end - frequency_start) * t / duration
        
        wave = np.sin(frequency * 2 * np.pi * t)
        
        # 应用包络
        envelope = 1 - np.exp(-t * 10)  # 快速上升
        wave = wave * envelope * 0.5
        
        # 转换为pygame音频格式
        wave = (wave * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.3)
        
        return sound
        
    def play_shoot(self) -> None:
        """播放射击音效。"""
        if self.enabled and 'shoot' in self.sounds:
            try:
                self.sounds['shoot'].play()
            except pygame.error:
                pass  # 忽略播放错误
                
    def play_enemy_kill(self) -> None:
        """播放敌机击杀音效。"""
        if self.enabled and 'enemy_kill' in self.sounds:
            try:
                self.sounds['enemy_kill'].play()
            except pygame.error:
                pass
                
    def play_player_hit(self) -> None:
        """播放玩家受击音效。"""
        if self.enabled and 'player_hit' in self.sounds:
            try:
                self.sounds['player_hit'].play()
            except pygame.error:
                pass
                
    def play_enemy_spawn(self) -> None:
        """播放敌机出现音效。"""
        if self.enabled and 'enemy_spawn' in self.sounds:
            try:
                self.sounds['enemy_spawn'].play()
            except pygame.error:
                pass
                
    def set_volume(self, volume: float) -> None:
        """设置音效音量。
        
        Args:
            volume (float): 音量值，范围0.0-1.0
        """
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
            
    def toggle_sound(self) -> None:
        """切换音效开关。"""
        self.enabled = not self.enabled
        
    def is_enabled(self) -> bool:
        """检查音效是否启用。
        
        Returns:
            bool: 音效是否启用
        """
        return self.enabled

    # 1.1.0 新增音效创建方法
    def _create_hit_small_sound(self) -> pygame.mixer.Sound:
        """创建小型敌机被击中音效（短促"噗"声）"""
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)

        import numpy as np
        t = np.linspace(0, duration, frames, False)

        # 低频短促声
        frequency = 200
        wave = np.sin(frequency * 2 * np.pi * t)
        envelope = np.exp(-t * 30)  # 快速衰减
        wave = wave * envelope

        wave = (wave * 16383).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.4)
        return sound

    def _create_hit_medium_sound(self) -> pygame.mixer.Sound:
        """创建中型敌机被击中音效（稍长"嘭"声）"""
        duration = 0.15
        sample_rate = 22050
        frames = int(duration * sample_rate)

        import numpy as np
        t = np.linspace(0, duration, frames, False)

        # 中频稍长声
        frequency = 150
        wave = np.sin(frequency * 2 * np.pi * t)
        envelope = np.exp(-t * 15)  # 较慢衰减
        wave = wave * envelope

        wave = (wave * 20000).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.5)
        return sound

    def _create_player_hit_sound(self) -> pygame.mixer.Sound:
        """创建玩家被击中音效（低沉"咚"声）"""
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)

        import numpy as np
        t = np.linspace(0, duration, frames, False)

        # 低频厚重声
        frequency = 80
        wave = np.sin(frequency * 2 * np.pi * t)
        envelope = np.exp(-t * 8)  # 慢衰减
        wave = wave * envelope

        wave = (wave * 25000).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.6)
        return sound

    def _create_item_pick_sound(self) -> pygame.mixer.Sound:
        """创建道具拾取音效（轻快"叮"声）"""
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)

        import numpy as np
        t = np.linspace(0, duration, frames, False)

        # 高频清脆声
        frequency = 1200
        wave = np.sin(frequency * 2 * np.pi * t)
        envelope = np.exp(-t * 12)
        wave = wave * envelope

        wave = (wave * 15000).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.3)
        return sound

    def _create_start_sound(self) -> pygame.mixer.Sound:
        """创建游戏开始音效（激昂短音乐段）"""
        duration = 1.5
        sample_rate = 22050
        frames = int(duration * sample_rate)

        import numpy as np
        t = np.linspace(0, duration, frames, False)

        # 上升音调
        freq_start = 440  # A4
        freq_end = 880    # A5
        frequency = freq_start + (freq_end - freq_start) * t / duration

        wave = np.sin(frequency * 2 * np.pi * t)
        envelope = np.exp(-t * 2) * (1 - t / duration)
        wave = wave * envelope

        wave = (wave * 20000).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.4)
        return sound

    def _create_game_over_sound(self) -> pygame.mixer.Sound:
        """创建游戏结束音效（低沉长音）"""
        duration = 1.5
        sample_rate = 22050
        frames = int(duration * sample_rate)

        import numpy as np
        t = np.linspace(0, duration, frames, False)

        # 下降音调
        freq_start = 220  # A3
        freq_end = 110    # A2
        frequency = freq_start - (freq_start - freq_end) * t / duration

        wave = np.sin(frequency * 2 * np.pi * t)
        envelope = np.exp(-t * 1.5)
        wave = wave * envelope

        wave = (wave * 25000).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.set_volume(self.volume * 0.5)
        return sound

    # 1.1.0 新增便捷播放方法
    def play_shot(self):
        """播放发射子弹音效"""
        self._play_sound('shot')

    def play_hit_small(self):
        """播放小型敌机被击中音效"""
        self._play_sound('hit_small')

    def play_hit_medium(self):
        """播放中型敌机被击中音效"""
        self._play_sound('hit_medium')

    def play_explosion(self):
        """播放敌机爆炸音效"""
        self._play_sound('explosion')

    def play_player_hit(self):
        """播放玩家被击中音效"""
        self._play_sound('player_hit')

    def play_item_pick(self):
        """播放道具拾取音效"""
        self._play_sound('item_pick')

    def play_start(self):
        """播放游戏开始音效"""
        self._play_sound('start')

    def play_game_over(self):
        """播放游戏结束音效"""
        self._play_sound('game_over')

    def _play_sound(self, sound_name: str):
        """内部音效播放方法"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error:
                pass

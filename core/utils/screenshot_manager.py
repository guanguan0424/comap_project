#!/usr/bin/env python3
"""截图管理工具模块 - 统一管理测试过程中产生的截图文件"""

import os
import time
import uuid
from datetime import datetime
from pathlib import Path
import shutil

class ScreenshotManager:
    """截图文件管理器"""
    
    def __init__(self, base_dir="test-screenshots"):
        """初始化截图管理器
        
        Args:
            base_dir: 截图存储的根目录路径
        """
        self.base_dir = Path(base_dir)
        self.setup_directories()
    
    def setup_directories(self):
        """创建必要的目录结构"""
        # 主分类目录
        directories = [
            "timestamped",  # 带时间戳的截图
            "latest",       # 最新截图（每次测试覆盖）
            "valid",        # 正确凭据测试截图
            "invalid",      # 错误凭据测试截图  
            "empty",        # 空凭据测试截图
            "incorrect",    # 密码错误测试截图
            "by_date"       # 按日期分类的截图
        ]
        
        for dir_name in directories:
            (self.base_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    def generate_screenshot_name(self, test_name, prefix="screenshot", timestamp=True):
        """生成截图文件名
        
        Args:
            test_name: 测试函数名称
            prefix: 文件名前缀
            timestamp: 是否包含时间戳
        
        Returns:
            str: 完整的截图文件名
        """
        # 规范化测试名称
        clean_name = test_name.replace("test_", "").replace("_", "-")
        
        if timestamp:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}_{clean_name}_{current_time}_{uuid.uuid4().hex[:8]}.png"
        else:
            filename = f"{prefix}_{clean_name}.png"
        
        return filename
    
    def save_screenshot(self, page, test_name, category="general", save_to_latest=True):
        """保存页面截图
        
        Args:
            page: Playwright页面对象
            test_name: 测试函数名称
            category: 截图分类
            save_to_latest: 是否保存到latest文件夹
        
        Returns:
            dict: 截图信息
        """
        # 生成时间戳版本文件名
        timestamp_filename = self.generate_screenshot_name(test_name, f"{category}_screenshot", timestamp=True)
        
        # 路径定义
        timestamp_path = self.base_dir / "timestamped" / timestamp_filename
        category_path = self.base_dir / category / f"{test_name}.png"
        latest_path = self.base_dir / "latest" / f"{category}_{test_name}.png"
        
        # 按日期分类的路径
        date_folder = datetime.now().strftime("%Y%m%d")
        dated_path = self.base_dir / "by_date" / date_folder / timestamp_filename
        dated_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 确保目录存在
        timestamp_path.parent.mkdir(parents=True, exist_ok=True)
        category_path.parent.mkdir(parents=True, exist_ok=True)
        latest_path.parent.mkdir(parents=True, exist_ok=True)
        dated_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存截图到各个目录
        screenshot_info = {
            "test_name": test_name,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "files": []
        }
        
        # 截图并保存到不同位置
        screenshot_paths = [
            (timestamp_path, "timestamped"),
            (dated_path, "dated"),
        ]
        
        # 只截图一次，然后复制到不同位置
        page.screenshot(path=str(timestamp_path))
        screenshot_info["files"].append({
            "path": str(timestamp_path),
            "type": "timestamped"
        })
        
        # 复制到其他位置
        shutil.copy2(timestamp_path, category_path)
        screenshot_info["files"].append({
            "path": str(category_path),
            "type": "category"
        })
        
        if save_to_latest:
            shutil.copy2(timestamp_path, latest_path)
            screenshot_info["files"].append({
                "path": str(latest_path),
                "type": "latest"
            })
        
        return screenshot_info
    
    def cleanup_old_screenshots(self, days_to_keep=7):
        """清理旧的截图文件
        
        Args:
            days_to_keep: 保留最近多少天的截图
        """
        cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
        deleted_count = 0
        
        for file_path in self.base_dir.rglob("*.png"):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                deleted_count += 1
        
        return deleted_count
    
    def get_screenshot_stats(self):
        """获取截图统计信息"""
        screenshot_files = list(self.base_dir.rglob("*.png"))
        
        stats = {
            "total_screenshots": len(screenshot_files),
            "categories": {},
            "by_category": {},
            "by_date": {}
        }
        
        # 按目录统计
        for file_path in screenshot_files:
            relative_path = file_path.relative_to(self.base_dir)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
            
            if category not in stats["categories"]:
                stats["categories"][category] = 0
            stats["categories"][category] += 1
        
        return stats


# 全局截图管理器实例
screenshot_manager = ScreenshotManager()


def take_screenshot(page, test_function, description=""):
    """便捷截图函数 - 供测试用例调用
    
    Args:
        page: 页面对象
        test_function: 测试函数名称或对象
        description: 截图描述
    
    Returns:
        dict: 截图信息
    """
    if hasattr(test_function, "__name__"):
        test_name = test_function.__name__
    else:
        test_name = str(test_function)
    
    # 根据测试名称确定分类
    category = "general"
    if "valid" in test_name.lower():
        category = "valid"
    elif "invalid" in test_name.lower():
        category = "invalid"
    elif "empty" in test_name.lower():
        category = "empty"
    elif "incorrect" in test_name.lower():
        category = "incorrect"
    
    screenshot_info = screenshot_manager.save_screenshot(page, test_name, category)
    
    # 添加截图描述
    if description:
        screenshot_info["description"] = description
    
    return screenshot_info


def cleanup_screenshots():  
    """清理截图文件的便捷函数"""
    return screenshot_manager.cleanup_old_screenshots()


def get_screenshot_stats():
    """获取截图统计信息的便捷函数"""
    return screenshot_manager.get_screenshot_stats()


if __name__ == "__main__":
    # 演示功能
    stats = get_screenshot_stats()
    print(f"截图统计信息: {stats}")
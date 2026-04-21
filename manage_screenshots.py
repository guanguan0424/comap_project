#!/usr/bin/env python3
"""截图管理脚本 - 清理、统计和归档测试截图"""

import os
import sys
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='测试截图管理工具')
    parser.add_argument('action', choices=['cleanup', 'stats', 'archive', 'list'], 
                       help='执行的操作')
    parser.add_argument('--days', type=int, default=7, 
                       help='保留最近多少天的截图（默认7天）')
    parser.add_argument('--screenshot-dir', default='artifacts\test-screenshots',
                       help='截图目录路径（默认：artifacts\test-screenshots）')
    parser.add_argument('--target-dir', help='归档目标目录')
    parser.add_argument('--verbose', action='store_true', 
                       help='显示详细输出')
    
    args = parser.parse_args()
    
    # 验证截图目录
    screenshot_dir = Path(args.screenshot_dir)
    if not screenshot_dir.exists():
        print(f"错误: 截图目录 {screenshot_dir} 不存在")
        return 1
    
    if args.action == 'cleanup':
        return cleanup_screenshots(screenshot_dir, args.days, args.verbose)
    elif args.action == 'stats':
        return show_stats(screenshot_dir, args.verbose)
    elif args.action == 'archive':
        return archive_screenshots(screenshot_dir, args.target_dir, args.verbose)
    elif args.action == 'list':
        return list_screenshots(screenshot_dir, args.verbose)

def cleanup_screenshots(screenshot_dir, days_to_keep, verbose=False):
    """清理旧的截图文件"""
    cutoff_time = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0
    
    for file_path in screenshot_dir.rglob("*.png"):
        if file_path.is_file():
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_time < cutoff_time:
                if verbose:
                    print(f"删除: {file_path} ({file_time.strftime('%Y-%m-%d %H:%M:%S')})")
                file_path.unlink()
                deleted_count += 1
    
    # 清理空目录
    for dir_path in sorted(screenshot_dir.rglob("*"), key=len, reverse=True):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            if verbose:
                print(f"删除空目录: {dir_path}")
            dir_path.rmdir()
    
    print(f"✅ 清理完成: 删除了 {deleted_count} 个超过 {days_to_keep} 天的截图文件")
    return 0

def show_stats(screenshot_dir, verbose=False):
    """显示截图统计信息"""
    screenshot_files = list(screenshot_dir.rglob("*.png"))
    total_size = sum(f.stat().st_size for f in screenshot_files if f.is_file())
    
    stats = {
        "total_screenshots": len(screenshot_files),
        "total_size_mb": total_size / (1024 * 1024),
        "categories": {},
        "recent_files": []
    }
    
    # 按目录统计
    for file_path in screenshot_files:
        relative_path = file_path.relative_to(screenshot_dir)
        category = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
        
        if category not in stats["categories"]:
            stats["categories"][category] = 0
        stats["categories"][category] += 1
    
    # 最近文件
    recent_files = sorted(screenshot_files, 
                         key=lambda f: f.stat().st_mtime, 
                         reverse=True)[:5]
    
    for file_path in recent_files:
        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        stats["recent_files"].append({
            "name": file_path.name,
            "path": str(file_path.relative_to(screenshot_dir)),
            "size_mb": file_path.stat().st_size / (1024 * 1024),
            "time": file_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 输出统计信息
    print("截图统计信息")
    print("=" * 50)
    print(f"总截图文件: {stats['total_screenshots']}")
    print(f"总大小: {stats['total_size_mb']:.2f} MB")
    print()
    
    print("按分类统计:")
    for category, count in sorted(stats['categories'].items()):
        print(f"  {category}: {count} 个文件")
    
    print()
    print("最近截图:")
    for file_info in stats['recent_files']:
        print(f"  {file_info['time']} - {file_info['name']} ({file_info['size_mb']:.2f} MB)")
    
    return 0

def archive_screenshots(screenshot_dir, target_dir=None, verbose=False):
    """归档截图文件"""
    if target_dir is None:
        # 使用时间戳创建归档目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir = f"screenshots_archive_{timestamp}"
    
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    screenshot_files = list(screenshot_dir.rglob("*.png"))
    archived_count = 0
    
    for file_path in screenshot_files:
        if file_path.is_file():
            # 保持目录结构
            relative_path = file_path.relative_to(screenshot_dir)
            target_file = target_path / relative_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(file_path, target_file)
            if verbose:
                print(f"归档: {relative_path}")
            archived_count += 1
    
    print(f"✅ 归档完成: {archived_count} 个截图已保存到 {target_dir}")
    return 0

def list_screenshots(screenshot_dir, verbose=False):
    """列出所有截图文件"""
    screenshot_files = list(screenshot_dir.rglob("*.png"))
    
    print(f"截图目录: {screenshot_dir}")
    print(f"总文件数: {len(screenshot_files)}")
    print()
    
    # 按修改时间排序
    sorted_files = sorted(screenshot_files, 
                         key=lambda f: f.stat().st_mtime, 
                         reverse=True)
    
    for file_path in sorted_files:
        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        size_mb = file_path.stat().st_size / (1024 * 1024)
        
        relative_path = file_path.relative_to(screenshot_dir)
        
        if verbose:
            print(f"{file_time.strftime('%Y-%m-%d %H:%M:%S')} "
                  f"[{size_mb:.2f} MB] {relative_path}")
        else:
            print(f"{file_time.strftime('%m-%d %H:%M')} "
                  f"[{size_mb:.1f} MB] {file_path.name}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
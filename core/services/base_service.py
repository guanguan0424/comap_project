#!/usr/bin/env python3
"""
基础服务类 - 为UI+API混合测试提供通用功能
"""

import json
import yaml
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseService(ABC):
    """混合测试服务基类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化服务
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path) if config_path else {}
        self.api_client = None  # API客户端实例
        self.ui_context = None  # UI上下文实例
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.json'):
                    return json.load(f)
                elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def setup_api_client(self, client):
        """设置API客户端"""
        self.api_client = client
        
    def setup_ui_context(self, context):
        """设置UI上下文"""
        self.ui_context = context
        
    @abstractmethod
    def execute_business_flow(self, *args, **kwargs):
        """执行业务流程（子类必须实现）"""
        pass
    
    def validate_ui_state(self, expected_state: Dict[str, Any]) -> bool:
        """验证UI状态"""
        # 子类实现具体的UI状态验证逻辑
        return True
        
    def validate_api_response(self, response: Any, expected_result: Dict[str, Any]) -> bool:
        """验证API响应"""
        # 子类实现具体的API响应验证逻辑
        return True
        
    def sync_ui_and_api_state(self):
        """同步UI和API状态"""
        # 子类实现状态同步逻辑
        pass
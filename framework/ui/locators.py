# UI元素定位器策略
# 针对React/Vue现代Web应用优化的定位策略

from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class LocatorStrategy:
    """定位策略配置"""
    name: str
    priority: int  # 优先级，数字越小优先级越高
    

# React/Vue应用常用的定位属性
REACT_LOCATOR_ATTRIBUTES = [
    "data-testid",  # 测试ID - 最高优先级
    "data-cy",      # Cypress测试ID
    "data-test",    # 通用测试属性
    "data-id",      # 数据ID
    "aria-label",   # 无障碍标签
    "name",         # 表单字段名
    "id",           # 元素ID
    "class",        # CSS类名
]


class ReactVueLocators:
    """React/Vue应用定位器工具"""
    
    @staticmethod
    def create_test_id_locator(test_id: str) -> str:
        """创建data-testid定位器"""
        return f'[data-testid="{test_id}"]'
    
    @staticmethod
    def create_data_cy_locator(data_cy: str) -> str:
        """创建data-cy定位器"""
        return f'[data-cy="{data_cy}"]'
    
    @staticmethod
    def create_component_locator(component_name: str, props: Dict = None) -> List[str]:
        """创建React组件定位器策略"""
        locators = []
        
        # 根据组件名称和属性生成可能的定位器
        locators.append(f'[class*="{component_name}"]')  # CSS类名包含组件名
        locators.append(f'[data-component="{component_name}"]')  # 组件属性
        
        # 如果有属性，生成更精确的定位器
        if props:
            prop_str = ",".join([f'{k}="{v}"' for k, v in props.items()])
            locators.append(f'[{prop_str}]')
        
        return locators


class FormLocators:
    """表单元素定位器"""
    
    @staticmethod
    def get_input_by_label(label_text: str) -> List[str]:
        """根据标签文本获取输入框定位器"""
        return [
            f'label:has-text("{label_text}") + input',
            f'label:has-text("{label_text}") ~ input',
            f'//label[contains(text(), "{label_text}")]/following-sibling::input',
        ]
    
    @staticmethod
    def get_input_by_placeholder(placeholder_text: str) -> List[str]:
        """根据占位符获取输入框定位器"""
        return [f'input[placeholder*="{placeholder_text}"]']


class ButtonLocators:
    """按钮定位器"""
    
    @staticmethod
    def get_button_by_text(button_text: str) -> List[str]:
        """根据按钮文本获取定位器"""
        return [
            f'button:text-is("{button_text}")',
            f'button:has-text("{button_text}")',
            f'[role="button"]:has-text("{button_text}")',
            f'button[data-testid*="{button_text.lower().replace(" ", "-")}"]'
        ]
    
    @staticmethod
    def get_button_by_type(button_type: str) -> List[str]:
        """根据按钮类型获取定位器"""
        return [f'button[type="{button_type}"]']


class NavigationLocators:
    """导航元素定位器"""
    
    @staticmethod
    def get_nav_item(text: str) -> List[str]:
        """获取导航项定位器"""
        return [
            f'nav a:has-text("{text}")',
            f'[role="navigation"] a:has-text("{text}")',
            f'.navbar a:has-text("{text}")',
            f'[data-testid="nav-{text.lower().replace(" ", "-")}"]'
        ]


class TableLocators:
    """表格元素定位器"""
    
    @staticmethod
    def get_table_cell(row_text: str, column_name: str) -> List[str]:
        """获取表格单元格定位器"""
        return [
            f'tr:has-text("{row_text}") td:nth-child({column_name})',
            f'tr:has-text("{row_text}") td[data-column="{column_name}"]'
        ]
    
    @staticmethod
    def get_row_by_text(row_text: str) -> List[str]:
        """根据行文本获取行定位器"""
        return [f'tr:has-text("{row_text}")']


class DialogLocators:
    """对话框定位器"""
    
    @staticmethod
    def get_dialog_by_title(title: str) -> List[str]:
        """获取对话框定位器"""
        return [
            f'[role="dialog"]:has-text("{title}")',
            f'.modal:has-text("{title}")',
            f'[data-testid="dialog-{title.lower().replace(" ", "-")}"]'
        ]


class CommonUILocators:
    """通用的UI元素定位器"""
    
    @staticmethod
    def get_dropdown_options() -> List[str]:
        """获取下拉选项定位器"""
        return ['[role="option"]', '.dropdown-option', '.select-option']
    
    @staticmethod
    def get_checkbox(label: str) -> List[str]:
        """获取复选框定位器"""
        return [
            f'label:has-text("{label}") + input[type="checkbox"]',
            f'input[type="checkbox"][name*="{label.lower()}"]'
        ]
    
    @staticmethod
    def get_radio_button(label: str) -> List[str]:
        """获取单选按钮定位器"""
        return [
            f'label:has-text("{label}") + input[type="radio"]',
            f'input[type="radio"][name*="{label.lower()}"]'
        ]


def create_fallback_locators(element_name: str, element_type: str = None) -> List[str]:
    """创建备用定位器策略"""
    locators = []
    
    if element_type == "button":
        locators.extend(ButtonLocators.get_button_by_text(element_name))
    elif element_type == "input":
        locators.extend(FormLocators.get_input_by_placeholder(element_name))
        locators.extend(FormLocators.get_input_by_label(element_name))
    elif element_type == "nav":
        locators.extend(NavigationLocators.get_nav_item(element_name))
    
    # 通用定位器
    for attr in REACT_LOCATOR_ATTRIBUTES:
        locators.append(f'[{attr}*="{element_name}"]')
    
    return locators
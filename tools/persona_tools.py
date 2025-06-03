"""
人物档案工具
"""

from typing import Dict, Any, Optional
from .base import BaseTools, generate_prompt_content

class PersonaTools(BaseTools):
    """人物档案工具类"""
    
    def get_persona(self) -> Dict[str, Any]:
        """获取用户画像信息"""
        try:
            persona = self.db.get_persona()
            if not persona:
                return {
                    "content": "未找到用户画像信息。",
                    "raw_data": None
                }
            
            # 生成提示内容
            template = """# 用户画像核心信息

以下是当前用户的个人画像数据。请在与用户互动时参考这些信息，以便提供更个性化和相关的回应。

## 基本信息
- **用户姓名 (name)**: {name}
- **性别 (gender)**: {gender} (这可能会影响语言风格和称呼)
- **性格特点 (personality)**: {personality} (例如：{personality}，请据此调整沟通方式)
- **个人简介 (bio)**: {bio}
- **头像链接 (avatar_url)**: {avatar_url}

## 系统信息
- **隐私级别 (privacy_level)**: {privacy_level}
- **档案创建时间 (created_time)**: {created_time}
- **档案最后更新时间 (updated_time)**: {updated_time}

**如何使用这些信息：**
- **个性化称呼与语气**: 根据姓名和性别使用合适的称呼。
- **理解用户偏好**: 性格和简介能揭示用户的沟通偏好和可能的兴趣点。
- **内容相关性**: 结合用户画像信息，使AI的回答和建议更贴近用户需求。"""
            
            content = generate_prompt_content(template, persona)
            
            return {
                "content": content,
                "raw_data": persona
            }
            
        except Exception as e:
            return self._create_error_response(str(e), 1)
    
    def save_persona(self, name: Optional[str] = None, gender: Optional[str] = None, 
                    personality: Optional[str] = None, avatar_url: Optional[str] = None, 
                    bio: Optional[str] = None, privacy_level: Optional[str] = None) -> Dict[str, Any]:
        """保存（更新）用户画像信息"""
        try:
            update_data = {}
            if name is not None:
                update_data['name'] = name
            if gender is not None:
                update_data['gender'] = gender
            if personality is not None:
                update_data['personality'] = personality
            if avatar_url is not None:
                update_data['avatar_url'] = avatar_url
            if bio is not None:
                update_data['bio'] = bio
            if privacy_level is not None:
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return self._create_success_response(1, "no_change")
            
            success = self.db.update_persona(**update_data)
            if success:
                return self._create_success_response(1, "updated")
            else:
                return self._create_error_response("更新失败", 1)
                
        except Exception as e:
            return self._create_error_response(str(e), 1) 
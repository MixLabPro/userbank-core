"""
Persona tools
"""

from typing import Dict, Any, Optional
from .base import BaseTools, generate_prompt_content

class PersonaTools(BaseTools):
    """Persona tools class"""
    
    def get_persona(self) -> Dict[str, Any]:
        """Get user persona information"""
        try:
            persona = self.db.get_persona()
            if not persona:
                return {
                    "content": "No user persona information found.",
                    "raw_data": None
                }
            
            # Generate prompt content
            template = """# User Persona Core Information

The following is the current user's personal persona data. Please refer to this information when interacting with the user to provide more personalized and relevant responses.

## Basic Information
- **User Name**: {name}
- **Gender**: {gender} (This may affect language style and addressing)
- **Personality Traits**: {personality} (For example: {personality}, please adjust communication style accordingly)
- **Personal Bio**: {bio}
- **Avatar URL**: {avatar_url}

## System Information
- **Privacy Level**: {privacy_level}
- **Profile Created Time**: {created_time}
- **Profile Last Updated Time**: {updated_time}

**How to use this information:**
- **Personalized addressing and tone**: Use appropriate addressing based on name and gender.
- **Understanding user preferences**: Personality and bio can reveal user's communication preferences and possible interests.
- **Content relevance**: Combine user persona information to make AI responses and suggestions more aligned with user needs."""
            
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
        """Save (update) user persona information"""
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
                return self._create_error_response("Update failed", 1)
                
        except Exception as e:
            return self._create_error_response(str(e), 1) 
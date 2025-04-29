from app.models.user import User

def is_admin(user: User) -> bool:
    return user.role == 'admin'

def can_edit_content(user: User, content) -> bool:
    return user.role in ['admin', 'editor'] or user.id == content.uploaded_by
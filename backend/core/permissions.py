from typing import Set, Dict

class Permission:
    ADMIN = 'admin'
    KICK_PLAYER = 'kick_player'
    BAN_PLAYER = 'ban_player'
    MODIFY_LOBBY = 'modify_lobby'
    ADD_BOT = 'add_bot'
    REMOVE_BOT = 'remove_bot'
    START_MATCH = 'start_match'
    VIEW_ANALYTICS = 'view_analytics'

class PermissionManager:
    def __init__(self):
        self.player_permissions: Dict[str, Set[str]] = {}
        self.role_permissions: Dict[str, Set[str]] = {
            'admin': {
                Permission.ADMIN,
                Permission.KICK_PLAYER,
                Permission.BAN_PLAYER,
                Permission.MODIFY_LOBBY,
                Permission.ADD_BOT,
                Permission.REMOVE_BOT,
                Permission.START_MATCH,
                Permission.VIEW_ANALYTICS
            },
            'moderator': {
                Permission.KICK_PLAYER,
                Permission.ADD_BOT,
                Permission.REMOVE_BOT
            },
            'player': set()
        }
    
    def grant_permission(self, player_id: str, permission: str):
        if player_id not in self.player_permissions:
            self.player_permissions[player_id] = set()
        self.player_permissions[player_id].add(permission)
    
    def revoke_permission(self, player_id: str, permission: str):
        if player_id in self.player_permissions:
            self.player_permissions[player_id].discard(permission)
    
    def has_permission(self, player_id: str, permission: str) -> bool:
        if player_id in self.player_permissions:
            return permission in self.player_permissions[player_id]
        return False
    
    def assign_role(self, player_id: str, role: str):
        if role in self.role_permissions:
            self.player_permissions[player_id] = self.role_permissions[role].copy()
    
    def get_permissions(self, player_id: str) -> Set[str]:
        return self.player_permissions.get(player_id, set())
    
    def is_admin(self, player_id: str) -> bool:
        return self.has_permission(player_id, Permission.ADMIN)
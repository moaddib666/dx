from enum import StrEnum
import uuid


class Channel(StrEnum):
    WORLD = "world::global"
    MASTER = "world::master"
    
    @classmethod
    def character(cls, character_id: str) -> str:
        """Generate a character-specific channel."""
        return f"world::character::{character_id}"

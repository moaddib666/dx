from pydantic import BaseModel


class MessageMeta(BaseModel):
    pass


class MessageData(BaseModel):
    pass


class Message(BaseModel):
    name: str
    meta: MessageMeta
    data: MessageData

    def serialize(self, serializer):
        return serializer(self.dict())

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Interfaces(BaseModel):
    screen: Optional[Dict[str, Any]]
    payments: Dict[str, Any]
    account_linking: Dict[str, Any]


class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: Interfaces


class User(BaseModel):
    user_id: str


class Application(BaseModel):
    application_id: str


class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: str
    user: User
    application: Application
    user_id: str
    new: bool


class Tokens(BaseModel):
    start: int
    end: int


class Entity(BaseModel):
    type: str
    tokens: Tokens
    value: Any


class Nlu(BaseModel):
    tokens: List[str]
    entities: List[Entity]
    intents: Dict[str, Any]


class Markup(BaseModel):
    dangerous_context: bool


class Request(BaseModel):
    command: str
    original_utterance: str
    nlu: Nlu
    markup: Markup
    type: str


class AliceRequest(BaseModel):
    meta: Meta
    session: Session
    request: Request
    version: str


class ResponsePart(BaseModel):
    text: str
    end_session: bool


class AliceResponse(BaseModel):
    version: str
    session_id: str
    response: ResponsePart

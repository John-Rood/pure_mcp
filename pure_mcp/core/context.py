from dataclasses import dataclass
from typing import Any, Generic, Union

from typing_extensions import TypeVar

from .session import BaseSession
from ..types.protocol import RequestId, RequestParams

SessionT = TypeVar("SessionT", bound=BaseSession[Any, Any, Any, Any, Any])
LifespanContextT = TypeVar("LifespanContextT")
RequestT = TypeVar("RequestT", default=Any)


@dataclass
class RequestContext(Generic[SessionT, LifespanContextT, RequestT]):
    request_id: RequestId
    meta: Union[RequestParams.Meta, None]
    session: SessionT
    lifespan_context: LifespanContextT
    request: Union[RequestT, None] = None

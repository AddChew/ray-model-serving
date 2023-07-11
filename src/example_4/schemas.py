from pydantic import BaseModel
from typing import Literal, List


class BaseAlert(BaseModel):
    input_name: str
    match_name: str


class DOBAlert(BaseAlert):
    input_dob: str
    match_dob: str


class BasePayload(BaseModel):
    model: Literal['BASE.PERSON', 'BASE.CORPORATE', 'BASE.ALL']
    alerts: List[BaseAlert]


class DOBPayload(BaseModel):
    model: Literal['DOB.PERSON', 'DOB.CORPORATE', 'DOB.ALL']
    alerts: List[DOBAlert]


class Prediction(BaseModel):
    label: str
    score: float


class Message(BaseModel):
    detail: str
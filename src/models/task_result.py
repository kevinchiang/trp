import datetime
import pydantic
from typing import Optional, List


class TaskParameter(pydantic.BaseModel):
    id: Optional[int]
    task_id: Optional[int]
    base_id: Optional[int]
    name: str
    type: str
    start_time: datetime.datetime
    duration: Optional[int]
    value_numeric: Optional[float] | Optional[int]
    value_string: Optional[str]
    comparator: str
    lsl: Optional[float] | Optional[int]
    usl: Optional[float] | Optional[int]
    expected_value: str
    status: str


class TaskResult(pydantic.BaseModel):
    id: Optional[int]
    serial_number: str
    start_time: datetime.datetime
    duration: Optional[int]
    test_status: int
    actor: str
    task_parameters: List[TaskParameter]

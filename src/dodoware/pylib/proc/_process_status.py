from typing import List, Union

from pydantic import BaseModel


class ProcessStatus(BaseModel):
    """
    Process status information.
    """

    begin_timestamp:Union[str, None]
    end_timestamp:Union[str, None]
    elaped_time:Union[float, None]
    return_code:Union[int, None]
    runner_exception:Union[str, None]
    stdout_exception:Union[str, None]
    stderr_exception:Union[str, None]
    stdout_lines:Union[List[str], None]
    stderr_lines:Union[List[str], None]

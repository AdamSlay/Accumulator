from dataclasses import dataclass


@dataclass
class Parm:
    parameters: list[tuple[str, str]]  # [(parm, unit), (parm, unit), ...]

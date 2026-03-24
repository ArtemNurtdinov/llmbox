from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationConfig:
    host: str
    port: int

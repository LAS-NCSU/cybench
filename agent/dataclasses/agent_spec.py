from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Dict


@dataclass(frozen=True)
class AgentConfig:
    """
    Dataclass that represents agent config
    """
    deployment_name: str   # ex "openai/o1-mini-2024-09-12"
    model: str             # name of the model (read from cli)
    provider: str          # for first-party hosted model
    tokenizer: str = None  # optional, for models that need it

    def __post_init__(self):
        if self.provider is None or self.model is None:
            raise ValueError("--provider and --model must be specified.")

    @staticmethod
    def from_dict(d: dict) -> "AgentConfig":
        for field in ["provider", "model", "tokenizer"]:
            if field not in d:
                d[field] = None
        if "deployment_name" not in d:
            d["deployment_name"] = d["provider"] + "/" + d["model"]
        return AgentConfig(
            deployment_name=d["deployment_name"],
            provider = d["provider"],
            model = d["model"],
            tokenizer = d["tokenizer"],
        )

@dataclass(frozen=True)
class IterationConfig:
    """
    Dataclass that represents config for a single iteration of a run
    """

    max_iterations: int
    iterations_until_hint: int

    @staticmethod
    def from_dict(d: dict) -> "IterationConfig":
        return IterationConfig(
            max_iterations=d["max_iterations"],
            iterations_until_hint=d["iterations_until_hint"],
        )

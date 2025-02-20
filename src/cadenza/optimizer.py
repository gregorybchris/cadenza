import logging
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator

import torch
from rich.console import Console
from torch import Tensor

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class OptimizerArgs:
    n_epochs: int
    learning_rate: float
    max_denominator: int
    convergence_threshold: float
    status_interval: int


@dataclass(kw_only=True)
class Optimizer:
    args: OptimizerArgs

    def optimize(self, frequencies: Tensor) -> Tensor:
        chord = frequencies.clone().detach().requires_grad_(True)
        optim = torch.optim.Adam([chord], lr=self.args.learning_rate)
        for i in range(self.args.n_epochs):
            optim.zero_grad()
            loss = self._ratio_simplicity_loss(chord, max_denominator=self.args.max_denominator)
            loss.backward()  # type: ignore
            optim.step()

            if i % self.args.status_interval == 0:
                logger.debug(f"Iteration {i:3d}, Loss: {loss.item():.6f}, Chord: {chord.detach().numpy().round(1)}")  # noqa: G004

            if loss < self.args.convergence_threshold:
                logger.debug(f"Converged at iteration {i}")  # noqa: G004
                break

        return chord.detach()

    @classmethod
    def _find_approximate_fraction(cls, x: float, max_denominator: int) -> Fraction:
        return Fraction(x).limit_denominator(max_denominator)

    @classmethod
    def _approximate(cls, t: Tensor, max_denominator: int) -> Tensor:
        values = [float(cls._find_approximate_fraction(x.item(), max_denominator)) for x in t]
        return torch.tensor(values, dtype=t.dtype)

    @classmethod
    def _compute_ratios(cls, chord: Tensor) -> Tensor:
        ratios = []
        for i in range(len(chord)):
            for j in range(i + 1, len(chord)):
                ratios.append(chord[j] / chord[i])
        return torch.stack(ratios)

    @classmethod
    def _ratio_simplicity_loss(cls, chord: Tensor, *, max_denominator: int) -> Tensor:
        ratios = cls._compute_ratios(chord)
        approximate_ratios = cls._approximate(ratios, max_denominator)
        return torch.sum((ratios - approximate_ratios) ** 2)

    @classmethod
    def _iter_ratios(cls, frequencies: Tensor) -> Iterator[tuple[float, float, float]]:
        for i in range(len(frequencies)):
            for j in range(i + 1, len(frequencies)):
                low_note = frequencies[i].item()
                high_note = frequencies[j].item()
                yield (high_note, low_note, high_note / low_note)

    def print_frequency_ratios(self, console: Console, frequencies: Tensor) -> None:
        for high_note, low_note, ratio in self._iter_ratios(frequencies):
            approximate_fraction = self._find_approximate_fraction(ratio, self.args.max_denominator)
            approximate_fraction_value = float(approximate_fraction)
            numerator = approximate_fraction.numerator
            denominator = approximate_fraction.denominator
            error = abs(ratio - approximate_fraction_value) / ratio * 100
            console.print(
                f"[reset]Ratio ([yellow]{high_note:.1f}[reset] / [yellow]{low_note:.1f}[reset]) ="
                f" [bold][yellow]{ratio:.4f}[reset] |"
                f" closest fraction = [blue]{numerator!s:>2}/{denominator!s:<2}[reset]"
                f" ([bold][blue]{approximate_fraction_value:.3f}[reset]) |"
                f" error = [bold][red]{error:.2f}%[reset]"
            )

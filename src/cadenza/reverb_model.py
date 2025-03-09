import torch
from torch import Tensor


class ReverbModel(torch.nn.Module):
    buffer: Tensor

    def __init__(self, delay_samples: int, feedback: float) -> None:
        super().__init__()
        self.delay_samples: int = delay_samples
        self.feedback: float = feedback
        self.register_buffer("buffer", torch.zeros(delay_samples))

    def forward(self, x: Tensor) -> Tensor:
        n: int = x.shape[0]
        y: Tensor = torch.zeros_like(x)

        for i in range(0, n, self.delay_samples):  # Process in chunks
            chunk: Tensor = x[i : i + self.delay_samples]
            buffer_out: Tensor = self.buffer[: chunk.shape[0]]
            y[i : i + self.delay_samples] = chunk + buffer_out * self.feedback

            self.buffer = torch.roll(self.buffer, -chunk.shape[0], dims=0)
            self.buffer[-chunk.shape[0] :] = y[i : i + chunk.shape[0]]

        return y

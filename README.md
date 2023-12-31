# A WandB Water & Carbon Metering Plug-in

A [wandb](https://github.com/wandb/wandb/) and [codecarbon](https://github.com/mlco2/codecarbon) wrapper that logs on cloud the water and carbon consumption of your experiments. This code is associated to the paper Zuccon, Scells, Zhuang. [Beyond CO2 Emissions: The Overlooked Impact of Water Consumption of Information Retrieval Models](https://ielab.io/green-ir), ICTIR 2023. For more of our [Green Information Retrieval]() research, visit the github repository [https://github.com/ielab/green-ir](https://github.com/ielab/green-ir).

## Installation

```bash
pip install wandc
```

## Usage
### Basic usage
```python
from wandc.emissions_logger import log_emissions

@log_emissions()
def your_function_to_track(project_name='your project name'):
  # your code
```
For other useful parameters see codecarbon documentation [here](https://mlco2.github.io/codecarbon/parameters.html).

### Tracking emissions of transformers trainer

```python
from wandc.emissions_logger import log_emissions
from transformers import Trainer

class WandcTrainer(Trainer):
    @log_emissions()
    def train(
        self,
        ...,
        **kwargs,
    ):
        super().train(..., **kwargs)

trainer = WandcTrainer(...)
trainer.train()
```

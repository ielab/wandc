from codecarbon import EmissionsTracker, OfflineEmissionsTracker
import wandb
from functools import wraps
from typing import Callable, Optional
from codecarbon.external.logger import logger
from .logger import logger, set_logger_level, set_logger_format

_sentinel = object()


def log_emissions(
    fn: Callable = None,
    project_name: Optional[str] = 'wandc',
    run_name: Optional[str] = None,
    offline: Optional[bool] = _sentinel,
    country_iso_code: Optional[str] = _sentinel,
    cloud_provider: Optional[str] = _sentinel,
    log_level: Optional[str] = "info",
    logger_preamble: Optional[str] = "",

    **kwargs,
):
    def _decorate(fn: Callable):
        set_logger_level(log_level)
        set_logger_format(logger_preamble)

        if offline and offline is not _sentinel:
            if (country_iso_code is None or country_iso_code is _sentinel) and (
                    cloud_provider is None or cloud_provider is _sentinel
            ):
                raise Exception("Needs ISO Code of the Country for Offline mode")
            tracker = OfflineEmissionsTracker(
                project_name=project_name,
                **kwargs,
            )
        else:
            tracker = EmissionsTracker(
                project_name=project_name,
                **kwargs,
            )

        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            fn_result = None
            tracker.start()
            try:
                fn_result = fn(*args, **kwargs)
            finally:
                logger.info(
                    "Graceful stopping: collecting and writing information. Please wait a few seconds..."
                )
                tracker.stop()

                if wandb.run is not None:
                    run = wandb.run
                else:
                    run = wandb.init(project=project_name, name=run_name)

                emissions_data = tracker.final_emissions_data
                columns = ['function']
                data = [fn.__name__]
                columns.extend(list(emissions_data.values.keys()))
                data.extend(list(emissions_data.values.values()))
                emissions_table = wandb.Table(columns=columns,
                                              data=[data])

                logger.info(f"Function '{fn.__name__}' total CO2 emissions: %s kg" % emissions_data.emissions)
                run.log({f"Emissions": emissions_table})

            return fn_result

        return wrapped_fn

    if fn:
        return _decorate(fn)
    return _decorate
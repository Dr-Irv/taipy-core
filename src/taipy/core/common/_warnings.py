# Copyright 2022 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import functools
import warnings

warnings.simplefilter("once", ResourceWarning)


def _warn_deprecated(deprecated: str, suggest: str = None, stacklevel: int = 3) -> None:
    category = DeprecationWarning
    message = f"{deprecated} is deprecated."
    if suggest:
        message += f" Use {suggest} instead."
    warnings.warn(message=message, category=category, stacklevel=stacklevel)


def _warn_no_core_service(stacklevel: int = 3):
    def inner(f):
        @functools.wraps(f)
        def _check_if_core_service_is_running(*args, **kwargs):
            from .._scheduler._scheduler_factory import _SchedulerFactory

            if not _SchedulerFactory._dispatcher:
                message = "The Core service is NOT running"
                warnings.warn(message=message, category=ResourceWarning, stacklevel=stacklevel)

            return f(*args, **kwargs)

        return _check_if_core_service_is_running

    return inner

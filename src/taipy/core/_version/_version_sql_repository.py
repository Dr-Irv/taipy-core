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


from typing import Optional

from ._version_model import _VersionModel
from ._version_repository import _VersionRepository


class _VersionSQLRepository(_VersionRepository):
    _LATEST_VERSION_KEY = "latest_version"
    _DEVELOPMENT_VERSION_KEY = "development_version"
    _PRODUCTION_VERSION_KEY = "production_version"

    def __init__(self):
        super().__init__(model=_VersionModel, model_name="version")

    def _load_all_by(self, by, version_number: Optional[str] = "all"):
        return super()._load_all_by(by, version_number)

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

import json
from typing import List

from taipy.logger._taipy_logger import _TaipyLogger

from ..exceptions.exceptions import VersionIsNotProductionVersion
from ._version_model import _VersionModel
from ._version_repository import _VersionRepository


class _VersionFSRepository(_VersionRepository):
    def __init__(self):
        super().__init__(model=_VersionModel, dir_name="version")

    @property
    def dir_path(self):
        return super().repository.dir_path

    @property
    def _version_file_path(self):
        return super().repository._storage_folder / "version.json"

    def _delete_all(self):
        super()._delete_all()

        if self._version_file_path.exists():
            self._version_file_path.unlink()

    def _set_latest_version(self, version_number):
        if self._version_file_path.exists():
            with open(self._version_file_path, "r") as f:
                file_content = json.load(f)

            file_content[self._LATEST_VERSION_KEY] = version_number

        else:
            self.dir_path.mkdir(parents=True, exist_ok=True)
            file_content = {
                self._LATEST_VERSION_KEY: version_number,
                self._DEVELOPMENT_VERSION_KEY: "",
                self._PRODUCTION_VERSION_KEY: [],
            }

        self._version_file_path.write_text(
            json.dumps(
                file_content,
                ensure_ascii=False,
                indent=0,
            )
        )

    def _get_latest_version(self) -> str:
        with open(self._version_file_path, "r") as f:
            file_content = json.load(f)

        return file_content[self._LATEST_VERSION_KEY]

    def _set_development_version(self, version_number):
        if self._version_file_path.exists():
            with open(self._version_file_path, "r") as f:
                file_content = json.load(f)

            file_content[self._DEVELOPMENT_VERSION_KEY] = version_number
            file_content[self._LATEST_VERSION_KEY] = version_number

        else:
            self.dir_path.mkdir(parents=True, exist_ok=True)
            file_content = {
                self._LATEST_VERSION_KEY: version_number,
                self._DEVELOPMENT_VERSION_KEY: version_number,
                self._PRODUCTION_VERSION_KEY: [],
            }

        self._version_file_path.write_text(
            json.dumps(
                file_content,
                ensure_ascii=False,
                indent=0,
            )
        )

    def _get_development_version(self) -> str:
        with open(self._version_file_path, "r") as f:
            file_content = json.load(f)

        return file_content[self._DEVELOPMENT_VERSION_KEY]

    def _set_production_version(self, version_number):
        if self._version_file_path.exists():
            with open(self._version_file_path, "r") as f:
                file_content = json.load(f)

            file_content[self._LATEST_VERSION_KEY] = version_number
            if version_number not in file_content[self._PRODUCTION_VERSION_KEY]:
                file_content[self._PRODUCTION_VERSION_KEY].append(version_number)
            else:
                _TaipyLogger._get_logger().info(f"Version {version_number} is already a production version.")

        else:
            self.dir_path.mkdir(parents=True, exist_ok=True)
            file_content = {
                self._LATEST_VERSION_KEY: version_number,
                self._DEVELOPMENT_VERSION_KEY: "",
                self._PRODUCTION_VERSION_KEY: [version_number],
            }

        self._version_file_path.write_text(
            json.dumps(
                file_content,
                ensure_ascii=False,
                indent=0,
            )
        )

    def _get_production_version(self) -> List[str]:
        with open(self._version_file_path, "r") as f:
            file_content = json.load(f)

        return file_content[self._PRODUCTION_VERSION_KEY]

    def _delete_production_version(self, version_number):
        try:
            with open(self._version_file_path, "r") as f:
                file_content = json.load(f)

            if version_number not in file_content[self._PRODUCTION_VERSION_KEY]:
                raise VersionIsNotProductionVersion(f"Version {version_number} is not a production version.")

            file_content[self._PRODUCTION_VERSION_KEY].remove(version_number)

            self._version_file_path.write_text(
                json.dumps(
                    file_content,
                    ensure_ascii=False,
                    indent=0,
                )
            )

        except FileNotFoundError:
            raise VersionIsNotProductionVersion(f"Version {version_number} is not a production version.")

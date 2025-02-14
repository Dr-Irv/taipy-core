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

from src.taipy.core.scenario._scenario_repository_factory import _ScenarioRepositoryFactory
from src.taipy.core.scenario._scenario_sql_repository import _ScenarioSQLRepository
from src.taipy.core.scenario.scenario import Scenario
from taipy.config.config import Config


def test_save_and_load(tmpdir, scenario):
    repository = _ScenarioRepositoryFactory._build_repository()
    repository.base_path = tmpdir
    repository._save(scenario)
    sc = repository.load(scenario.id)

    assert isinstance(sc, Scenario)
    assert scenario.id == sc.id


def test_from_and_to_model(scenario, scenario_model):
    repository = _ScenarioRepositoryFactory._build_repository()
    assert repository._to_model(scenario) == scenario_model
    assert repository._from_model(scenario_model) == scenario


def test_save_and_load_with_sql_repo(tmpdir, scenario):
    Config.configure_global_app(repository_type="sql")

    repository = _ScenarioRepositoryFactory._build_repository()
    repository._save(scenario)
    sc = repository.load(scenario.id)

    assert isinstance(sc, Scenario)
    assert scenario.id == sc.id


def test_from_and_to_model_with_sql_repo(scenario, scenario_model):
    Config.configure_global_app(repository_type="sql")

    repository = _ScenarioRepositoryFactory._build_repository()

    assert repository._to_model(scenario) == scenario_model
    assert repository._from_model(scenario_model) == scenario

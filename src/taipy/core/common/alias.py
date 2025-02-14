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

from typing import NewType, Any, Dict

PipelineId = NewType("PipelineId", str)
PipelineId.__doc__ = """Type that holds a `Pipeline^` identifier."""
ScenarioId = NewType("ScenarioId", str)
ScenarioId.__doc__ = """Type that holds a `Scenario^` identifier."""
TaskId = NewType("TaskId", str)
TaskId.__doc__ = """Type that holds a `Task^` identifier."""
JobId = NewType("JobId", str)
JobId.__doc__ = """Type that holds a `Job^` identifier."""
CycleId = NewType("CycleId", str)
CycleId.__doc__ = """Type that holds a `Cycle^` identifier."""
DataNodeId = NewType("DataNodeId", str)
DataNodeId.__doc__ = """Type that holds a `DataNode^` identifier."""
Edit = NewType("Edit", Dict[str, Any])
Edit.__doc__ = """Type that holds a `DataNode^` edit information."""

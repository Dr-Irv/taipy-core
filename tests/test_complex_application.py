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

import os
import pathlib
from time import sleep

import pandas as pd

import src.taipy.core.taipy as tp
from src.taipy.core import Status
from src.taipy.core._scheduler._scheduler_factory import _SchedulerFactory
from src.taipy.core.config.job_config import JobConfig
from taipy.config import Config

# ################################  USER FUNCTIONS  ##################################


def sum(a, b):
    a = a["number"]
    b = b["number"]
    return a + b


def subtract(a, b):
    a = a["number"]
    b = b["number"]
    return a - b


def mult(a, b):
    return a * b


def mult_by_2(a):
    return a


def divide(a, b):
    return a / b


def average(a):
    return [a.sum() / len(a)]


def div_constant_with_sleep(a):
    sleep(1)
    return a["number"] / 10


def return_a_number():
    return 10


def return_a_number_with_sleep():
    sleep(1)
    return 10


# ################################  TEST METHODS    ##################################


def test_skipped_jobs():
    Config.configure_job_executions(mode=JobConfig._DEVELOPMENT_MODE)
    _SchedulerFactory._build_scheduler()
    input_config = Config.configure_data_node("input")
    intermediate_config = Config.configure_data_node("intermediate", cacheable=True)
    output_config = Config.configure_data_node("output", cacheable=True)
    task_config_1 = Config.configure_task("first", mult_by_2, input_config, intermediate_config)
    task_config_2 = Config.configure_task("second", mult_by_2, intermediate_config, output_config)
    pipeline_config = Config.configure_pipeline("pipeline", [task_config_1, task_config_2])

    pipeline = tp.create_pipeline(pipeline_config)
    pipeline.input.write(2)
    pipeline.submit()
    assert len(tp.get_jobs()) == 2
    for job in tp.get_jobs():
        assert job.status == Status.COMPLETED
    pipeline.submit()
    assert len(tp.get_jobs()) == 4
    skipped = []
    for job in tp.get_jobs():
        if job.status != Status.COMPLETED:
            assert job.status == Status.SKIPPED
            skipped.append(job)
    assert len(skipped) == 2


def test_complex():
    # d1 --- t1
    # |
    # | --- t2 --- d5 --- |                   t10 --- d12
    #        |            |                   |
    #        |            |                   |
    #        d2           | --- t5 --- d7 --- t7 --- d9 --- t8 --- d10 --- t9 --- d11
    #                     |                   |             |
    # d3 --- |            |                   |             |
    # |      |            |     t6 --- d8 -------------------
    # |      t3 --- d6 ---|
    # |      |
    # |      |
    # t4     d4

    Config.configure_job_executions(mode=JobConfig._DEVELOPMENT_MODE)
    _SchedulerFactory._build_scheduler()

    csv_path_inp = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/example.csv")
    excel_path_inp = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/example.xlsx")

    csv_path_sum = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/sum.csv")
    excel_path_sum = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/sum.xlsx")

    excel_path_out = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/res.xlsx")
    csv_path_out = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/res.csv")

    inp_csv_dn_1 = Config.configure_csv_data_node("dn_csv_in_1", default_path=csv_path_inp)
    inp_csv_dn_2 = Config.configure_csv_data_node("dn_csv_in_2", default_path=csv_path_inp)

    inp_excel_dn_1 = Config.configure_excel_data_node("dn_excel_in_1", default_path=excel_path_inp, sheet_name="Sheet1")
    inp_excel_dn_2 = Config.configure_excel_data_node("dn_excel_in_2", default_path=excel_path_inp, sheet_name="Sheet1")

    placeholder = Config.configure_data_node("dn_placeholder", default_data=10)

    dn_csv_sum = Config.configure_csv_data_node("dn_sum_csv", default_path=csv_path_sum)
    dn_excel_sum = Config.configure_excel_data_node("dn_sum_excel", default_path=excel_path_sum, sheet_name="Sheet1")

    dn_subtract_csv_excel = Config.configure_pickle_data_node("dn_subtract_csv_excel")
    dn_mult = Config.configure_pickle_data_node("dn_mult")
    dn_div = Config.configure_pickle_data_node("dn_div")

    output_csv_dn = Config.configure_csv_data_node("csv_out", csv_path_out)
    output_excel_dn = Config.configure_excel_data_node("excel_out", excel_path_out)

    task_print_csv = Config.configure_task("task_print_csv", print, input=inp_csv_dn_1)
    task_print_excel = Config.configure_task("task_print_excel", print, input=inp_excel_dn_1)
    task_sum_csv = Config.configure_task("task_sum_csv", sum, input=[inp_csv_dn_2, inp_csv_dn_1], output=dn_csv_sum)
    task_sum_excel = Config.configure_task(
        "task_sum_excel", sum, input=[inp_excel_dn_2, inp_excel_dn_1], output=dn_excel_sum
    )

    task_subtract_csv_excel = Config.configure_task(
        "task_subtract_csv_excel", subtract, input=[dn_csv_sum, dn_excel_sum], output=dn_subtract_csv_excel
    )
    task_insert_placeholder = Config.configure_task("task_insert_placeholder", return_a_number, output=[placeholder])
    task_mult = Config.configure_task(
        "task_mult_by_placeholder", mult, input=[dn_subtract_csv_excel, placeholder], output=dn_mult
    )
    task_div = Config.configure_task("task_div_by_placeholder", divide, input=[dn_mult, placeholder], output=dn_div)
    task_avg_div = Config.configure_task("task_avg_div", average, input=dn_div, output=output_csv_dn)
    task_avg_mult = Config.configure_task("task_avg_mult", average, input=dn_mult, output=output_excel_dn)

    pipeline_sum_print_mul_print_avg_placeholder_mul = Config.configure_pipeline(
        "pipeline",
        [
            task_print_csv,
            task_print_excel,
            task_sum_csv,
            task_sum_excel,
            task_subtract_csv_excel,
            task_insert_placeholder,
            task_mult,
            task_div,
            task_avg_div,
            task_avg_mult,
        ],
    )

    scenario_config = Config.configure_scenario("scenario", [pipeline_sum_print_mul_print_avg_placeholder_mul])

    scenario = tp.create_scenario(scenario_config)

    tp.submit(scenario)

    csv_sum_res = pd.read_csv(csv_path_sum)
    excel_sum_res = pd.read_excel(excel_path_sum)
    csv_out = pd.read_csv(csv_path_out)
    excel_out = pd.read_excel(excel_path_out)
    assert csv_sum_res.to_numpy().flatten().tolist() == [i * 20 for i in range(1, 11)]
    assert excel_sum_res.to_numpy().flatten().tolist() == [i * 2 for i in range(1, 11)]
    assert average(csv_sum_res["number"] - excel_sum_res["number"]) == csv_out.to_numpy()[0]
    assert average((csv_sum_res["number"] - excel_sum_res["number"]) * 10) == excel_out.to_numpy()[0]

    for path in [csv_path_sum, excel_path_sum, csv_path_out, excel_path_out]:
        os.remove(path)


# def test_same_pipeline_submission_with_overlap_datanode():
#     Config.configure_job_executions(mode=JobConfig._STANDALONE_MODE, nb_of_workers=1)
#     _Scheduler._update_job_config()

#     # d1 ---- t1 ---- d2 ---- t2
#     # t3 ---- d2

#     csv_path_inp = os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/example.csv")

#     dn1_inp_csv = Config.configure_csv_data_node("dn1_inp_csv", default_path=csv_path_inp)
#     dn2_div = Config.configure_pickle_data_node("dn2_div")

#     task1_div_csv_with_constant = Config.configure_task(
#         "task1_div_csv_with_constant", div_constant_with_sleep, input=dn1_inp_csv, output=dn2_div
#     )
#     task2_print_pickle = Config.configure_task("task2_print_pickle", print_with_sleep, input=dn2_div)
#     task3_populate_constant = Config.configure_task(
#         "task3_populate_constant", return_a_number_with_sleep, output=dn2_div
#     )

#     pipeline_div_print_config = Config.configure_pipeline(
#         "pipeline_div_print", [task1_div_csv_with_constant, task2_print_pickle]
#     )
#     pipeline_populate_constant_config = Config.configure_pipeline(
#         "pipeline_populate_constant", [task3_populate_constant]
#     )

#     pipeline_div_print = tp.create_pipeline(pipeline_div_print_config)
#     pipeline_populate_constant = tp.create_pipeline(pipeline_populate_constant_config)

#     tp.submit(pipeline_div_print)
#     tp.submit(pipeline_div_print)
#     tp.submit(pipeline_populate_constant)

#     assert _Scheduler.jobs_to_run.qsize() == 2
#     assert pipeline_div_print.dn2_div.read() is None

#     sleep(1.5)
#     assert _Scheduler.jobs_to_run.qsize() == 2
#     assert pipeline_div_print.dn2_div.read() is not None
#     assert len(pipeline_div_print.dn2_div.read()) == 10

#     sleep(1)
#     assert _Scheduler.jobs_to_run.qsize() == 2
#     assert pipeline_div_print.dn2_div.read() is not None
#     assert len(pipeline_div_print.dn2_div.read()) == 10

#     sleep(1.5)
#     assert _Scheduler.jobs_to_run.qsize() == 0
#     assert pipeline_div_print.dn2_div.read() == 10

#     Config.configure_job_executions(mode=JobConfig._STANDALONE_MODE, nb_of_workers=2)
#     _Scheduler._update_job_config()

#     tp.submit(pipeline_div_print)
#     tp.submit(pipeline_div_print)

#     assert _Scheduler.jobs_to_run.qsize() == 0

#     sleep(2.5)
#     assert pipeline_div_print.dn2_div.read() is not None
#     assert len(pipeline_div_print.dn2_div.read()) == 10

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# TODO(mik-laj): We have to implement it.
#     Do you want to help? Please look at: https://github.com/apache/airflow/issues/8132
import operator
from flask import request
from airflow.utils.session import provide_session
from airflow.models import TaskInstance, DagRun
from airflow.api_connexion.schemas.task_instance_schema\
    import task_instance_schema, task_instance_collection_schema
from airflow.api_connexion import parameters

@provide_session
def get_task_instance(dag_id, dag_run_id, task_id, session):
    """
    Get a task instance
    """
    query = session.query(TaskInstance, DagRun)
    task_instance = query.filter(
        TaskInstance.dag_id == dag_id,
        TaskInstance.task_id == task_id
    ).filter(
        DagRun.id == dag_run_id,
    ).one_or_none()
    if task_instance is None:
        return response_404 #TODO(Gabriel): Implement and discuss solution for handling
    return task_instance_schema.dump(task_instance)


@provide_session
def get_task_instances(dag_id, dag_run_id, session):
    """
    Get list of task instances of DAG.
    """
    params = { #TODO(Gabriel) Look this over, not sure if it will work at all.
        parameters.FilterExecutionDateGTE: (TaskInstance.execution_date, operator.ge),
        parameters.FilterExecutionDateLTE: (TaskInstance.execution_date, operator.le),
        parameters.FilterStartDateGTE: (TaskInstance.start_date, operator.ge),
        parameters.FilterStartDateLTE: (TaskInstance.start_date, operator.le),
        parameters.FilterEndDateGTE: (TaskInstance.end_date, operator.ge),
        parameters.FilterEndDateLTE: (TaskInstance.end_date, operator.le),
        parameters.FilterDurationGTE: (TaskInstance.duration, operator.ge),
        parameters.FilterDurationLTE: (TaskInstance.duration, operator.le),
        parameters.FilterState: (TaskInstance.state, operator.eq),
        parameters.FilterPool: (TaskInstance.pool, operator.eq),
        parameters.FilterQueue: (TaskInstance.queue, operator.eq)
    }
    #task_instance_filters = reduce(lambda p, cur: cur.update({p: request.args.get(p)}), params, {})

    query = session.query(TaskInstance, DagRun)
    query = query.filter(
        TaskInstance.dag_id == dag_id,
        DagRun.id == dag_run_id,
    )
    for (param, (field, op)) in params.items():
        value = request.args.get(param)
        if value is not None:
            query = query.filter(op(field, param))

    offset = request.args.get(parameters.Offset, 0)
    limit = request.args.get(parameters.Limit, 100)
    query.offset(offset).limit(limit)

    task_instances = query.all()
    return task_instance_collection_schema.\
        dump(task_instances=task_instances, total_entries=len(task_instances))


def get_task_instances_batch():
    """
    Get list of task instances.
    """
    raise NotImplementedError("Not implemented yet.")


def post_clear_task_instances():
    """
    Clear task instances.
    """
    raise NotImplementedError("Not implemented yet.")

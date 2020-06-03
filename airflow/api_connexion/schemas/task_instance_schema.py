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

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from airflow.models import (TaskInstance, SlaMiss)

class SlaMissSchema(SQLAlchemySchema):
    """
    Schema for a SLAMiss
    """
    class Meta:
        """
        Meta
        """
        model = SlaMiss

    task_id = auto_field()
    dag_id = auto_field()
    execution_date = auto_field()
    email_sent = auto_field()
    timestamp = auto_field()
    description = auto_field()
    notification_sent = auto_field()


class TaskInstanceSchema(SQLAlchemySchema):
    """
    Schema for a TaskInstance
    """
    class Meta:
        """
        Meta
        """
        model = TaskInstance

    task_id = auto_field()
    dag_id = auto_field()
    execution_date = auto_field()
    start_date = auto_field()
    end_date = auto_field()
    duration = auto_field()
    state = auto_field() #Refs TaskState which is an enum
    try_number = auto_field()
    max_tries = auto_field()
    hostname = auto_field()
    unixname = auto_field()
    pool = auto_field()
    queue = auto_field()
    priority_weight = auto_field()
    operator = auto_field()
    queued_when = auto_field("queued_dttm")
    pid = auto_field()
    executor_config = auto_field()
    sla_miss = Nested(SlaMissSchema)

task_instance_schema = TaskInstanceSchema()

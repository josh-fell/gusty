import pytest
from gusty import create_dag
from gusty.utils import days_ago
from datetime import timedelta

###############
## FIXTURES ##
###############


@pytest.fixture(scope="session")
def multi_task_dir():
    return "tests/dags/multi_task"


@pytest.fixture(scope="session")
def dag(multi_task_dir):
    dag = create_dag(
        multi_task_dir,
        description="A dag created without metadata",
        schedule_interval="0 0 * * *",
        default_args={
            "owner": "gusty",
            "depends_on_past": False,
            "start_date": days_ago(1),
            "email": "gusty@gusty.com",
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": 3,
            "retry_delay": timedelta(minutes=5),
        },
        latest_only=False,
    )
    return dag


###########
## TESTS ##
###########


def test_multiple_tasks_exist(dag):
    assert "bash_a" in dag.task_dict.keys()
    assert "bash_b" in dag.task_dict.keys()
    assert "bash_c" in dag.task_dict.keys()
    assert "multi_bash" not in dag.task_dict.keys()


def test_multiple_tasks_changed(dag):
    bash_a_cmd = dag.task_dict["bash_a"].__dict__["bash_command"]
    bash_b_cmd = dag.task_dict["bash_b"].__dict__["bash_command"]
    assert bash_a_cmd == "echo a"
    assert bash_b_cmd == "echo b"


def test_multiple_tasks_defaults(dag):
    bash_c_cmd = dag.task_dict["bash_c"].__dict__["bash_command"]
    assert bash_c_cmd == "echo default"

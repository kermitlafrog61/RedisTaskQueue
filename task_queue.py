import asyncio
import logging
import pickle
import threading
import uuid

import redis

logging.basicConfig(level=logging.INFO)


class Task:
    """
    Task object.
    :param name: name of the task
    :param expected_result: expected result of the task
    """

    def __init__(self, name: str, expected_result: str) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.expected_result = expected_result


def add_task(task: Task):
    """
    Adding task to the queue.

    :param task: Task object
    """
    r = redis.Redis()

    r.rpush('task_queue', str(task.id))
    task_data = pickle.dumps(task)

    r.set(f'task:{task.id}', task_data)

    logging.info(f'Task with ID {task.id} added to the queue.')


async def _process_tasks():
    r = redis.Redis()

    while True:
        task_id = r.lpop('task_queue')

        if task_id:
            task_id = task_id.decode()
            task = r.get(f'task:{task_id}')
            task: Task = pickle.loads(task)
            r.delete(f'task:{task_id}')
            logging.info(f'Task {task.name} is processing...')
            await asyncio.sleep(3)

            r.set(f'result:{task_id}', task.expected_result)
        else:
            await asyncio.sleep(0.1)


def get_result(task_id: int):
    """
    Getting result of the task.
    :param task_id: uuid of task you need
    """
    r = redis.Redis()
    result = r.get(f'result:{task_id}')
    if result:
        logging.info(result.decode())
    else:
        logging.info(f"Task {task_id} is not finished yet")


def get_process_task_thread():
    """
    Getting thread for processing tasks.
    :return: thread
    """
    loop = asyncio.new_event_loop()
    loop.create_task(_process_tasks())
    process_tasks_thread = threading.Thread(target=loop.run_forever)

    return process_tasks_thread

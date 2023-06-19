import threading

from task_queue import get_process_task_thread, add_task, get_result, Task


class Interface:
    @staticmethod
    def add_task():
        name = input("Input task name: ")
        result = input("Input task result: ")
        task = Task(name, result)
        add_task(task)

    @staticmethod
    def get_result():
        id = input("Input task id: ")
        get_result(id)


def process_input():
    interface = Interface()

    while True:
        method = input("""
Input preferred method:
    add_task
    get_result
""")
        try:
            getattr(interface, method)()
        except AttributeError:
            print("Method not found")


if __name__ == "__main__":
    process_tasks_thread = get_process_task_thread()
    input_thread = threading.Thread(target=process_input)

    process_tasks_thread.start()
    input_thread.start()

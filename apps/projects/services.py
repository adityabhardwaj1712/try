from .models import Task

class TaskService:

    @staticmethod
    def move_task(task, new_status):
        task.status = new_status
        task.save(update_fields=["status"])
        return task

    @staticmethod
    def assign_task(task, user):
        task.assignee = user
        task.save(update_fields=["assignee"])
        return task

    @staticmethod
    def archive_task(task):
        task.is_archived = True
        task.save(update_fields=["is_archived"])
        return task
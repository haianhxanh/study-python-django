from enum import Enum


class RoleEnum(Enum):
    # name  = value
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

    @staticmethod
    def from_str(value: str):
        for member in RoleEnum:
            if value == member.value:
                return member

        raise ValueError(f"No member found for value {value}")


# RoleChoices = [(member.name, member.value) for member in RoleEnum]

class ProjectStatusEnum(Enum):
    DONE = 'done'
    IN_PROGRESS = 'in progress'
    ARCHIVED = 'archived'
    CREATED = 'created'


ProjectStatusChoices = [(status.name, status.value) for status in ProjectStatusEnum]


class TaskStatusEnum(Enum):
    DONE = 'done'
    IN_PROGRESS = 'in progress'
    CANCELLED = 'cancelled'
    TO_DO = "to do"


TaskStatusChoices = [(status.name, status.value) for status in TaskStatusEnum]

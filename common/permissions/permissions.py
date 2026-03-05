def is_admin(user):
    return user.role == "ADMIN"


def is_admin_or_manager(user):
    return user.role in ["ADMIN", "MANAGER"]


def can_edit(user):
    return user.role in ["ADMIN", "MANAGER", "DEVELOPER"]


def read_only(user):
    return user.role == "VIEWER"
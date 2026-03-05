def is_admin(request):
    return request.role == "admin"


def is_manager(request):
    return request.role in ["admin", "manager"]


def can_edit(request):
    return request.role in ["admin", "manager", "developer"]


def read_only(request):
    return request.role == "viewer"
from django.core.cache import cache


def cache_kanban(org_id, data):
    cache.set(f"kanban_{org_id}", data, timeout=300)


def get_cached_kanban(org_id):
    return cache.get(f"kanban_{org_id}")


def invalidate_kanban_cache(org_id):
    cache.delete(f"kanban_{org_id}")
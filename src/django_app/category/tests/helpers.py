def init_category_resource_all_none(category_resource_class, **kwargs):
    default = {
        "create_use_case": None,
        "list_use_case": None,
        "get_use_case": None,
        "update_use_case": None,
        "delete_use_case": None,
    } | kwargs
    return category_resource_class(**default)

from wagtail import hooks


@hooks.register("construct_main_menu")
def hide_explorer_for_non_superusers(request, menu_items):
    if not request.user.is_superuser:
        menu_items[:] = [item for item in menu_items if item.name != "explorer"]

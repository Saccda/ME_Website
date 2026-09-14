from wagtail import hooks

from .models import NewsEvent
from .photo_titles import name_story_gallery


@hooks.register("construct_main_menu")
def hide_explorer_for_non_superusers(request, menu_items):
    if not request.user.is_superuser:
        menu_items[:] = [item for item in menu_items if item.name != "explorer"]


# After the save rather than inside NewsEvent.save(): Wagtail runs these once
# the whole form is stored, gallery rows included, so the photos an editor has
# just added are in the database to be named.
@hooks.register("after_create_snippet")
@hooks.register("after_edit_snippet")
def name_story_gallery_photos(request, instance):
    """Name a saved story's device-named gallery photos after the story."""
    if isinstance(instance, NewsEvent):
        name_story_gallery(instance)

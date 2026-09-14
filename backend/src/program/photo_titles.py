"""Names for gallery photos that arrive carrying a device's file name.

Wagtail copies an uploaded file's name into the image title. Photos saved out
of Telegram, or taken straight off a phone or camera, therefore arrive titled
photo_1_2026-08-21_17-13-07 or IMG_8617 -- and the title is what the image
library lists, what its search matches, and what a screen reader announces for
a gallery photo that has no caption.

Renaming forty photos by hand is not a job anyone does. So a photo whose title
is still a device's file name is named after the story whose gallery it joins,
numbered by its place in that gallery: "Staff training with CJDM – photo 7".

Only device names are replaced. A title someone chose, even a terse one such
as Communities_10, says what its author meant and is left alone.
"""

import re

# The file-name conventions of the phones, cameras and apps these photos come
# from. A pattern belongs here only if nobody would plausibly type it as a name.
DEVICE_NAME = re.compile(
    r"""
    ^(?:
        photo_(?:\d+_)?\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}    # Telegram export
      | IMG[_-]?E?\d{3,}(?:[_-](?:WA)?\d+)*                    # iPhone, Android, WhatsApp
      | (?:PXL|VID|MVIMG)_\d{8}_\d+(?:[._~-]\w+)*             # Pixel and other Android
      | DSC[FN_]?\d{3,}                                        # Sony, Nikon, Fujifilm
      | GOPR\d{4}                                              # GoPro
      | \d{8}[_-]\d{6}(?:[_-]\d+)?                             # Samsung and others
      | WhatsApp[ ]Image[ ]\d{4}-\d{2}-\d{2}[ ]at[ ][\d.]+     # WhatsApp desktop
      | Screen[ _]?shot[ _-].*                                 # a screenshot
      | (?:image|photo|picture|unnamed)(?:[ _-]?\d+)?          # an app's default
    )
    (?:[ ]?\(\d+\))?                                           # a duplicate's "(1)"
    (?:\.(?:jpe?g|png|heic|heif|webp))?                        # an extension left on
    $
    """,
    re.IGNORECASE | re.VERBOSE,
)

# wagtailimages.Image.title
TITLE_LENGTH = 255


def is_device_name(title):
    return bool(DEVICE_NAME.match((title or "").strip()))


def gallery_photo_title(story_title, position):
    """The story's title and the photo's place in its gallery, cut to fit."""
    suffix = f" – photo {position}"
    return story_title.strip()[: TITLE_LENGTH - len(suffix)] + suffix


def name_story_gallery(story, *, dry_run=False):
    """Name the story's device-named gallery photos, in gallery order.

    Numbered by position among all the story's photos, so photo 7 is the
    seventh picture in the gallery whichever of its neighbours kept a typed
    name. Saved one at a time rather than in a bulk update, so Wagtail's image
    search picks up the new names. Returns (old, new) title pairs.
    """
    entries = sorted(
        story.gallery_images.all(),
        key=lambda entry: (entry.sort_order is None, entry.sort_order or 0, entry.pk or 0),
    )
    changes = []
    for position, entry in enumerate(entries, start=1):
        image = entry.image
        if not is_device_name(image.title):
            continue
        title = gallery_photo_title(story.title, position)
        changes.append((image.title, title))
        if not dry_run:
            image.title = title
            image.save(update_fields=["title"])
    return changes

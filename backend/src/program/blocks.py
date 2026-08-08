"""Content blocks for story bodies.

A StreamField is what gives authors the arrangement they expect in Wagtail: a
body is a list of blocks that can be added, reordered by dragging, and removed
independently, rather than one fixed field. Each block below is deliberately
small, so a story is assembled from parts instead of formatted inside a single
rich-text box.
"""

from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(
        required=False,
        max_length=250,
        help_text="Shown under the image.",
    )
    alt_text = blocks.CharBlock(
        required=False,
        max_length=250,
        help_text=(
            "Describes the image for screen readers. Leave empty if the image "
            "is decorative and the caption already says what it shows."
        ),
    )

    class Meta:
        icon = "image"
        label = "Image"


class GalleryBlock(blocks.StructBlock):
    """Two or three images across one row, as a set rather than one after another."""

    images = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("alt_text", blocks.CharBlock(required=False, max_length=250)),
            ]
        ),
        min_num=2,
        max_num=3,
    )
    caption = blocks.CharBlock(
        required=False,
        max_length=250,
        help_text="Shown under the row.",
    )

    class Meta:
        icon = "image"
        label = "Image row"


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock()
    attribution = blocks.CharBlock(required=False, max_length=160)

    class Meta:
        icon = "openquote"
        label = "Quote"


class VideoBlock(blocks.StructBlock):
    """A video, either hosted elsewhere or uploaded here.

    Give a link for anything long: this server has no adaptive streaming and
    sends the whole file on every play. Upload a file for a short clip that
    should not depend on an outside account.
    """

    url = blocks.URLBlock(
        required=False,
        help_text="A YouTube, Vimeo, or Facebook link. Leave empty if uploading a file.",
    )
    video_file = DocumentChooserBlock(
        required=False,
        help_text="An uploaded .mp4 or .webm, up to 100MB. Used when there is no link.",
    )
    caption = blocks.CharBlock(required=False, max_length=250)
    poster = ImageChooserBlock(
        required=False,
        help_text=(
            "Still shown before the video is played. YouTube links use their "
            "own thumbnail when this is empty."
        ),
    )

    class Meta:
        icon = "media"
        label = "Video"


class MediaGalleryBlock(blocks.StructBlock):
    """A whole set of media, for an activity that ran over several days.

    Images and videos sit in one stream so they can be interleaved in the order
    things happened, rather than forcing an author to keep them in separate
    blocks. There is no maximum: the grid reflows and the page opens each item
    full size on click.
    """

    heading = blocks.CharBlock(required=False, max_length=200)
    items = blocks.StreamBlock(
        [
            ("image", ImageBlock()),
            ("video", VideoBlock()),
        ],
        min_num=1,
    )
    caption = blocks.CharBlock(required=False, max_length=250)

    class Meta:
        icon = "image"
        label = "Gallery (images and videos)"


def collection_choices():
    """Every image collection, resolved when the form is rendered.

    A callable rather than a fixed list, so a collection created after this
    module was imported still appears in the chooser.
    """
    from wagtail.models import Collection

    return [
        (str(collection.pk), collection.name)
        for collection in Collection.objects.all().order_by("name")
    ]


class CollectionGalleryBlock(blocks.StructBlock):
    """Every image in a Wagtail collection, as one gallery.

    The way to publish forty photographs from a three-day activity: upload them
    in one go with Images -> Add multiple images into a collection named for the
    activity, then point one block at that collection. Adding a photograph later
    means uploading it to the collection; the page picks it up with no edit
    here.
    """

    heading = blocks.CharBlock(required=False, max_length=200)
    collection = blocks.ChoiceBlock(
        choices=collection_choices,
        help_text="Images uploaded into this collection are shown, newest last.",
    )
    caption = blocks.CharBlock(required=False, max_length=250)

    class Meta:
        icon = "image"
        label = "Gallery from an image collection"


class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    label = blocks.CharBlock(
        required=False,
        max_length=120,
        help_text="Text on the download link. Defaults to the document title.",
    )

    class Meta:
        icon = "doc-full"
        label = "Document"


class KeyFactsBlock(blocks.StructBlock):
    """The standing facts of a project: team, duration, funding, status.

    A labelled list rather than prose, because a reader scanning a research
    page looks for these before they read anything else.
    """

    heading = blocks.CharBlock(required=False, max_length=200, default="Project facts")
    facts = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("label", blocks.CharBlock(max_length=80)),
                ("value", blocks.CharBlock(max_length=300)),
            ]
        ),
        min_num=1,
    )

    class Meta:
        icon = "list-ul"
        label = "Key facts"


class StatsBlock(blocks.StructBlock):
    """Headline figures -- a measured result, a sample size, a percentage."""

    heading = blocks.CharBlock(required=False, max_length=200)
    stats = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("value", blocks.CharBlock(max_length=40, help_text="For example 42% or 1.8 kW.")),
                ("label", blocks.CharBlock(max_length=120)),
            ]
        ),
        min_num=2,
        max_num=4,
    )

    class Meta:
        icon = "form"
        label = "Key figures"


class StepsBlock(blocks.StructBlock):
    """Numbered stages: a method, a procedure, a build sequence."""

    heading = blocks.CharBlock(required=False, max_length=200, default="Method")
    steps = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=200)),
                ("description", blocks.TextBlock(required=False)),
            ]
        ),
        min_num=1,
    )

    class Meta:
        icon = "order"
        label = "Numbered steps"


class DataTableBlock(blocks.StructBlock):
    """Results, specifications, or test conditions."""

    heading = blocks.CharBlock(required=False, max_length=200)
    table = TableBlock()
    caption = blocks.CharBlock(required=False, max_length=250)

    class Meta:
        icon = "table"
        label = "Table"


class CalloutBlock(blocks.StructBlock):
    """A short highlighted note: a status, a caveat, a safety point."""

    label = blocks.CharBlock(required=False, max_length=60, default="Note")
    text = blocks.TextBlock()

    class Meta:
        icon = "help"
        label = "Callout"


class ReferencesBlock(blocks.StructBlock):
    """Publications and external resources, with optional links."""

    heading = blocks.CharBlock(
        required=False, max_length=200, default="Publications and references"
    )
    entries = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("citation", blocks.TextBlock()),
                ("url", blocks.URLBlock(required=False)),
            ]
        ),
        min_num=1,
    )

    class Meta:
        icon = "doc-empty"
        label = "References"


class StoryBodyBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        max_length=200,
        icon="title",
        label="Section heading",
    )
    paragraph = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul"],
        icon="pilcrow",
        label="Text",
    )
    image = ImageBlock()
    gallery = GalleryBlock()
    media_gallery = MediaGalleryBlock()
    collection_gallery = CollectionGalleryBlock()
    quote = QuoteBlock()
    video = VideoBlock()
    document = DocumentBlock()

    class Meta:
        required = False


class ResearchBodyBlock(StoryBodyBlock):
    """Everything a story can hold, plus the structures a project needs.

    Research pages carry method, results and provenance as well as narrative,
    and those read badly as paragraphs. Inheriting keeps the shared blocks in
    one place so a fix to the image or gallery block reaches both.
    """

    key_facts = KeyFactsBlock()
    stats = StatsBlock()
    steps = StepsBlock()
    table = DataTableBlock()
    callout = CalloutBlock()
    references = ReferencesBlock()

    class Meta:
        required = False

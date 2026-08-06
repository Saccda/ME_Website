"""Content blocks for story bodies.

A StreamField is what gives authors the arrangement they expect in Wagtail: a
body is a list of blocks that can be added, reordered by dragging, and removed
independently, rather than one fixed field. Each block below is deliberately
small, so a story is assembled from parts instead of formatted inside a single
rich-text box.
"""

from wagtail import blocks
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
    url = blocks.URLBlock(help_text="A YouTube, Vimeo, or Facebook video link.")
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
    quote = QuoteBlock()
    video = VideoBlock()
    document = DocumentBlock()

    class Meta:
        required = False

from galleries.annotations_parsers.gallery_annots_parsers import GalleryAnnotationsParser
from galleries.gallery import Gallery
from galleries.images_providers.gallery_images_provider import GalleryImagesProvider
from propsettings.configurable import register_as_setting
from pyrulo_qt import ClassSelector

import galleries_qt.parser_widgets


register_as_setting(Gallery, "_images_provider", setting_type=ClassSelector(GalleryImagesProvider), sort_order=0)
register_as_setting(Gallery, "_annots_parser", setting_type=ClassSelector(GalleryAnnotationsParser), sort_order=1)

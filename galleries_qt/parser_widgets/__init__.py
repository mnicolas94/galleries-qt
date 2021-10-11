from galleries.annotations_parsers.file_name_parser import FileNameSepParser
from propsettings_qt.setting_widget_retrieval import register_object_drawer

from galleries_qt.parser_widgets.file_name_parser_widget import FileNameParserWidget


register_object_drawer(FileNameSepParser, FileNameParserWidget)

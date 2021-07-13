import os
from pathlib import Path

from PySide2 import QtWidgets, QtGui, QtCore

from galleries.gallery import Gallery
from galleries.gallery_annots_parsers import FileNameSepParser
from galleries_qt.file_name_parser_widget import FileNameParserWidget
from galleries_qt.gallery_annotations_parser_view import GalleryAnnotationsParserView
from uix.qtutils import setup_widget_from_ui


class GalleryWizard(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(GalleryWizard, self).__init__(parent=parent)

        self._dirty = False
        self._parsers_widgets = [
            ('Por nombre de archivo', FileNameParserWidget(), FileNameSepParser)
        ]

        ui_file_path = os.path.join(Path(__file__).parent, 'gallery_wizard.ui')
        self._widget: QtWidgets.QWidget = setup_widget_from_ui(ui_file_path, self)

        self._name_edit: QtWidgets.QLineEdit = self._widget.name_edit
        self._name_edit.setValidator(QtGui.QRegExpValidator('[A-Za-z0-9_áéíóúÁÉÍÓÚ]*'))
        self._name_edit.textEdited.connect(self._set_dirty)

        self._path_edit: QtWidgets.QLineEdit = self._widget.path_edit
        self._path_edit.textEdited.connect(self._set_dirty)

        self._path_button: QtWidgets.QPushButton = self._widget.path_button
        self._path_button.clicked.connect(self._select_gallery_path)
        self._path_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))

        self._recursive_checkbox: QtWidgets.QCheckBox = self._widget.recursive_checkbox
        self._recursive_checkbox.stateChanged.connect(self._set_dirty())

        self._parser_combobox: QtWidgets.QComboBox = self._widget.parser_combobox
        self._parser_combobox.currentIndexChanged.connect(self._on_parser_changed)
        self._parser_container: QtWidgets.QStackedWidget = self._widget.parser_widget_container

        self._populate_parsers_combobox()

    def is_dirty(self):
        dirty = self._dirty
        parser_dirty = self._current_parser_widget().is_dirty()
        return dirty or parser_dirty

    def _current_parser_widget(self) -> GalleryAnnotationsParserView:
        return self._parser_container.currentWidget()

    def set_gallery(self, gallery_name: str, gallery: Gallery):
        self._name_edit.setText(gallery_name)
        self._path_edit.setText(gallery.directory)
        self._set_combobox_index_by_parser(gallery.annotations_parser)
        self._recursive_checkbox.setChecked(gallery.recursive)
        self._dirty = False

    def get_gallery(self) -> Gallery:
        directory = self._path_edit.text()
        parser = self._current_parser_widget().get_parser()
        recursive = self._recursive_checkbox.checkState() == QtCore.Qt.Checked
        gallery = Gallery(directory, parser, recursive=recursive)
        return gallery

    def get_name(self) -> str:
        return self._name_edit.text()

    def clear(self):
        self._name_edit.setText('')
        self._path_edit.setText('')
        self._parser_combobox.setCurrentIndex(0)
        parser = self._current_parser_widget()
        parser.clear()
        self._dirty = False

    def _set_combobox_index_by_parser(self, parser: type):
        for i, (parser_name, parser_widget, parser_class) in enumerate(self._parsers_widgets):
            if isinstance(parser, parser_class):
                self._parser_combobox.setCurrentIndex(i)
                parser_widget.populate_with_parser(parser)
                break

    def _populate_parsers_combobox(self):
        for parser_name, parser_widget, parser_class in self._parsers_widgets:
            self._parser_combobox.addItem(parser_name)
            self._parser_container.addWidget(parser_widget)

    def _on_parser_changed(self, index):
        self._parser_container.setCurrentIndex(index)
        self._set_dirty()

    def _select_gallery_path(self):
        workdir = os.getcwd()
        gallery_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            self.tr("Seleccionar ubicación de la galería"),
            workdir,
        )
        if self._is_valid_path(gallery_path):
            self._path_edit.setText(gallery_path)
            self._set_dirty()

    def _is_valid_path(self, gallery_path: str) -> bool:
        return gallery_path != ''

    def _set_dirty(self):
        self._dirty = True


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QWidget, QVBoxLayout

    app = QApplication(sys.argv)

    window = QWidget()
    window.setMinimumSize(100, 100)
    layout = QVBoxLayout()
    window.setLayout(layout)

    panel = GalleryWizard()
    layout.addWidget(panel)

    window.show()

    sys.exit(app.exec_())

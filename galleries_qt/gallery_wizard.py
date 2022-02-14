from galleries.igallery import IGallery
from mnd_qtutils.qtutils import setup_widget_from_ui
import os
from pathlib import Path
from pyrulo_qt.ui_configurable_selector import ConfigurableSelector
from PySide2 import QtWidgets, QtGui, QtCore

import galleries_qt


class GalleryWizard(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(GalleryWizard, self).__init__(parent=parent)

        self._dirty = False

        ui_file_path = os.path.join(Path(__file__).parent, 'gallery_wizard.ui')
        self._widget: QtWidgets.QWidget = setup_widget_from_ui(ui_file_path, self)

        self._name_edit: QtWidgets.QLineEdit = self._widget.name_edit
        self._name_edit.setValidator(QtGui.QRegExpValidator('[A-Za-z0-9_áéíóúÁÉÍÓÚ]*'))
        self._name_edit.textEdited.connect(self._set_dirty)

        self._gallery_container: QtWidgets.QWidget = self._widget.gallery_container
        self._gallery_selector = ConfigurableSelector(base_class=IGallery)
        self._gallery_selector.eventObjectSelected.connect(self._on_gallery_changed)
        self._gallery_container.layout().addWidget(self._gallery_selector)

    def is_dirty(self):
        dirty = self._dirty
        return dirty

    def set_gallery(self, gallery_name: str, gallery: IGallery):
        self._name_edit.setText(gallery_name)
        self._set_gallery_ui_by_gallery(gallery)
        self._dirty = False

    def get_gallery(self) -> IGallery:
        gallery_name = self._name_edit.text()
        gallery: IGallery = self._gallery_selector.current_object()
        gallery.set_name(gallery_name)
        return gallery

    def get_name(self) -> str:
        return self._name_edit.text()

    def clear(self):
        self._provider_selector.set_current_index(0)
        self._parser_selector.set_current_index(0)
        self._dirty = False

    def _set_gallery_ui_by_gallery(self, gallery: IGallery):
        gallery_class = type(gallery)
        self._gallery_selector.add_class(gallery_class)
        self._gallery_selector.set_object_for_class(gallery_class, gallery)
        self._gallery_selector.select_class(gallery_class)

    @QtCore.Slot()
    def _on_gallery_changed(self, index):
        self._set_dirty()

    def _set_dirty(self):
        self._dirty = True


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QWidget, QVBoxLayout

    app = QApplication(sys.argv)

    window = QWidget()
    window.setMinimumSize(600, 500)
    layout = QVBoxLayout()
    window.setLayout(layout)

    panel = GalleryWizard()
    layout.addWidget(panel)

    window.show()

    sys.exit(app.exec_())

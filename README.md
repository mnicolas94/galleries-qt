# Galleries-qt

Galleries-qt provides Qt widgets to create and manage images galleries through a user interface. The galleries are created with [galleries](https://github.com/mnicolas94/galleries) python package.

# Installation

`pip install galleries-qt`

# Usage

Galleries-qt provides two widgets. A galleries manager to create, update and delete galleries:

```python
from galleries_qt.galleries_manager import GalleriesManager

widget = GalleriesManager()
```

and a combobox that allows to select from all galleries you have created

```python
from galleries_qt.galleries_combobox import GalleriesCombobox

widget = GalleriesCombobox()
```


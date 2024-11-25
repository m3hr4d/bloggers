"""Custom form fields."""
from wtforms import SelectMultipleField, widgets

class MultipleCheckboxField(SelectMultipleField):
    """Custom field for multiple checkbox selection."""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

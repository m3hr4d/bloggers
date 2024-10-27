# Persian Date Picker Setup Guide

This guide explains how to implement the Persian Date Picker in a Flask project with proper form submission functionality.

## Installation

1. Add the required JavaScript and CSS files to your base template:

```html
<!-- In base.html -->
<link href="https://unpkg.com/persian-datepicker@1.2.0/dist/css/persian-datepicker.min.css" rel="stylesheet">
<script src="https://unpkg.com/persian-date@1.1.0/dist/persian-date.min.js"></script>
<script src="https://unpkg.com/persian-datepicker@1.2.0/dist/js/persian-datepicker.min.js"></script>
```

## HTML Implementation

1. Create input fields with proper IDs and names:

```html
<div class="input-group">
    <input type="text" class="form-control form-control-lg" id="start_date" name="start_date" placeholder="انتخاب تاریخ">
    <span class="input-group-text cursor-pointer" id="start_date_btn">
        <i class="bi bi-calendar"></i>
    </span>
</div>
```

## JavaScript Implementation

1. Initialize the date picker with proper options:

```javascript
$(document).ready(function() {
    const dateOptions = {
        format: 'YYYY/MM/DD',
        autoClose: true,
        initialValue: false,
        persianDigit: true,
        observer: true,
        calendar: {
            persian: {
                locale: 'fa'
            }
        },
        onSelect: function(unix) {
            const input = $(this.model.inputElement);
            const date = new persianDate(unix);
            input.val(date.format('YYYY/MM/DD'));
        }
    };

    $('#start_date').persianDatepicker(dateOptions);
    $('#end_date').persianDatepicker(dateOptions);

    // Add click handlers for calendar icons
    $('#start_date_btn').click(function() {
        $('#start_date').focus();
    });

    $('#end_date_btn').click(function() {
        $('#end_date').focus();
    });
});
```

## CSS Styling

Add these styles to make the date picker match your theme:

```css
.datepicker-plot-area {
    font-family: 'BYekan', sans-serif !important;
    background-color: #fff;
    border: none;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    border-radius: 10px;
    z-index: 9999;
}

.datepicker-plot-area .datepicker-header {
    background-color: #0069ff;
    color: white;
    border-radius: 10px 10px 0 0;
    padding: 10px;
}

.datepicker-plot-area .datepicker-header .btn-next,
.datepicker-plot-area .datepicker-header .btn-prev,
.datepicker-plot-area .datepicker-header .btn-switch {
    color: white;
    font-size: 1.2rem;
    margin: 0 5px;
}

.datepicker-plot-area .datepicker-day-view .table-days td.selected span {
    background-color: #0069ff !important;
    color: white !important;
    border-radius: 50%;
}

.datepicker-plot-area .datepicker-day-view .table-days td span {
    width: 40px;
    height: 40px;
    line-height: 40px;
    font-size: 1rem;
}

.datepicker-plot-area .datepicker-day-view .month-grid-box .header .header-row-cell {
    color: #0069ff;
    font-weight: bold;
}

.datepicker-plot-area .toolbox {
    background-color: #f8f9fa;
    border-radius: 0 0 10px 10px;
    padding: 10px;
}

.datepicker-plot-area .toolbox .btn-today {
    background-color: #0069ff;
    color: white;
    border-radius: 5px;
    padding: 5px 10px;
}
```

## Key Features

1. **No Pre-filled Values**: The date picker starts empty, allowing users to choose their own dates
2. **Persian Calendar**: Uses proper Persian/Jalali calendar with Persian digits
3. **Auto-close**: Calendar closes automatically after date selection
4. **Form Integration**: Selected dates are properly set in form fields for submission
5. **Mobile Friendly**: Works well on both desktop and mobile devices
6. **RTL Support**: Properly aligned for right-to-left text direction
7. **Custom Styling**: Matches your application's theme

## Important Notes

1. Make sure jQuery is loaded before the Persian date picker scripts
2. The input fields should be type="text" to allow proper date formatting
3. Use unique IDs for each date picker input field
4. The calendar icon click handler should focus the input field to open the calendar
5. The onSelect function is crucial for properly setting the selected date in the input field

## Troubleshooting

1. If dates aren't being submitted:
   - Check that the input field has a proper name attribute
   - Verify the onSelect function is properly setting the input value

2. If calendar isn't showing:
   - Check z-index values in CSS
   - Verify jQuery is properly loaded
   - Check for JavaScript console errors

3. If styling looks wrong:
   - Verify all CSS files are properly loaded
   - Check for CSS conflicts with your theme
   - Ensure proper font-family is set

## Form Processing

In your Flask route, you can process the dates as strings in 'YYYY/MM/DD' format:

```python
@app.route('/submit', methods=['POST'])
def submit():
    start_date = request.form.get('start_date')  # Will be in 'YYYY/MM/DD' format
    end_date = request.form.get('end_date')      # Will be in 'YYYY/MM/DD' format
```

This implementation provides a clean, user-friendly Persian date picker that properly integrates with form submission while maintaining a consistent look and feel with your application's theme.

import dateutil.parser
from reportr import app

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d %b %Y'
    return native.strftime(format) 
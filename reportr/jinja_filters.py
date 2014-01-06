import dateutil.parser
from reportr import app

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d %b %Y'
    return native.strftime(format) 

@app.template_filter('administration_route_convert')
def _jinja2_filter_administration_route_convert(routecode, fmt=None):
    routes = {}
    routes = {'001': 'Auricular (otic)', '002': 'Buccal', '003': 'Cutaneous', '004': 'Dental', '005': 'Endocervical', '006': 'Endosinusial', '007': 'Endotracheal', '008': 'Epidural', '009': 'Extra-amniotic', '010': 'Hemodialysis', '011': 'Intra corpus cavernosum', '012': 'Intra-amniotic', '013': 'Intra-arterial', '014': 'Intra-articular', '015': 'Intra-uterine', '016': 'Intracardiac', '017': 'Intracavernous', '018': 'Intracerebral', '019': 'Intracervical', '020': 'Intracisternal', '021': 'Intracorneal', '022': 'Intracoronary', '023': 'Intradermal', '024': 'Intradiscal (intraspinal)', '025': 'Intrahepatic', '026': 'Intralesional', '027': 'Intralymphatic', '028': 'Intramedullar (bone marrow)', '029': 'Intrameningeal', '030': 'Intramuscular', '031': 'Intraocular', '032': 'Intrapericardial', '033': 'Intraperitoneal', '034': 'Intrapleural', '035': 'Intrasynovial', '036': 'Intratumor', '037': 'Intrathecal', '038': 'Intrathoracic', '039': 'Intratracheal', '040': 'Intravenous bolus', '041': 'Intravenous drip', '042': 'Intravenous (not otherwise specified)', '043': 'Intravesical', '044': 'Iontophoresis', '045': 'Nasal', '046': 'Occlusive dressing technique', '047': 'Ophthalmic', '048': 'Oral', '049': 'Oropharingeal', '050': 'Other', '051': 'Parenteral', '052': 'Periarticular', '053': 'Perineural', '054': 'Rectal', '055': 'Respiratory (inhalation)', '056': 'Retrobulbar', '057': 'Sunconjunctival', '058': 'Subcutaneous', '059': 'Subdermal', '060': 'Sublingual', '061': 'Topical', '062': 'Transdermal', '063': 'Transmammary', '064': 'Transplacental', '065': 'Unknown', '066': 'Urethral', '067': 'Vaginal'}
    for code, term in routes.iteritems():
        if code == routecode:
            return term

@app.template_filter('time_unit_convert')
def _jinja2_filter_time_unit_convert(time_unit, fmt=None):
    time_units = {}
    time_units = {'800': 'Decade', '801': 'Year', '802': 'Month', '803': 'Week', '804': 'Day', '805': 'Hour'}
    for unit, term in time_units.iteritems():
        if unit == time_unit:
            return term
            

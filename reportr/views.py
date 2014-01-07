from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from urlparse import parse_qs

from pyelasticsearch import ElasticSearch

from reportr import app
from jinja_filters import *


# We'll initalize the ElasticSearch engine with the URL from the settings file
es = ElasticSearch(app.config['ES_URL'])

#
# This controls the view for the homepage, which shows the most recent additions
#
@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def show_all_reports(page):
    # Pagination Control
    search_from = page * app.config['RESULTS_PER_PAGE'] - app.config['RESULTS_PER_PAGE'] + 1
    if page == 1:
        first_page = True
    else:
        first_page = False
    starting_number = search_from
    ending_number = search_from + app.config['RESULTS_PER_PAGE'] - 1
    next_page = page + 1
    previous_page = page - 1
    
    # Construct a basic query that captures all reports and organizes the start number and returned size
    reports = es.search('sender.senderorganization:"FDA-Public Use"', index=app.config['ES_INDEX'], es_from=search_from, size=app.config['RESULTS_PER_PAGE'])
    
    # Return the template
    return render_template('show_all_reports.html', reports=reports["hits"]["hits"], first_page=first_page, starting_number=starting_number, ending_number=ending_number, count=reports["hits"]["total"], per_page=app.config['RESULTS_PER_PAGE'], next_page=next_page, previous_page=previous_page)

#
# This controls the view for search pages. The search params are delivered via query strings
#
@app.route('/search')
def search_reports():
    # Query String Parsing
    search_page = True
    search = []
    page = 1
    for param, term in parse_qs(request.query_string).iteritems():
        if param == "medicinalproduct":
            search.append("patient.drug.medicinalproduct:%s" % str(term[0]))
        if param == "reaction":
            search.append("patient.reaction.reactionmeddrapt:%s" % str(term[0]))
        if param == "page":
            page = int(term[0])
    query = ""
    for phrase in search:
        query+="%s AND " % str(phrase)
    query = query[:-5]
    
    # Pagination Control
    search_from = page * app.config['RESULTS_PER_PAGE'] - app.config['RESULTS_PER_PAGE'] + 1
    if page == 1:
        first_page = True
    else:
        first_page = False
    starting_number = search_from
    ending_number = search_from + app.config['RESULTS_PER_PAGE'] - 1
    next_page = page + 1
    previous_page = page - 1
    
    # Construct a basic query that captures all reports and organizes the start number and returned size
    reports = es.search('sender.senderorganization:"FDA-Public Use"', index=app.config['ES_INDEX'], es_from=search_from, size=app.config['RESULTS_PER_PAGE'])
    
    # Return the template
    return render_template('show_all_reports.html', reports=reports["hits"]["hits"], first_page=first_page, starting_number=starting_number, ending_number=ending_number, count=reports["hits"]["total"], per_page=app.config['RESULTS_PER_PAGE'], next_page=next_page, previous_page=previous_page)

#
# This controls the view for a single report
#
@app.route('/safetyreport/<safetyreportid>')
def show_report(safetyreportid):
    # Pull a report by safetyreportid
    report = es.search('safetyreportid:%s' % safetyreportid, index=app.config['ES_INDEX'])
    
    # Only return the top ranked report
    if report["hits"]["hits"][0]["_score"] > 1:
        return render_template('show_report.html', report=report["hits"]["hits"][0]["_source"])
    else:
        return "Nothing Found"
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from urlparse import parse_qs

from pyelasticsearch import ElasticSearch

from reportr import app
from jinja_filters import *

es = ElasticSearch(app.config['ES_URL'])

@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def show_all_reports(page):
    search_from = page * app.config['RESULTS_PER_PAGE'] - app.config['RESULTS_PER_PAGE'] + 1
    if page == 1:
        first_page = True
    else:
        first_page = False
    starting_number = search_from
    ending_number = search_from + app.config['RESULTS_PER_PAGE'] - 1
    next_page = page + 1
    previous_page = page - 1
    reports = es.search('sender.senderorganization:"FDA-Public Use"', index=app.config['ES_INDEX'], es_from=search_from, size=app.config['RESULTS_PER_PAGE'])
    return render_template('show_all_reports.html', reports=reports["hits"]["hits"], first_page=first_page, starting_number=starting_number, ending_number=ending_number, count=reports["hits"]["total"], per_page=app.config['RESULTS_PER_PAGE'], next_page=next_page, previous_page=previous_page)

@app.route('/', defaults={'page': 1})
@app.route('/search/')
def search_reports():
    search = ""
    #return str(parse_qs(request.query_string))
    for param, term in parse_qs(request.query_string).iteritems():
        if param == "medicinalproduct":
            search+="patient.drug.medicinalproduct:%s" % str(term[0])
   # search_from = page * app.config['RESULTS_PER_PAGE'] - app.config['RESULTS_PER_PAGE'] + 1
  #  starting_number = search_from
   # ending_number = search_from + app.config['RESULTS_PER_PAGE'] - 1
   # next_page = page + 1
  #  previous_page = page - 1
    reports = es.search(search, index=app.config['ES_INDEX'])
    return render_template('show_all_reports.html', reports=reports["hits"]["hits"])


@app.route('/safetyreport/<safetyreportid>')
def show_report(safetyreportid):
    report = es.search('safetyreportid:%s' % safetyreportid, index=app.config['ES_INDEX'])
    if report["hits"]["hits"][0]["_score"] > 1:
        return render_template('show_report.html', report=report["hits"]["hits"][0]["_source"])
    else:
        return "nope"
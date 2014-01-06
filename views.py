from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from reportr import app
from pyelasticsearch import ElasticSearch
from jinja_filters import _jinja2_filter_datetime

es = ElasticSearch(app.config['ES_URL'])

@app.route('/')
def show_all_reports():
  reports = es.search('sender.senderorganization:"FDA-Public Use"', index=app.config['ES_INDEX'])
  return render_template('show_all_reports.html', reports=reports["hits"]["hits"])

@app.route('/safetyreport/<safetyreportid>')
def show_report(safetyreportid):
	report = es.search('safetyreportid:%s' % safetyreportid, index=app.config['ES_INDEX'])
	if report["hits"]["hits"][0]["_score"] > 1:
		return render_template('show_report.html', report=report["hits"]["hits"][0]["_source"])
	else:
		return "nope"
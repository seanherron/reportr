from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from pyelasticsearch import ElasticSearch

DEBUG = True

es = ElasticSearch('http://ec2-54-204-7-238.compute-1.amazonaws.com:9000')


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_all_reports():
  reports = es.search('sender.senderorganization:"FDA-Public Use"', index='test')
  return render_template('show_all_reports.html', reports=reports["hits"]["hits"])

@app.route('/safetyreport/<safetyreportid>')
def show_report(safetyreportid):
	report = es.search('safetyreportid:%s' % safetyreportid, index='test')
	if report["hits"]["hits"][0]["_score"] > 1:
		return render_template('show_report.html', report=report["hits"]["hits"][0]["_source"])
	else:
		return "nope"

if __name__ == '__main__':
  app.run()

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, flash, render_template, request
from translator import translate


app = Flask(__name__)
app.debug = True
app.secret_key = 'uhd8*%ˆsa7gn29dhl10wjs;-'


@app.route("/")
def hello():
    page = request.args.get('page')

    print page

    confluence_output = None
    if page:
        try:
            confluence_output = translate(page)
        except Exception as e:
            import traceback
            print traceback.print_exc(file=sys.stdout)
            flash('An Exception was found: %s' % e)
        else:
            if not confluence_output:
                flash('The page %s was not found.' % page)

    return render_template("index.html", page=page,
                           confluence_output=confluence_output)


if __name__ == "__main__":
    app.run()

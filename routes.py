from dash import Input, Output, State
from base.login import view as login
from pages.pqr_dashboard import view  as pqr_dashboard
from pages.pqr_exploration import view as pqr_exploration
from pages.pqr_reports import view as pqr_reports
from app import app
import time

import app as server

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('url','search')])
def display_page(pathname, search): 

    try:

        t1 = time.time()

        redirect = {'/': pqr_dashboard.layout,
                    '/pqr_dashboard': pqr_dashboard.layout,
                    '/pqr_exploration': pqr_exploration.layout,
                    '/pqr_reports': pqr_reports.layout,
                    # '/profile': profile.layout,
                    # '/messages': messages.layout,
                    # 'NoAccess': NoAccess.layout,
                    }

        return redirect[pathname]
    except Exception as e:
        print(f'Catched the following exception while redirecting: {e}')






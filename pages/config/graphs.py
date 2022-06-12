from dash import html, dcc, Input, Output, State, ALL, MATCH
import dash_mantine_components as dmc
from dash import html, dcc
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

def DateFilters(id):
  output = [html.Div(className="col-4",children=[
                  html.Label("Choose a period", className="text-dark"),
                  dcc.Dropdown(
                  id={'type':"timeframe_dropdown","index":id},
                  multi=False,
                  options=[
                      {'label': 'Fixed', 'value': 'fixed'},
                      {'label': 'Today', 'value': str([datetime.today().strftime('%Y-%m-%d')]*2)},
                      {'label': 'Yesterday', 'value': str([(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')]*2)},
                      {'label': 'This week (from monday)', 'value': str([(date.today() - timedelta(days=date.today().weekday())).strftime('%Y-%m-%d'),(date.today() + timedelta(days=(6 - date.today().weekday()))).strftime('%Y-%m-%d')])},
                      {'label': 'Last week (from monday)', 'value': str([(date.today() - timedelta(days=date.today().weekday(),weeks=1)).strftime('%Y-%m-%d'),((date.today() - timedelta(days=date.today().weekday(),weeks=1)) + timedelta(days=7)).strftime('%Y-%m-%d')])},
                      {'label': 'This month', 'value': str([format(datetime.now() - relativedelta(days=datetime.now().day-1), '%Y-%m-%d'),format(datetime.now() + relativedelta(months=1) - relativedelta(days=datetime.now().day), '%Y-%m-%d')])},
                      {'label': 'Last month', 'value': str([format(datetime.now() - relativedelta(months=1, days=datetime.now().day-1), '%Y-%m-%d'),format(datetime.now() - relativedelta(days=datetime.now().day), '%Y-%m-%d')])},
                      {'label': 'This year', 'value': str([(date.today().replace(month=1).replace(day=1)).strftime('%Y-%m-%d'),(date.today().replace(month=12).replace(day=calendar.monthrange(date.today().year, 12)[1])).strftime('%Y-%m-%d')])},
                      {'label': 'Last year', 'value': str([(date.today().replace(year=date.today().year - 1).replace(month=1).replace(day=1)).strftime('%Y-%m-%d'),date.today().replace(year=date.today().year - 1).replace(month=12).replace(day=calendar.monthrange(date.today().year, 12)[1]).strftime('%Y-%m-%d')])}
                  ],
                  placeholder='Predefinido',
                  value='fixed',
                  clearable=False,
                  className=""
              )]),
              html.Div(className="col-8 p-0",children=[
                  html.Label("Date Picker", className="text-dark"),
                  dmc.DateRangePicker(
                              id={'type':"date-range-picker","index":id},
                              value=[datetime.now().date(), datetime.now().date()],
                              amountOfMonths=2,
                              dropdownType="modal",
                              zIndex=1000,
                              shadow='sm',
                              modalZIndex=1000,
                              allowSingleDateInRange = True,
                              class_name=""

                  )
              ])
    ]

  return output
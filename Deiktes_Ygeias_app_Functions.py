#Importing Libraries
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_dynamic_filters import DynamicFilters

##Function for 2 categories Pie Charts:
def two_cat_pie (val,val2):
    fig_two_cat_pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])


    fig_two_cat_pie.add_trace(go.Pie(labels=['', ''],
                         values=[val, 100 - val],
                         hole=0.85,
                         textinfo='none',
                         hoverinfo='none',
                         marker_colors=['rgb(113,209,145)', 'rgb(240,240,240)'],
                         direction='clockwise',
                         ), row=1, col=1)

    fig_two_cat_pie.add_trace(go.Pie(labels=['', ''],
                         values=[val2, 100 - val2],
                         hole=0.85,
                         textinfo='none',
                         hoverinfo="none",
                         marker_colors=['rgba(255,43,43,0.8)', 'rgb(240,240,240)'],
                         direction='clockwise',
                         ), row=1, col=2)
    fig_two_cat_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')

    return fig_two_cat_pie
#######################################################################################################################################
#######################################################################################################################################

##Function for 3 categories Pie Charts:
def three_cat_pie (val,val2,val3):
    fig_three_cat_pie = make_subplots(rows=1, cols=3,specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]])

    fig_three_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val,100-val],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=1)

    fig_three_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val2,100-val2],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255, 127, 14,0.7)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=2)

    fig_three_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val3,100-val3],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255,43,43,0.8)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=3)
    fig_three_cat_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')

    return fig_three_cat_pie
#######################################################################################################################################
#######################################################################################################################################

##Function for 3 categories Pie Charts: **With two red Pies**
def three_cat_pie_v2 (val,val2,val3):
    fig_three_cat_pie_v2 = make_subplots(rows=1, cols=3,specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]])

    fig_three_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val,100-val],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=1)

    fig_three_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val2,100-val2],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255,43,43,0.8)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=2)

    fig_three_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val3,100-val3],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255,43,43,0.8)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=3)
    fig_three_cat_pie_v2.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')

    return fig_three_cat_pie_v2
#######################################################################################################################################
#######################################################################################################################################

##Function for 4 categories Pie Charts:
def four_cat_pie (val,val2,val3,val4):
    fig_four_cat_pie = make_subplots(rows=1, cols=4,specs=[[{"type": "pie"}, {"type": "pie"},{"type": "pie"},{"type": "pie"}]])

    fig_four_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val,100-val],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=1)

    fig_four_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val2,100-val2],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255, 127, 14,0.7)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=2)

    fig_four_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val3,100-val3],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255,43,43,0.6)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=3)
    fig_four_cat_pie.add_trace(go.Pie(labels=['',''],
                      values=[val4,100-val4],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255,43,43,0.8)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=4)
    fig_four_cat_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')

    return fig_four_cat_pie

#######################################################################################################################################
#######################################################################################################################################

##Function for 4 categories Pie Charts: **With 2 Green pies**
def four_cat_pie_v2 (val,val2,val3,val4):
    fig_four_cat_pie_v2 = make_subplots(rows=1, cols=4,specs=[[{"type": "pie"}, {"type": "pie"},{"type": "pie"},{"type": "pie"}]])

    fig_four_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val,100-val],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=1)

    fig_four_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val2,100-val2],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(113,209,145,0.6)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=2)

    fig_four_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val3,100-val3],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255, 127, 14,0.7)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=3)
    fig_four_cat_pie_v2.add_trace(go.Pie(labels=['',''],
                      values=[val4,100-val4],
                      hole=0.85,
                      textinfo='none',
                      hoverinfo="none",
                      marker_colors=['rgba(255,43,43,0.8)','rgb(240,240,240)'],
                      direction='clockwise',
                      ),row=1, col=4)
    fig_four_cat_pie_v2.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')

    return fig_four_cat_pie_v2

#######################################################################################################################################
#######################################################################################################################################

##Function for Histogramm with KPI's:
def kpis_hist(value):

    # Initialize figure with subplots
    fig_kpis_hist = make_subplots(
      rows=2, cols=5,
      #column_widths=[0.6, 0.4],
      row_heights=[0.05, 0.95],
      specs=[[{"type": "indicator"}, {"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"}],
           [{"type": "Histogram","colspan":5},None,None,None,None]])
    #Set the color:
    #color="#29648a"
    color="#379683"

    #Set the KPIS and the Hist:
    fig_kpis_hist.add_trace(go.Indicator(
                  value=value.count(),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Εργαζόμενοι","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=1)
    fig_kpis_hist.add_trace(go.Indicator(
                  value=round(value.mean(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Μέσος όρος","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=2)
    fig_kpis_hist.add_trace(go.Indicator(
                  value=round(value.min(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Min","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=3)
    fig_kpis_hist.add_trace(go.Indicator(
                  value=round(value.quantile(0.75),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"75%","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=4)
    fig_kpis_hist.add_trace(go.Indicator(
                  value=round(value.max(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Max","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=5)
    fig_kpis_hist.add_trace(go.Histogram(
                  x=value,
                  #xbins=go.XBins(size=1),
                  autobinx=True,
                  opacity=0.5,
                  #nbinsx=4,
                  #xaxis="x1",
                  #yaxis="y1",
                  marker=go.Marker(color=color,line=dict(color="rgb(2, 99, 99)", width=1))
                  #name="Test"
                  #histnorm="density"
                  ),row=2,col=1)
    name=value.name
    fig_kpis_hist.update_xaxes(title_text=name, row=2, col=1)
    fig_kpis_hist.update_yaxes(title_text="", row=2, col=1)
    fig_kpis_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig_kpis_hist.update_layout(hoverlabel_font_size=16)
    

    return fig_kpis_hist
#######################################################################################################################################
#######################################################################################################################################

##Function for Histogramm and BoxPlot with KPI's:
def kpis_extra_hist(value):

    # Initialize figure with subplots
    fig_extra_kpis_hist = make_subplots(
      rows=2, cols=7,
      #column_widths=[0.6, 0.4],
      row_heights=[0.05, 0.95],
      specs=[[{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"}],
           [{"type": "Histogram","colspan":6},None,None,None,None,None,None,]])
    #Set the color:
    color="#379683"
    
    #Set the KPIS and the Hist:
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=value.count(),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Εργαζόμενοι","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=1)
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=round(value.mean(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Μέσος όρος","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=2)
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=round(value.min(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Min","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=3)
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=round(value.quantile(0.25),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"25%","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=4)
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=round(value.median(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Διάμεσος","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=5)
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=round(value.quantile(0.75),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"75%","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=6)
    fig_extra_kpis_hist.add_trace(go.Indicator(
                  value=round(value.max(),1),
                  align="left",
                  number={"font": {"size": 40,"color":color}},
                  title={"text":"Max","font":{"size":20,"color":"gray"},"align":"left"}
                  ),row=1,col=7)
    fig_extra_kpis_hist.add_trace(go.Histogram(
                  x=value,
                  #xbins=go.XBins(size=1),
                  autobinx=True,
                  opacity=0.5,
                  #nbinsx=4,
                  #xaxis="x1",
                  #yaxis="y1",
                  marker=go.Marker(color=color,line=dict(color="#123c69", width=1))
                  #name="Test"
                  #histnorm="density"
                  ),row=2,col=1)
    name=value.name
    fig_extra_kpis_hist.update_xaxes(title_text=name, row=2, col=1)
    fig_extra_kpis_hist.update_yaxes(title_text="", row=2, col=1)
    fig_extra_kpis_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig_extra_kpis_hist.update_layout(showlegend=False)
    fig_extra_kpis_hist.update_layout(hoverlabel_font_size=16)

    return fig_extra_kpis_hist
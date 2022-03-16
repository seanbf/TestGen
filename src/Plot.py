import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st


def Plot_Profile(profile, Profile_Voltage, Project_Speeds, Project_Torques, Speed_Limit_Forward, Speed_Limit_Reverse):  
        
        # IDEA 1y left, 2y right
        test_plot_scatter = go.Figure()

        test_plot_scatter.add_trace	(go.Scattergl (  
                                x       		= Project_Speeds,
                                y       		= Project_Torques,
                                name 			= "Avaiable Envelope",
                                mode            = 'lines',
                                        )
                        )

        test_plot_scatter.add_trace	(go.Scattergl (  
                                    x       		= profile.speedDemand,
                                    y       		= profile.torqueDemand,
                                    name 			= "Test Points",
                                    mode            = 'markers',
                                            )
                            )

        test_plot_scatter.update_layout(   
                                    title       = "Test Points: "  + str(Profile_Voltage) + "V, " + str(min(profile.speedDemand)) + "rpm to " + str(max(profile.speedDemand)) + " rpm, ",
                                    xaxis_title = "Speed [rpm]",
                                    yaxis_title = "Torque Demanded [Nm]"
                                    )
      
        # TIMELINe
        test_plot_time = go.Figure()

        test_plot_time.add_trace(go.Scattergl (  
                                    y       		= profile.speedDemand,
                                    name 		= "Speed (rpm)",
                                    yaxis='y1'
                                    
                                                    )
                            )
        test_plot_time.add_trace(go.Scattergl (  
                                    y       		= Speed_Limit_Forward,
                                    name 		= "Speed Limit Forward (rpm)",
                                    yaxis='y1'
                                    
                                                    )
                            )
        test_plot_time.add_trace(go.Scattergl (  
                                    y       		= Speed_Limit_Reverse,
                                    name 		= "Speed Limit Reverse (rpm)",
                                    yaxis='y1'
                                    
                                                    )
                            )


        test_plot_time.add_trace(go.Scattergl (  
                                y       		= profile.torqueDemand,
                                name 			= "Torque (Nm)",
                                yaxis='y3'

                                        )
                        )    

        test_plot_time.add_trace(go.Scattergl (  
                            y       		= profile.powerMech,
                            name 			= "Mech Power (W)",
                            yaxis='y4'


                                    )
                    )                      

        test_plot_time.update_traces(mode="markers+lines")

        test_plot_time.update_layout(
            xaxis=dict(
                domain=[0, 0.8]
            ),
            yaxis=dict(
                title="Speed [rpm]",
            ),
            yaxis3=dict(
                title="Torque [Nm]",
                anchor="x",
                overlaying="y",
                side="right"
            ),
            yaxis4=dict(
                title="Mech Power [W]",
                anchor="free",
                overlaying="y",
                side="right",
                position=0.9
            ),
                title       = "Test Input Timeline: "  + str(Profile_Voltage) + "V, " + str(min(profile.speedDemand)) + "rpm to " + str(max(profile.speedDemand)) + " rpm, " ,
                xaxis_title = "Test Point",
                hovermode="x unified",
                legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.0,
                xanchor="right",
                x=1)
                
        )

        return test_plot_scatter, test_plot_time
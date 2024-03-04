import plotly.graph_objects as go

class Plotter:
    def plot_data_pie(self, data, key, user, period):
        names = []
        full_names = []
        playcounts = []
        colors = ['#da7fe0', '#e0b3da', '#e0dada', '#b3dae0']

        for item in data[f"top{key}s"][key][:10]:
            full_name = item["name"]
            full_names.append(full_name)
            if len(full_name) > 25:
                name = full_name[:22] + '...'
            else:
                name = full_name
            names.append(name)
            playcounts.append(int(item["playcount"]))

        pie = go.Pie(
            labels=names, 
            values=playcounts, 
            name=", ".join(names), 
            hole=.3, 
            textinfo='label', 
            textposition='inside', 
            insidetextorientation='radial', 
            textfont=dict(size=18),
            marker=dict(
                colors=colors,
                line=dict(color='#000000', width=2)
            ),
            hoverinfo='label+percent',
            hovertext=full_names,
            hoverlabel=dict(
                bgcolor='black',
                font=dict(color='white', size=16)
            )
        )
        layout = go.Layout(
            yaxis=dict(title='Playcount', automargin=True), 
            autosize=True, 
            height=600, 

            xaxis=dict(tickangle=-45, automargin=True)
        )   
            
        fig = go.Figure(data=[pie], layout=layout)

        return fig.to_json()


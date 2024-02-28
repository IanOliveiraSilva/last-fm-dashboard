import plotly.graph_objects as go
import textwrap
import networkx as nx

class Plotter:
    def __init__(self, data, key):
        self.data = data
        self.key = key

    def plot_data(data, key, user, period):
        names = []
        playcounts = []

        for item in data[f"top{key}s"][key][:15]:
            names.append(item["name"])
            playcounts.append(int(item["playcount"]))

        bar = go.Bar(
            x=names, 
            y=playcounts, 
            marker_color='rgb(82,41,177)',
            text=playcounts,
            textposition='outside',
            hovertemplate="<b>%{x}</b><br><br>%{y} plays",
            marker=dict(
                line=dict(color='rgb(0,0,0)', width=1.5),  
            ),
            opacity=0.7,
        )

        layout = go.Layout(
            title=f"Top {key} from {user}({period})",
            yaxis=dict(title='Playcount', automargin=True), 
            autosize=True, 
            height=600, 
            xaxis=dict(tickangle=-45, automargin=True)
        )

        fig = go.Figure(data=[bar], layout=layout)

        return fig.to_json()

    def plot_data_pie(data, key, user, period):
        names = []
        full_names = []
        playcounts = []
        colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

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
            title=f"Top {key} from {user}({period})",
            title_x=0.5,
            title_xanchor="center",
            yaxis=dict(title='Playcount', automargin=True), 
            autosize=True, 
            height=600, 
            xaxis=dict(tickangle=-45, automargin=True)
        )   
            
        fig = go.Figure(data=[pie], layout=layout)

        return fig.to_json()

    def plot_data_tree(data):
        labels = []
        parents = []
        artist_count = 0
        colors = ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF', '#BDB2FF', '#FFC6FF'] 

        color_dict = {}

        for track in data["recenttracks"]["track"]:
            artist = track["artist"]["#text"]
            album = " " + track["album"]["#text"]
            track_name = "" + track["name"]

            if artist not in labels:
                if artist_count >= 5:
                    break
                labels.append(artist)
                parents.append("")
                color_dict[artist] = colors[artist_count]
                artist_count += 1

            if album not in labels and artist in labels:
                labels.append(album)
                parents.append(artist)

            if album in labels:
                labels.append(track_name)
                parents.append(album)

        marker_colors = [color_dict.get(label, '#FFFFFF') for label in labels]

        fig = go.Treemap(
            labels=labels,
            parents=parents,
            textfont=dict(size=23, color='black'),
            marker=dict(
                colors=marker_colors,
                line=dict(width=1.5, color='black')
            ),
            tiling=dict(
                pad=5
            )
        )

        layout = go.Layout(
        autosize=True, 
        height=600
        )   

        fig = go.Figure(data=[fig], layout=layout)

        return fig.to_json()
    
    def plot_data_sunburst(data):
        labels = []
        parents = []
        artist_count = 0
        colors = ['#3b234a', '#523961', '#baafc4', '#c3bbc9', '#dcd6f7']
        color_dict = {}

        for track in data["recenttracks"]["track"]:
            artist = textwrap.fill(track["artist"]["#text"], 20)
            album = " " + textwrap.fill(track["album"]["#text"], 20)
            track_name = "" + textwrap.fill(track["name"], 20)

            if artist not in labels and artist_count < 5:
                labels.append(artist)
                parents.append("")
                color_dict[artist] = colors[artist_count]
                artist_count += 1

            if album not in labels and artist in labels:
                labels.append(album)
                parents.append(artist)
                color_dict[album] = color_dict[artist]

            if album in labels:
                labels.append(track_name)
                parents.append(album)
                color_dict[track_name] = color_dict[artist]

        marker_colors = [color_dict[label] for label in labels]

        fig = go.Sunburst(
            labels=labels,
            parents=parents,
            textfont=dict(size=14, color='white'),
            marker=dict(
                colors=marker_colors,
                line=dict(width=2.5, color='black')
            ),
            leaf=dict(opacity=0.9),
            branchvalues='total',
            hoverinfo='label+percent parent',
            maxdepth=2 
        )

        layout = go.Layout(
        autosize=True, 
        height=600
        ) 

        fig = go.Figure(data=[fig], layout=layout)

        return fig.to_json()
    
    def plot_network_graph(data):
        G = nx.Graph()
        node_colors = []

        for track in data['recenttracks']['track']:
            artist_name = track['artist']['#text']
            album_name = track['album']['#text']
            track_name = track['name']

            if artist_name not in G:
                G.add_node(artist_name, type='artista')
                node_colors.append('rgba(255, 0, 0, 0.8)') 

            if album_name not in G:
                G.add_node(album_name, type='album')
                G.add_edge(artist_name, album_name)
                node_colors.append('rgba(0, 255, 0, 0.8)') 

            if track_name not in G:
                G.add_node(track_name, type='musica')
                G.add_edge(album_name, track_name)
                node_colors.append('rgba(0, 0, 255, 0.8)') 

        pos = nx.spring_layout(G, seed=42)

        edge_trace = go.Scatter(
            x=[], y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[], y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=node_colors,
                size=10,
                line=dict(color='black', width=2)))

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([f'{node} ({G.nodes[node]["type"]})'])

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Network Graph of Recent Tracks',
                            titlefont=dict(size=16),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        

        return fig.to_json()

    def plot_data_stacked_bar(data):
        artists = []
        albums = []
        tracks = []

        for track in data["recenttracks"]["track"]:
            artist = track["artist"]["#text"]
            album = track["album"]["#text"]
            track_name = track["name"]

            artists.append(artist)
            albums.append(album)
            tracks.append(track_name)

        fig = go.Figure(data=[
            go.Bar(name='Artists', x=list(set(artists)), y=[artists.count(artist) for artist in set(artists)]),
            go.Bar(name='Albums', x=list(set(albums)), y=[albums.count(album) for album in set(albums)]),
            go.Bar(name='Tracks', x=list(set(tracks)), y=[tracks.count(track) for track in set(tracks)])
        ])

        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, title_text='Music Data')
        return fig.to_json()
    
    
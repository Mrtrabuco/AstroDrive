import pandas as pd
import plotly.express as px

class Maps:

    def generar_mapa_ventas(queryset):
        if queryset:
            df = pd.DataFrame.from_records(queryset)
            df['state'] = df['state'].str.upper()
        else:
            df = pd.DataFrame([{'state': 'NONE', 'ventas': 0}])

        fig = px.choropleth(
            df,
            title='Ventas por Estado',
            locations='state',
            locationmode="USA-states",
            color='ventas',
            scope="usa",
            color_continuous_scale="Viridis",
            width=900,
            height=600
        )
        return fig.to_html(full_html=False)
    
    def generar_grafico_ventas(queryset):
        if queryset:
            df = pd.DataFrame.from_records(queryset)
            df['year'] = df['year'].astype(str)
        else:
            df = pd.DataFrame([{'year': 'NONE', 'ventas': 0}])
        fig = px.bar(
            df,
            x='year',
            y='ventas',
            title='Ventas por Año',
            labels={'year': 'Año', 'ventas': 'Ventas'},
            text='ventas',
            width=900,
            height=600
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis=dict(dtick=1))
        return fig.to_html(full_html=False)
    
    def generar_grafico_marcas(queryset, top_n=10):
        if queryset:
            df = pd.DataFrame.from_records(queryset)
        else:
            df = pd.DataFrame([{'make': 'NONE', 'ventas': 0}])
        fig = px.bar(
            df,
            x='make',
            y='ventas',
            title=f'Top {top_n} Marcas Más Vendidas',
            text='ventas',
            width=900,
            height=600
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)
        return fig.to_html(full_html=False)
    
    def generar_grafico_condicion_vs_precio(queryset):
        if queryset:
            df = pd.DataFrame.from_records(queryset)
            df['condition'] = df['condition'].astype(str)
        else:
            df = pd.DataFrame([{'condition': 'NONE', 'sellingprice': 0}])

        fig = px.box(
            df,
            x='condition',
            y='sellingprice',
            title='Distribución de Precio por Condición del Vehículo',
            labels={'condition': 'Condición', 'sellingprice': 'Precio de Venta'},
            width=900,
            height=600
        )
        fig.update_layout(xaxis_title="Condición", yaxis_title="Precio de Venta")
        return fig.to_html(full_html=False)

    def generar_grafico_modelos(queryset, top_n=10):
        if queryset:
            df = pd.DataFrame.from_records(queryset)
            df = df.dropna(subset=['model'])
            modelo_counts = df['model'].value_counts().head(top_n).reset_index()
            modelo_counts.columns = ['Modelo', 'Ventas']
        else:
            df = pd.DataFrame([{'model': 'NONE', 'ventas': 0}])
            modelo_counts = pd.DataFrame([{'Modelo': 'NONE', 'Ventas': 0}])

        fig = px.bar(
            modelo_counts,
            x='Modelo',
            y='Ventas',
            title=f'Top {top_n} Modelos Más Vendidos',
            text='Ventas',
            width=900,
            height=600
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)
        return fig.to_html(full_html=False)
#block one imports
import pandas as pd
import plotly.express as px

#block two leitura de dados
df = pd.read_csv("USD_BRL_hist.csv")
df["Data"] = pd.to_datetime(df["Data"], format="%d.%m.%Y")
df = df.sort_values("Data").reset_index(drop=True)


df["Ano"] = df["Data"].dt.year
df["Mes"] = df["Data"].dt.month
df["Trimestre"] = "T" + df["Data"].dt.quarter.astype(str)

#block tree grafico 1 line
fig_linha = px.line(
    df,
    x="Data",
    y="USD_BRL",
    title="Histórico Diário da Cotação USD/BRL (2010–2019)",
    labels={"Data": "Período", "USD_BRL": "Taxa de Câmbio (R$)"},
)

fig_linha.update_traces(line_color="#1565C0", line_width=1.5)

fig_linha.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(buttons=[
        dict(count=1, label="1a", step="year", stepmode="backward"),
        dict(count=3, label="3a", step="year", stepmode="backward"),
        dict(step="all", label="Tudo")
    ])
)

fig_linha.update_layout(
    plot_bgcolor="white",
    yaxis=dict(gridcolor="#e0e0e0", title="R$ por 1 USD"),
    xaxis=dict(gridcolor="#e0e0e0"),
)

fig_linha.show()

#block four grafico 2 barra
df_barras = df.groupby("Ano")["USD_BRL"].mean().reset_index()
df_barras["USD_BRL"] = df_barras["USD_BRL"].round(2)

fig_barras = px.bar(
    df_barras,
    x="Ano",
    y="USD_BRL",
    title="Cotação Média Anual USD/BRL (2010–2019)",
    labels={"Ano": "Ano", "USD_BRL": "Cotação Média (R$)"},
    color="USD_BRL",
    color_continuous_scale="Blues",
    text="USD_BRL",
)

fig_barras.update_traces(texttemplate="R$ %{text:.2f}", textposition="outside")
fig_barras.update_xaxes(type="category")
fig_barras.update_layout(plot_bgcolor="white", yaxis=dict(gridcolor="#e0e0e0"))

fig_barras.show()

#block five grafico 3 treemap
df_hierarquico = df.groupby(["Ano", "Trimestre"])["USD_BRL"].mean().reset_index()
df_hierarquico["USD_BRL"] = df_hierarquico["USD_BRL"].round(2)

fig_treemap = px.treemap(
    df_hierarquico,
    path=["Ano", "Trimestre"],
    values="USD_BRL",
    title="Cotação Média USD/BRL por Ano e Trimestre",
    color="USD_BRL",
    color_continuous_scale="RdBu_r",
    hover_data={"USD_BRL": ":.2f"},
)

fig_treemap.update_traces(textinfo="label+value")  
fig_treemap.update_layout(margin=dict(t=50, l=10, r=10, b=10))

fig_treemap.show()

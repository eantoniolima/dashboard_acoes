# ==========================================
# IMPORTANDO BIBLIOTECAS
# ==========================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid

# ==========================================
# CONFIGURAÇÕES INICIAIS
# ==========================================
st.set_page_config(
    page_title="Dashboard de Ações",
    page_icon="quant_orange__sem_fundo.png",
    layout="wide"
)
# ==========================================
# CSS RESPONSIVO
# ==========================================
st.markdown("""
<style>

/* ==========================================
   NÚMEROS DAS MÉTRICAS
   ========================================== */
[data-testid="stMetricValue"] {
    font-size: clamp(14px, 1.4vw, 24px);
    white-space: nowrap;
}


/* ==========================================
   TEXTO DAS MÉTRICAS
   ========================================== */
[data-testid="stMetricLabel"] {
    font-size: clamp(8px, 0.8vw, 14px);
}


/* ==========================================
   IMAGENS
   ========================================== */
[data-testid="stImage"] img {
    max-width: 85px;
    width: 100%;
    height: auto;
}


/* ==========================================
   AJUSTE PARA TELAS MENORES
   ========================================== */
@media (max-width: 900px) {

    [data-testid="stMetricValue"] {
        font-size: clamp(14px, 2vw, 22px);
    }

    [data-testid="stMetricLabel"] {
        font-size: 11px;
    }

}

</style>
""", unsafe_allow_html=True)

# ==========================================
# CORPO PRINCIPAL DO DASHBOARD
# ==========================================
st.title("Dashboard de Ações")

# ==========================================
# CONFIGURAÇÕES DA BARRA LATERAL
# ==========================================


def build_sidebar():
    # Configurações da barra lateral
    # para colocar a logo no centro da barra lateral
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])

    with col2:
        st.image("quant_orange__sem_fundo.png", width=200)

    ticker_list = pd.read_csv("acoes-listadas-b3.csv")  # lista de ações da B3

# selecionando as ações que o usuário deseja analisar
    tickers = st.multiselect(
        label="Selecione as ações",
        options=ticker_list
    )

    tickers = [t + ".SA" for t in tickers]
# selecionando o período de análise
    start_date = st.date_input(
        "Data de início",
        format="DD/MM/YYYY",
        value=datetime(2018, 1, 1)
    )

    end_date = st.date_input(
        "Data de fim",
        format="DD/MM/YYYY",
        value=datetime.now()
    )

    if tickers:
        prices = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            auto_adjust=False
            # retornando apenas os preços ajustados de fechamento das ações selecionadas
        )["Adj Close"]
        # removendo o sufixo ".SA" dos nomes das colunas do dataframe de preços
        prices.columns = prices.columns.str.rstrip(".SA")
    else:
        prices = pd.DataFrame()  # criando um dataframe vazio caso não haja tickers selecionados

    return tickers, prices

#

# ==========================================
# Função para construir o corpo principal do dashboard
# ==========================================


def build_main(tickers, prices):

    if prices.empty:
        st.info("Selecione pelo menos uma ação no menu lateral.")
        return
    # ==========================================
    # IBOVESPA
    # ==========================================

    ibov = yf.download(
        "^BVSP",
        start=prices.index[0],
        end=prices.index[-1],
        auto_adjust=False,
        progress=False
    )["Adj Close"]

    # Garante que seja uma Series
    if isinstance(ibov, pd.DataFrame):
        ibov = ibov.iloc[:, 0]

    # Retorno total do Ibovespa
    ibov_retorno = (ibov.iloc[-1] / ibov.iloc[0]) - 1

    # Volatilidade anualizada do Ibovespa
    ibov_vol = ibov.pct_change().dropna().std() * np.sqrt(252)

    # ==========================================
    # CÁLCULOS
    # ==========================================
    # Colocando pesos iguais para cada ação selecionada
    # utilizando o comando np.ones para criar um array de uns com o tamanho do número de tickers selecionados,
    # e dividindo pelo número de tickers para obter pesos iguais. e em seguida,
    # utilizando o comando np.array para criar um array vazio caso não haja tickers selecionados.
    weights = np.ones(len(tickers)) / len(tickers) if tickers else np.array([])

    # weights #teste de pesos iguais para cada ação selecionada

    # calculando o preço do portfólio como a soma ponderada dos preços das ações selecionadas
    prices["Portfolio"] = prices @ weights
    # normalizando os preços para o primeiro dia do período selecionado
    norm_prices = 100 * prices / prices.iloc[0]
    # calculando os retornos diários das ações selecionadas, preferencia para usar o dropna() para
    # remover os valores nulos que podem ocorrer no primeiro dia do período selecionado
    returns = prices.pct_change().dropna()
    # calculando a volatilidade anualizada das ações selecionadas
    vols = returns.std() * np.sqrt(252)
    # calculando o retorno total das ações selecionadas
    rets = (norm_prices.iloc[-1] - 100)/100

    # ==========================================
    # GRID DE VISUALIZAÇÃO
    # ==========================================
    num_cards = len(prices.columns)

    if num_cards <= 2:
        cards_por_linha = num_cards
    else:
        cards_por_linha = 4

    mygrid = grid(
        cards_por_linha,
        vertical_align='top'
    )

    for t in prices.columns:
        c = mygrid.container(border=True)
        c.subheader(t, divider="red")

        COL1, COL2, COL3 = c.columns(
            [0.9, 2, 2],
            gap="small",
            vertical_alignment="center"
        )

        if t == "Portfolio":
            COL1.image('pie_chart.svg',
                       use_container_width=True
                       )
        else:
            COL1.image(
                f"https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png",
                use_container_width=True
            )

        COL2.metric("Retorno", f"{rets[t]:.0%}")
        COL3.metric("Volatilidade", f"{vols[t]:.0%}")
        style_metric_cards(
            background_color='rgba(255, 255, 255, 0.1)'
        )
        # ==========================================
    # CARD FIXO DO IBOVESPA
    # ==========================================

    c = mygrid.container(border=True)

    c.subheader("IBOVESPA", divider="green")

    COL1, COL2, COL3 = c.columns(
        [2, 2, 2],
        gap="small",
        vertical_alignment="center"
    )

    COL1.image(
        "ibov.svg",
        use_container_width=True
    )

    COL2.metric(
        "Retorno",
        f"{ibov_retorno:.0%}"
    )

    COL3.metric(
        "Volatilidade",
        f"{ibov_vol:.0%}"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Desempenho Relativo")
        st.line_chart(norm_prices, height=600)

    with col2:
        st.subheader("Risco-Retorno")
        fig = px.scatter(
            x=vols,
            y=rets,
            text=vols.index,
            color=rets/vols,
            color_continuous_scale=px.colors.sequential.Bluered_r
        )
        fig.update_traces(
            textfont_color='white',
            marker=dict(size=45),
            textfont_size=10,
        )
        fig.layout.yaxis.title = 'Retorno Total'
        fig.layout.xaxis.title = 'Volatilidade (anualizada)'
        fig.layout.height = 600
        fig.layout.xaxis.tickformat = ".0%"
        fig.layout.yaxis.tickformat = ".0%"
        fig.layout.coloraxis.colorbar.title = 'Sharpe'
        st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # GRÁFICOS DE LINHA
    # ==========================================
    st.dataframe(prices)


with st.sidebar:
    tickers, prices = build_sidebar()

# Construção do corpo principal do dashboard
build_main(tickers, prices)

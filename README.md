DASHBOARD DE AÇÕES

Aplicação desenvolvida em Python para estudar o mercado financeiro por meio da análise de ações brasileiras, de uma composição de portfólio e de indicadores do Ibovespa.

O objetivo principal é aprender sobre o mercado financeiro e construir um portfólio de projetos de análise de dados, praticando programação, cálculos financeiros e visualização interativa.

INSPIRAÇÃO E CRÉDITOS

Este dashboard foi inspirado no vídeo do Código Quant indicado abaixo. Os créditos pelo tutorial, pela proposta original e pelo código que serviu de base pertencem ao seu autor. Esta versão é uma adaptação para estudo, com personalizações de interface e inclusão de funcionalidades.

Vídeo original:
https://www.youtube.com/watch?v=LAHlE_Lt9N4&t=296s

Repositório de referência:
https://github.com/codigoquant/stock_dashboard

Quem é antigo na "internetê" sabe o significado do termo “kibado”! Quem lembra do Kibe Loco vai entender a referência. 
Aqui, a inspiração vem acompanhada dos devidos créditos e do reconhecimento ao trabalho original.

SOBRE O PROJETO

A aplicação permite:
- Selecionar ações da B3 a partir de uma lista em CSV.
- Definir o período de análise.
- Consultar preços históricos ajustados de fechamento.
- Visualizar retorno total e volatilidade anualizada em cards.
- Exibir uma composição denominada Portfolio.
- Consultar retorno e volatilidade do Ibovespa em um card adicional.
- Comparar séries normalizadas na base 100.
- Explorar um gráfico de risco e retorno.
- Consultar a tabela dos preços utilizados.

PERSONALIZAÇÕES E ADAPTAÇÕES DESTA VERSÃO

Os itens abaixo descrevem as adaptações presentes no código enviado. Sem uma comparação integral com o código original do vídeo, não se atribui novidade a todas as funcionalidades ou fórmulas.

1. CSS e organização dos grids

O principal foco da personalização visual foi ajustar o tamanho dos números, dos rótulos e das imagens dentro dos cards:
- Números das métricas: font-size: clamp(14px, 1.4vw, 24px).
- Rótulos das métricas: font-size: clamp(8px, 0.8vw, 14px).
- white-space: nowrap para manter os valores na mesma linha.
- Imagens com largura máxima de 85px, largura de 100% e altura proporcional.
- Regra específica para telas com até 900px, ajustando números e rótulos.

A função CSS clamp define um tamanho mínimo, um tamanho variável conforme a largura da janela e um tamanho máximo. Isso ajuda a adaptar a fonte à tela, mas não mede automaticamente o espaço disponível em cada card. Portanto, valores longos ainda podem ficar apertados.

O grid usa um ou dois cards por linha quando existem até duas colunas no dataframe; nos demais casos, configura quatro posições por linha. Essa contagem inclui Portfolio, mas não inclui o card do Ibovespa, acrescentado posteriormente.

Dentro dos cards das ações e do Portfolio, as colunas seguem a proporção [0.9, 2, 2], com espaçamento pequeno e alinhamento vertical central. O card do Ibovespa utiliza [2, 2, 2]. Também foram utilizados bordas, divisores coloridos e fundo semitransparente nas métricas.

O CSS atual é global: afeta todas as métricas e imagens correspondentes aos seletores, incluindo as do Ibovespa. Não existe neste código uma regra exclusiva para diminuir apenas os números desse card.

2. Identidade visual e ícones

Inclusão de logo na barra lateral e ícone da página, além de imagens das empresas e arquivos SVG específicos para Portfolio e Ibovespa.

Os ícones das ações são carregados do repositório thefintz/icones-b3. Os créditos desses recursos pertencem aos seus respectivos autores:
https://github.com/thefintz/icones-b3

3. Inclusão do Ibovespa

Consulta do índice pelo ticker ^BVSP e exibição de um card com retorno total e volatilidade anualizada. Há também tratamento para converter o resultado em uma Series quando o download retorna um DataFrame.

Nesta versão, o Ibovespa aparece no card, mas não foi incluído no gráfico de desempenho relativo nem no gráfico de risco e retorno.

4. Consulta dos preços ajustados

O download utiliza auto_adjust=False e seleciona explicitamente a coluna Adj Close, mantendo o uso dos preços ajustados de fechamento nos cálculos.

FÓRMULAS UTILIZADAS

As fórmulas abaixo documentam o funcionamento da versão atual. Não são apresentadas como fórmulas inéditas ou necessariamente diferentes das utilizadas pelo autor do tutorial.

Normalização na base 100:
    preço normalizado = 100 × preço atual / preço inicial
Permite comparar a evolução de séries que começam em valores diferentes.

Retorno total:
    retorno total = preço final / preço inicial − 1
No código das ações, a expressão equivalente é:
    (preço normalizado final − 100) / 100
O Ibovespa utiliza diretamente a razão entre valor final e inicial.

Retorno diário:
    retorno diário = preço atual / preço anterior − 1
Calculado com pct_change(), seguido da remoção dos registros com valores ausentes.

Volatilidade anualizada:
    volatilidade = desvio padrão dos retornos diários × raiz quadrada de 252
Adota a convenção de 252 pregões por ano.

Composição Portfolio:
    coeficiente de cada ação = 1 / quantidade de ações
    Portfolio = soma dos preços multiplicados por esses coeficientes
O código aplica coeficientes iguais aos preços nominais. Isso produz uma média de preços, mas não representa, em geral, uma carteira com o mesmo valor financeiro investido em cada ação. Para representar esse objetivo, seria necessário ajustar a construção da carteira, por exemplo usando séries normalizadas e definindo a regra de rebalanceamento.

Indicador de cor do gráfico de risco e retorno:
    indicador = retorno total / volatilidade anualizada
A legenda atual chama esse indicador de “Sharpe”. Entretanto, a expressão não desconta uma taxa livre de risco e combina retorno acumulado do período com volatilidade anualizada. Por isso, deve ser entendida como uma razão simplificada de retorno por volatilidade, e não como o índice de Sharpe convencional.

TECNOLOGIAS E BIBLIOTECAS

Python
Linguagem utilizada no desenvolvimento da aplicação.

Streamlit
Criação da interface web, dos filtros, dos cards, das tabelas e dos gráficos.

Pandas
Organização dos dados, leitura do CSV e cálculo das séries de retornos.

NumPy
Operações numéricas, criação dos coeficientes e anualização da volatilidade.

yfinance
Obtenção dos dados históricos das ações e do Ibovespa pelo Yahoo Finance.

Plotly Express
Construção do gráfico interativo de risco e retorno.

streamlit-extras
Organização do grid e personalização visual dos cards de métricas.

datetime
Definição das datas iniciais dos filtros.

CSS / HTML
Personalização de fontes, imagens e apresentação em diferentes tamanhos de tela.

ARQUIVOS NECESSÁRIOS

- dashboard.py: código da aplicação, caso salvo com esse nome.
- acoes-listadas-b3.csv: lista de ações disponíveis para seleção.
- quant_orange__sem_fundo.png: logo e ícone da página.
- pie_chart.svg: ícone do Portfolio.
- ibov.svg: ícone do Ibovespa.

Os arquivos locais devem estar acessíveis pelos caminhos utilizados no código. Também é necessária conexão com a internet para obter as cotações e os ícones das empresas.

COMO EXECUTAR

Instale as dependências:
    pip install streamlit pandas numpy yfinance plotly streamlit-extras

Na pasta do projeto, execute:
    python -m streamlit run dashboard.py

ou execute diretamente do streamlit


O projeto está em desenvolvimento e serve como exercício prático de estudo do mercado financeiro e construção de um portfólio de análises.

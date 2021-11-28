# Como conseguir os dados crus?

## Empresas

A Receita Federal compila e divulga informação públicas das empresas brasileiras. Para acessar os microdados, basta visitar o [Portal de Dados Abertos](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj) do Ministério da Economia.

O tratamento realizado nos dados se limitou a selecionar as colunas necessárias e filtrar as linhas representativas de empresas ativas de Recife.

## CEPs

Existem algumas fontes públicas de informações de CEPs. A maioria delas é resultado de raspagem de dados dos Correios. Para conseguir dados geolocalizados de CEPs, fiz uma raspagem do site [CEP da Rua](https://cepdarua.net/). No HTML das listas de CEPs por bairro do Recife, é possível identificar a latitude e longitude do ponto central de cada CEP. O código de raspagem não apresenta nenhuma característica especial, uma vez que trata-se de um site estático, bastante amigável a execução automações.

Com relação a precisão das informações, a partir da base de CEPs extraída, é possível mapear 85% dos CEPs das empresas de Recife.

## Transporte cicloviário

No [Portal de Dados Abertos ](http://dados.recife.pe.gov.br/dataset/ciclovias-ciclofaixas-estacoes-de-aluguel-de-bikes-e-rotas/) é possível acessar dados geolocalizados de estações de bicicletas compartilhadas.

## Transporte público

No [Portal de Dados Abertos ](http://dados.recife.pe.gov.br/fa_IR/dataset/faixas-e-corredores-de-onibus/) é possível acessar dados geolocalizados de corredores de ônibus. Os dados representam polígonos, para adequá-los realizei uma transformação dos dados de wide (em que cada linha representa um corredor de ônibus e cada valor de coluna um ponto que desenha o contorno da via) para narrow (em que há 3 colunas, NOME_VIA, LAT e LONG que, respectivamente, identificam a via e mapeiam as coordenadas em que há ponto de contato com a via).

## Área Risco

Dados sobre segurança não são nada fáceis de encontrar. São poucas as Secretarias de Segurança divulgam informações de maneira transparente (disponível em arquivos que podem ser utilizados em projetos e pesquisas) e num nível de desagregação que permita identificar hotspots de violência.

Os dados de Área de Risco utilizados dizem respeito ao monitoramento realizado pela Defesa Civil de Recife. A base compila chamados que denunciam tanto situação irregular de moradias como eventos de violência nos bairros. Eles podem ser consultados no [Portal de Dados Abertos ](http://dados.recife.pe.gov.br/de/dataset/monitoramento-das-areas-de-riscos) da Prefeitura de Recife.
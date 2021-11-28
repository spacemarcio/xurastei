create table empresas (
	CNPJ				bigint primary key,
	SITUACAO_CADASTRAL	char(5),
	NATUREZA_JURIDICA	integer,
	DATA_ABERTURA		date,
	CNAE				integer,
	CEP					bigint
);

create table area_risco (
	NUMERO_PROCESSO		bigint primary key,
	DATA_SOLICITACAO	date,
	LAT					double precision,
	LONG				double precision,
	VITIMA				char(3),
	VITIMA_FATAL		char(3),
	DATA_CONCLUSAO		date
);

create table bikes (
	ID_ESTACAO			integer primary key,
	ESTACAO				char(50),
	CAPACIDADE			integer,
	LAT					double precision,
	LONG				double precision
);

create table corredor_onibus (
	ID_PONTO			integer primary key,
	NOME_VIA			char(75),
	BAIRRO				char(25),
	LAT					double precision,
	LONG				double precision
);

create table ceps (
	CEP					bigint primary key,
	LOGRADOURO			char(100),
	BAIRRO				char(25),
	LAT					double precision,
	LONG				double precision
);

create table pracas (
	ID_AREA				bigint primary key,
	NOME_AREA			char(100),
	TIPO_AREA			char(15),
	LAT					double precision,
	LONG				double precision
);

create table feiras (
	ID_FEIRA			integer primary key,
	NOME_FEIRA			char(100),
	LAT					double precision,
	LONG				double precision
);

create table anuncios (
	TITULO char(250),
	VALOR integer,
	DESCRICAO text,
	MUNICIPIO char(250),
	BAIRRO char(250),
	CEP integer,
	LOGRADOURO char(250),
	CATEGORIA char(50),
	TIPO char(50),
	CONDOMINIO integer,
	IPTU integer,
	AREA_UTIL integer,
	QUARTOS integer,
	BANHEIROS integer,
	VAGAS_GARAGEM integer,
	DETALHES_IMOVEL text,
	DETALHES_CONDOMINIO text,
	FOTOS text,
	URL char(250) primary key,
	DATA_CONSULTA timestamp
);

create table lugares (
	CEP					integer primary key,
	TIPO_LUGAR			char(50)
);
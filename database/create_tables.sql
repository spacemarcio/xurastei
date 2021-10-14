create table empresas (
	CNPJ				bigint,
	SITUACAO_CADASTRAL	char(5),
	NATUREZA_JURIDICA	integer,
	DATA_ABERTURA		date,
	CNAE				integer,
	CEP					bigint
);

create table area_risco (
	NUMERO_PROCESSO		bigint,
	DATA_SOLICITACAO	date,
	LAT					double precision,
	LONG				double precision,
	VITIMA				char(3),
	VITIMA_FATAL		char(3),
	DATA_CONCLUSAO		date
);

create table bikes (
	ESTACAO				char(50),
	CAPACIDADE			integer,
	LAT					double precision,
	LONG				double precision
);

create table corredor_onibus (
	NOME_VIA			char(75),
	BAIRRO				char(25),
	LAT					double precision,
	LONG				double precision
);

create table ceps (
	CEP					bigint,
	LOGRADOURO			char(100),
	BAIRRO				char(25),
	LAT					double precision,
	LONG				double precision
);

create table pracas (
	ID					bigint,
	NOME_AREA			char(100),
	TIPO_AREA			char(15),
	LAT					double precision,
	LONG				double precision
);

create table feiras (
	NOME_FEIRA			char(100),
	LAT					double precision,
	LONG				double precision
);
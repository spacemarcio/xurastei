drop table if exists cep_features;
create table cep_features as (
	select
		a.CEP,
		case when qtd_esporte is Null then 0 else qtd_esporte end qtd_esporte,
		case when qtd_mercado is Null then 0 else qtd_mercado end qtd_mercado,
		case when qtd_educacao is Null then 0 else qtd_educacao end qtd_educacao,
		case when qtd_cultura is Null then 0 else qtd_cultura end qtd_cultura,
		case when qtd_saude is Null then 0 else qtd_saude end qtd_saude,
		case when qtd_policia is Null then 0 else qtd_policia end qtd_policia,
		case when qtd_turismo is Null then 0 else qtd_turismo end qtd_turismo,
		case when qtd_condominio is Null then 0 else qtd_condominio end qtd_condominio,
		case when qtd_restaurante is Null then 0 else qtd_restaurante end qtd_restaurante,
		case when qtd_industria is Null then 0 else qtd_industria end qtd_industria,
		case when qtd_ocorrencias_risco is Null then 0 else qtd_ocorrencias_risco end qtd_ocorrencias_risco,
		case when qtd_estacoes_bikes is Null then 0 else qtd_estacoes_bikes end qtd_estacoes_bikes,
		case when qtd_onibus is Null then 0 else qtd_onibus end qtd_onibus,
		case when qtd_area_verde is Null then 0 else qtd_area_verde end qtd_area_verde,
		case when qtd_pracas is Null then 0 else qtd_pracas end qtd_pracas,
		case when qtd_feiras is Null then 0 else qtd_feiras end qtd_feiras
	from
		ceps as a
	left join
		cep_servicos_temp as b
	on
		a.CEP = b.CEP
	left join
		cep_area_risco_temp as c
	on
		a.CEP = c.CEP
	left join
		cep_bikes_temp as d
	on
		a.CEP = d.CEP
	left join
		cep_onibus_temp as e
	on
		a.CEP = e.CEP
	left join
		cep_pracas_temp as f
	on
		a.CEP = f.CEP
	left join
		cep_feiras_temp as g
	on a.CEP = g.CEP
);
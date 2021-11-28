drop table if exists servicos_temp;
create temporary table servicos_temp as (
	select
        coord,
        case 
            when cast(CNAE as varchar) like '85911%' then 1 
            when cast(CNAE as varchar) like '93123%' then 1
            when cast(CNAE as varchar) like '93131%' then 1
            when cast(CNAE as varchar) like '93191%' then 1
            else 0
        end as ind_esporte,
        case
            when cast(CNAE as varchar) like '472%' then 1 
            when cast(CNAE as varchar) like '47113%' then 1 
            when cast(CNAE as varchar) like '47121%' then 1
            else 0
        end as ind_mercado,
        case
            when cast(CNAE as varchar) like '85%' then 1
            when cast(CNAE as varchar) like '91015%' then 1
            when cast(CNAE as varchar) like '91023%' then 1
            else 0
        end as ind_educacao,
        case
            when cast(CNAE as varchar) like '91%' then 1
            when cast(CNAE as varchar) like '83%' then 1
            else 0
        end as ind_cultura,
        case
            when cast(CNAE as varchar) like '86%' then 1
            when cast(CNAE as varchar) like '87%' then 1
            when cast(CNAE as varchar) like '477%' then 1
            else 0
        end as ind_saude,
        case
            when cast(CNAE as varchar) like '84248%' then 1
            when cast(CNAE as varchar) like '84256%' then 1
            else 0
        end as ind_policia,
        case
            when cast(CNAE as varchar) like '551%' then 1
            when cast(CNAE as varchar) like '79902%' then 1
            else 0
        end as ind_turismo,
        case
            when cast(CNAE as varchar) like '81125%' then 1
            else 0
        end as ind_condominio,
        case
            when cast(CNAE as varchar) like '56%' then 1
            else 0            
        end as ind_restaurante,
        case
            when CNAE/100000 < 33 then 1
            else 0
        end as ind_industria
	from
		empresas a
	inner join
		ceps b
	on
		a.CEP = b.CEP
);

drop table if exists servicos;
create table servicos as (
	select
		coord,
		max(ind_esporte) as ind_esporte,
		max(ind_mercado) as ind_mercado,
		max(ind_educacao) as ind_educacao,
		max(ind_cultura) as ind_cultura,
		max(ind_saude) as ind_saude,
		max(ind_policia) as ind_policia,
		max(ind_turismo) as ind_turismo,
		max(ind_condominio) as ind_condominio,
		max(ind_restaurante) as ind_restaurante,
		max(ind_industria) as ind_industria
	from
		servicos_temp
	group by
		coord
);

drop table if exists cep_servicos_temp;
create temporary table cep_servicos_temp as (
	select
		CEP,
		sum(ind_esporte) as qtd_esporte,
		sum(ind_mercado) as qtd_mercado,
		sum(ind_educacao) as qtd_educacao,
		sum(ind_cultura) as qtd_cultura,
		sum(ind_saude) as qtd_saude,
		sum(ind_policia) as qtd_policia,
		sum(ind_turismo) as qtd_turismo,
		sum(ind_condominio) as qtd_condominio,
		sum(ind_restaurante) as qtd_restaurante,
		sum(ind_industria) as qtd_industria
	from
		ceps as a, servicos as b 
	where 
		ST_Distance(a.coord, b.coord) < 0.006 -- 0.006 degrees = 600 meters
	group by
		CEP
);

drop table if exists cep_area_risco_temp;
create temporary table cep_area_risco_temp as (
	select
		CEP,
		count(distinct(numero_processo)) as qtd_ocorrencias_risco
	from
		ceps as a, area_risco as b
	where 
		ST_Distance(a.coord, b.coord) < 0.006 -- 0.006 degrees = 600 meters
	group by
		CEP
);

drop table if exists cep_bikes_temp;
create temporary table cep_bikes_temp as (
	select
		CEP,
		count(distinct(estacao)) as qtd_estacoes_bikes
	from
		ceps as a, bikes as b
	where 
		ST_Distance(a.coord, b.coord) < 0.006 -- 0.006 degrees = 600 meters
	group by
		CEP
);

drop table if exists cep_onibus_temp;
create temporary table cep_onibus_temp as (
	select
		CEP,
		count(nome_via) as qtd_onibus
	from
		ceps as a, corredor_onibus as b
	where 
		ST_Distance(a.coord, b.coord) < 0.006 -- 0.006 degrees = 600 meters
	group by
		CEP
);

drop table if exists cep_pracas_temp;
create temporary table cep_pracas_temp as (
	select
		CEP,
		sum(
			case
				when tipo_area = 'Area Verde' then 1
				else 0
			end
		) as qtd_area_verde,
		sum(
			case
				when tipo_area = 'Praça' then 1
				else 0
			end
		) as qtd_pracas
	from
		ceps as a, pracas as b
	where 
		ST_Distance(a.coord, b.coord) < 0.006 -- 0.006 degrees = 600 meters
	group by
		CEP
);

drop table if exists cep_feiras_temp;
create temporary table cep_feiras_temp as (
	select
		CEP,
		count(distinct(nome_feira)) as qtd_feiras
	from
		ceps as a, feiras as b
	where 
		ST_Distance(a.coord, b.coord) < 0.006 -- 0.006 degrees = 600 meters
	group by
		CEP
);

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
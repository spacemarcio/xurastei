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
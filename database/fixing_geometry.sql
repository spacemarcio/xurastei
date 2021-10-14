alter table area_risco add column coord geometry(Point, 4326);

update area_risco set coord = ST_SetSRID(ST_MakePoint(LONG, LAT),4326);


alter table bikes add column coord geometry(Point, 4326);

update bikes set coord = ST_SetSRID(ST_MakePoint(LONG, LAT),4326);


alter table corredor_onibus add column coord geometry(Point, 4326);

update corredor_onibus set coord = ST_SetSRID(ST_MakePoint(LONG, LAT),4326);


alter table ceps add column coord geometry(Point, 4326);

update ceps set coord = ST_SetSRID(ST_MakePoint(LONG, LAT),4326);


alter table pracas add column coord geometry(Point, 4326);

update pracas set coord = ST_SetSRID(ST_MakePoint(LONG, LAT),4326);


alter table feiras add column coord geometry(Point, 4326);

update feiras set coord = ST_SetSRID(ST_MakePoint(LONG, LAT),4326);
## Step-by-step to setup database

1. Execute `create_tables.sql`. 
2. Populate tables `empresas`, `area_risco`, `bikes`, `corredor_onibus`, `ceps`, `pracas`, `feiras` with data (you can do that with copy command PSQL or Dbeaver interface).
3. Execute `fixing_geometry.sql` to add postgis extension to RDS and transform lat/long columns in geometry points.
4. Execute `create_features.sql` to prepare tables of features.
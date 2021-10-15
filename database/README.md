## Step-by-step to setup database

1. Execute `create_tables.sql`.
2. Populate tables with data (you can do that with copy command PSQL or Dbeaver interface).
3. Execute `fixing_geometry.sql` to transform lat/long columns in geometry points.
4. Execute `create_features.sql` to prepare tables of features.
5. Execute `features_view.sql` to join features tables and make finial adjustments.
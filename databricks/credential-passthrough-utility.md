You can import credential-passthrough-utility notebook in Azure Databricks with

```
%run /credential-passthrough-utility
```

Then you can run:

```
df = pandas_read_csv('datalakehuduaexample', 'raw', 'sample_data.csv', nrows = 50)
```

```
pandas_write_csv(df, 'datalakehuduaexample', 'raw', 'sample_data_3.csv', index = False)
```

```
pandas_write_to_excel(df, 'datalakehuduaexample', 'raw', 'sample_data.xlsx')
```

```
gdf = geopandas_load_shapefile('datalakehuduaexample', 'raw', 'shapefile_dir', rows = 10)
```

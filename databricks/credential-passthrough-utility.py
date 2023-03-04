import pandas as pd
import uuid
import os
import shutil
import geopandas as gpd

def pandas_read_csv(storage_account, container, path, **kwarg):
    guid = str(uuid.uuid4())
    newpath = f'/dbfs/mnt/tmpadlsgen2/{guid}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    dbutils.fs.cp(f"abfss://{container}@{storage_account}.dfs.core.windows.net/{path}", f"dbfs:/mnt/tmpadlsgen2/{guid}/{path}")
    df = pd.read_csv(f"/dbfs/mnt/tmpadlsgen2/{guid}/{path}", **kwarg)
    shutil.rmtree(newpath)
    return df
print('pandas_read_csv(storage_account, container, path, **kwarg) is available')


def pandas_write_csv(df, storage_account, container, path, **kwarg):
    guid = str(uuid.uuid4())
    newpath = f'/dbfs/mnt/tmpadlsgen2/{guid}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    df.to_csv(f"/dbfs/mnt/tmpadlsgen2/{guid}/{path}", **kwarg)
    dbutils.fs.cp(f"dbfs:/mnt/tmpadlsgen2/{guid}/{path}", f"abfss://{container}@{storage_account}.dfs.core.windows.net/{path}")
    shutil.rmtree(newpath)
print('pandas_write_csv(df, storage_account, container, path, **kwarg) is available')


def geopandas_load_shapefile(storage_account, container, folder, **kwarg):
    guid = str(uuid.uuid4())
    newpath = f'/dbfs/mnt/tmpadlsgen2/{guid}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    files = dbutils.fs.ls('abfss://raw@datalakehuduaexample.dfs.core.windows.net/shapefile_dir')
    for file in files:
        dbutils.fs.cp(file.path, f"dbfs:/mnt/tmpadlsgen2/{guid}/{folder}/{file.name}")
    gdf = gpd.read_file(f"/dbfs/mnt/tmpadlsgen2/{guid}/{folder}", **kwarg)
    shutil.rmtree(newpath)
    return gdf
print('geopandas_load_shapefile(storage_account, container, folder, **kwarg) is available')


def pandas_write_to_excel(df, storage_account, container, path, **kwarg):
    guid = str(uuid.uuid4())
    newpath_dbfs_mnt = f'/dbfs/mnt/tmpadlsgen2/{guid}'
    if not os.path.exists(newpath_dbfs_mnt):
        os.makedirs(newpath_dbfs_mnt)
    newpath_local = f'{guid}'
    if not os.path.exists(newpath_local):
        os.makedirs(newpath_local)
    df.to_excel(f'{newpath_local}/{path}', **kwarg)
    shutil.copyfile(f'{newpath_local}/{path}', f'{newpath_dbfs_mnt}/{path}')
    dbutils.fs.cp(f"dbfs:/mnt/tmpadlsgen2/{guid}/{path}", f"abfss://{container}@{storage_account}.dfs.core.windows.net/{path}")
    shutil.rmtree(newpath_dbfs_mnt)
    shutil.rmtree(newpath_local)
print('pandas_write_to_excel(df, storage_account, container, path, **kwarg) is available')

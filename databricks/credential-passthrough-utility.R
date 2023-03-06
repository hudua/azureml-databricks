%r

r_read_csv <- function(storage_account, container, path) {
  temp_dir <- "/dbfs/mnt/tmpadlsgen2/r-temp-dir/"
  if (file.exists(temp_dir)){} else {
    dir.create(temp_dir)
  }
  dbutils.fs.cp(paste0("abfss://",container,"@",storage_account,".dfs.core.windows.net/",path), paste0("dbfs:/mnt/tmpadlsgen2/r-temp-dir/",path))
  data.frame <- read.csv(file.path(temp_dir, path))
  file.remove(paste0(temp_dir,path))
  return(data.frame)
}
print("r_read_csv(storage_account, container, path) is available")

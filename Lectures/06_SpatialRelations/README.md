## Spatial Relations

more to come ... 


## Conda 
https://medium.com/analytics-vidhya/fastest-way-to-install-geopandas-in-jupyter-notebook-on-windows-8f734e11fa2b
https://realpython.com/advanced-visual-studio-code-python/

```
conda init "$(basename "${SHELL}")"

conda create -n geo_env

conda activate geo_env

conda config  --env --add channels conda-forge

conda config --env --set channel_priority strict

conda install geopandas

conda install jupyter notebook

# start using environment
python -m ipykernel install --name geo_env

# stop using environment
conda deactivate

# permanently delete an environment
conda env remove --name ENVIRONMENT



conda install -n geo_env -y numpy scipy pandas matplotlib ipython ipykernel ipympl  rtree shapely geos geopandas 
```


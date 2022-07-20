# IMDB_Parser

## This repository provide script for crawling the casts' photos from IMDB.com

## Usage
```
source activate aws_neuron_mxnet_p36
```

```
mkdir -p temp/actors
mkdir -p data/actors
```
You can put nameid, name in the JSON/ directory.

```
python Actors_photos_parcer.py
```

Then the photos will be saved in data/actors/name_id


# winterveil
Add winter effect to images

## Features
- Add fog
- Add showfall
- Add fallen snow

## Example


| Input                            | Fog                                | Snow                               | Fallen snow                         |
| -------------------------------- | ---------------------------------- | ---------------------------------- | ----------------------------------- |
| ![output_f](examples/makise.jpg) | ![output_f](examples/output_f.png) | ![output_f](examples/output_s.png) | ![output_f](examples/output_fs.png) |

| Fog + Snow                           | Fog + Fallen snow                     | Fallen snow + Snow                    | Fog + Snow + Fallen snow                |
| ------------------------------------ | ------------------------------------- | ------------------------------------- | --------------------------------------- |
| ![output_f](examples/output_f_s.png) | ![output_f](examples/output_f_fs.png) | ![output_f](examples/output_s_fs.png) | ![output_f](examples/output_f_s_fs.png) |


## Usage
### Install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Winterize image
```
python3 main.py path_to_image
```

## Options
```
usage: WinterVeil [-h] -i IMAGE [-f] [-s] [-ss SNOWFLAKE_SIZE] [-sc SNOWFLAKE_COUNT] [-fs]

options:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        input image path
  -f, --fog             add fog to the image
  -s, --snow            add snow to the image
  -ss SNOWFLAKE_SIZE, --snowflake-size SNOWFLAKE_SIZE
                        size of snowflakes in pixel
  -sc SNOWFLAKE_COUNT, --snowflake-count SNOWFLAKE_COUNT
                        number of snowflakes on image (visibility depends on depth map!)
  -fs, --fallen-snow    add fallen snow to the image
```

## Acknowledgments

This project uses the [MiDaS depth estimation model]([link-to-model-repository-or-paper](https://arxiv.org/abs/1907.01341)) by René Ranftl, Katrin Lasinger, David Hafner, Konrad Schindler, and Vladlen Koltun, which is licensed under the MIT License. If you use this project, please also cite their original work:

```bibtex
@article{Ranftl2020,
	author    = {Ren\'{e} Ranftl and Katrin Lasinger and David Hafner and Konrad Schindler and Vladlen Koltun},
	title     = {Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer},
	journal   = {IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)},
	year      = {2020},
}
```

```bibtex
@article{Ranftl2021,
	author    = {Ren\'{e} Ranftl and Alexey Bochkovskiy and Vladlen Koltun},
	title     = {Vision Transformers for Dense Prediction},
	journal   = {ArXiv preprint},
	year      = {2021},
}
```

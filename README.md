# Fraunhofer Versatile Video Encoder (VVenC)




## Partition Extraction:

For extracting partitions:  

1. Use cmd line as: ./vvencFFapp --InputFile path_to_yuv -s 1920x1080  -fr 60 -f 64 -q 22 --NumPasses 1 --GOPSize 1 -ip 1 -qpa 1 -t 1 -b path_to_bin  --TraceFile="name_or_path_of_trace.csv"  --TraceRule="D_PART_STAT:poc>=0"  > path_to_output_txt.txt

2. Normally we will get two csv files for each encoding CTU_xxx.csv and trace_xxx.csv.

3. Put all the csv files of sequences of same resolution under a directory and then call the python script csv_process.py as follow: csv_process.py -w <width_frame> -h <height_frame> -f <number_frame> -p <path_csv_files>
   where the -f option indicate the total number of frames encoded of frames and -p represent the path of generated partition python files (not given then generated in the same place as trace files)

4. Then we will get 4 python numpy arrays: ctu.npy, qt_map.npy, mt1_map.npy and mt2_map.npy (The max depth of mt split is equal to 2 for VVenc so two mt split maps would be enough)

ctu.npy: 	store the pixels for all ctus in shape (x, 128, 128, 1): Pixel values scaled by 1024
qt_map.npy:	store the qtmaps for all ctus in shape (x, 8, 8, 1) => The value of each element of qtmap is the depth QT for 16x16 region in CTU knowing that its value ranges from 1 to 4 for VVenc intra config

mt1_map.npy:	store the mtmaps for all ctus in shape (x, 32, 32, 1) => The value of each element mtmap represents the split type of each 4x4 region at mt depth 1: 
mt2_map.npy: 	..................................................................................................................................... at mt depth 2:

              
split types: 0 => Not split, 2 => Binary Horzontal Split, 3 => Binary Vertical Split, 4 => Tenary Horizontal Split, 5 => Tenary Vertical Split








## Shortcut by CU size info:
 
Step 1: Get the trace file for encoding QP37, for this we should manually set the macro VVENC_STAT to 1 (line 91 of .\source\Lib\CommonLib\TypeDef.h) and set the macro VVENC_ORACLE to 0 (line 50 of .\source\Lib\EncoderLib\EncCfg.h) and build the release bin file

   ./vvencFFapp  --InputFile  <path_to_yuv>  -s 416x240  -fr 60 -f 8 -q 37 --NumPasses 1 --GOPSize 1 -ip 1 -qpa 1 -t 1 -b BQSquare_416x240p_60Hz_iyuv_qp37_AI.266  --TraceFile="BQSquare_416x240p_60Hz_iyuv_qp37_AI_encoder.csv"  --TraceRule="D_PART_STAT:poc>=0"   > BQSquare_416x240p_60Hz_iyuv_qp37_AI_encoder.txt

Step 2: Get the cu size numpy file,  the -f option should be the number of frame contained by each csv trace file. -p should be the path containing all these csv trace files. 
 
python   ./csv_process.py -w <width_frame> -h <height_frame> -f <number_frame> -p <path_csv_files>

Step 3: Process the cu size file to get the max/min size map, for the --path and --npy option, we should just give the path (do not specify the file name)

python ./get_metric_map_from_npy.py --npy <path to the cu size numpy file>    --path  <path for the generated size map> --cell_size  <the scale of generated size map>  --metric <what kind of map we want to have>

Here the cell size indicate the scale by number of pixels on which we calculate the size map. For example  --cell_size  8 means we get a max/min size value for each 8x8 region inside CTU.  The metric option has 4 possible values: max_size_map_1d, max_size_map_2d, min_size_map_1d, min_size_map_2d. For example, max_size_map_1d means we will get a max value of width and height for each cell_size x cell_size region. Meanwhile, the max_size_map_2d is that we will get max maps separately for width and height, so the max map is two dimensional.

Step 4: Accelerate the encoding QP22 by reading the size map, for this we should set VVENC_STAT to 0 and VVENC_ORACLE to 1 and build the release bin file

   ./vvencFFapp    --InputFile  <path_to_yuv>  -s 416x240 -fr 60 -f 8 --NumPasses 1 --GOPSize 1 -ip 1 -qpa 1 -t 1 -b str.266  -q 22 --metric  max_size_map_2d  --metricscale 8 --metricpath  <path for the size map to load>  --metricqp 37 
 
Here the metricqp option represent the QP of encoding we want to use to speed up. metricscale is the same as cell_size of step 3. For --metricpath option, we should not specify the filename





## Getting the table of comparison between reference coding and dependent coding


python ./scripts/compare_cu_shape.py    <path to the cu shape files>

1. The cushape files are with file name started by cushape_map. These files are obtained after running the csv_process.npy.

2. The format of output is like this:  
	4x4 matrix 
	row represents dependent coding with QP 22, 27, 32, 37
	column represents reference coding with QP 22, 27, 32, 37  
 
3. each element of matrixs indicates the percentage of regions where the CU sizes of dependent encoding is smaller or equal to (both width and height) that of reference encoding   






The Fraunhofer Versatile Video Encoder (VVenC) is a fast and efficient H.266/VVC encoder implementation with the following main features:
- Easy to use encoder implementation with five predefined quality/speed presets;
- Perceptual optimization to improve subjective video quality, based on the XPSNR visual model;
- Extensive frame-level and task-based parallelization with very good scaling;
- Frame-level single-pass and two-pass rate control supporting variable bit-rate (VBR) encoding;
- Expert mode encoder interface available, allowing fine-grained control of the encoding process.

## Information

See the [Wiki-Page](https://github.com/fraunhoferhhi/vvenc/wiki) for more information:

* [Build information](https://github.com/fraunhoferhhi/vvenc/wiki/Build)
* [Usage documentation](https://github.com/fraunhoferhhi/vvenc/wiki/Usage)
* [VVenC performance](https://github.com/fraunhoferhhi/vvenc/wiki/Encoder-Performance)
* [License](https://github.com/fraunhoferhhi/vvenc/wiki/License)
* [Publications](https://github.com/fraunhoferhhi/vvenc/wiki/Publications)
* [Version history](https://github.com/fraunhoferhhi/vvenc/wiki/Changelog)

## Build

VVenC uses CMake to describe and manage the build process. A working [CMake](https://cmake.org/) installation is required to build the software. In the following, the basic build steps are described. Please refer to the [Wiki](https://github.com/fraunhoferhhi/vvenc/wiki/Build) for the description of all build options.

### How to build using CMake?

To build using CMake, create a `build` directory and generate the project:

```sh
mkdir build
cd build
cmake .. <build options>
```

To actually build the project, run the following after completing project generation:

```sh
cmake --build .
```

For multi-configuration projects (e.g. Visual Studio or Xcode) specify `--config Release` to build the release configuration.

### How to build using GNU Make?

On top of the CMake build system, convinence Makefile is provided to simplify the build process. To build using GNU Make please run the following:

```sh
make install-release <options>
```

Other supported build targets include `configure`, `release`, `debug`, `relwithdebinfo`, `test`,  and `clean`. Refer to the Wiki for a full list of supported features.

## Citing

Please use the following citation when referencing VVenC in literature:

```bibtex
@InProceedings{VVenC,
  author    = {Wieckowski, Adam and Brandenburg, Jens and Hinz, Tobias and Bartnik, Christian and George, Valeri and Hege, Gabriel and Helmrich, Christian and Henkel, Anastasia and Lehmann, Christian and Stoffers, Christian and Zupancic, Ivan and Bross, Benjamin and Marpe, Detlev},
  booktitle = {Proc. IEEE International Conference on Multimedia Expo Workshops (ICMEW)},
  date      = {2021},
  title     = {VVenC: An Open And Optimized VVC Encoder Implementation},
  doi       = {10.1109/ICMEW53276.2021.9455944},
  pages     = {1-2},
}
```

## Contributing

Feel free to contribute. To do so:

* Fork the current-most state of the master branch
* Apply the desired changes
* Add your name to [AUTHORS.md](./AUTHORS.md)
* Create a pull-request to the upstream repository

## License

Please see [LICENSE.txt](./LICENSE.txt) file for the terms of use of the contents of this repository.

For more information, please contact: vvc@hhi.fraunhofer.de

**Copyright (c) 2019-2022, Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung e.V. & The VVenC Authors.**

**All rights reserved.**

# Fraunhofer Versatile Video Encoder (VVenC)




Partition Extraction:

For extracting partitions:  

1. Use cmd line as: ./vvencFFapp --InputFile path_to_yuv -s 1920x1080  -fr 60 -f 64 -q 22 --NumPasses 1 --GOPSize 1 -ip 1 -qpa 1 -t 1 -b path_to_bin  --TraceFile="name_or_path_of_trace.csv"  --TraceRule="D_PART_STAT:poc>=0"  > path_to_output_txt.txt

2. Normally we will get two csv files for each encoding CTU_xxx.csv and trace_xxx.csv.

3. Put all the csv files of sequences of same resolution under a directory and then call the python script csv_process.py as follow: csv_process.py -w <width_frame> -h <height_frame> -f <number_frame> -p <path_csv_files>
   where the -f option indicate the total number of frames encoded of frames and -p represent the path of generated partition python files (not given then generated in the same place as trace files)

4. Then we will get 4 python numpy arrays: ctu.npy, qt_map.npy, mt1_map.npy and mt2_map.npy (The max depth of mt split is equal to 2 for VVenc so two mt split maps would be enough)

ctu.npy: 	store the pixels for all ctus in shape (x, 128, 128, 1)
qt_map.npy:	store the qtmaps for all ctus in shape (x, 8, 8, 1) => The value of each element of qtmap is the depth QT for 16x16 region in CTU knowing that its value ranges from 1 to 4 for VVenc intra config

mt1_map.npy:	store the mtmaps for all ctus in shape (x, 32, 32, 1) => The value of each element mtmap represents the split type of each 4x4 region at mt depth 1: 
mt2_map.npy: 	..................................................................................................................................... at mt depth 2:

              
split types: 0 => Not split, 2 => Binary Horzontal Split, 3 => Binary Vertical Split, 4 => Tenary Horizontal Split, 5 => Tenary Vertical Split








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

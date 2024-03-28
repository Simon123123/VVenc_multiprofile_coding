# Fraunhofer Versatile Video Encoder (VVenC)


This is the one of the first implemetation for multi-rate and multi-resolution fast encoding on VVenc encoder. We can leverage the reference encoding to accelerate the dependent encodings at various bitrates and resolutions respectively.
First of all, we should do the ref encoding and collect the partition information. Then we should process the partition obtained by python scripts to get the **CUshape map** or **Split map**. Then in the dependent encodings, we load the output of 
python script execution to achieve speed-ups.

There are multiple macros to for ref encoding and dependent encoding. The **VVENC_STAT**, **VVENC_MULTI_RESO** and **VVENC_MULTI_RATE** are both defined in TypeDef.h and at in EncCfg.h. The different functionings of the encoder with macro setting are shown in 
the following table.   




| 		              | Ref multi-rate & multi-reso encoding | Dep multi-rate encoding | Dep multi-reso encoding   |
| -------------       |:------------------------------------:|:-----------------------:| :------------------------:|    
|VVENC_STAT           | on 					     			 | off 					   | off	   				   |
|VVENC_MULTI_RESO     | on					     	         | off 					   | on      				   |
|VVENC_MULTI_RATE     | off                             	 | on 					   | off 					   |






## Partition Extraction:


1. For extracting partitions for multi-rate & multi-reso senario, set the corresponding macros 

2. Use the following command:  

```
./vvencFFapp -c <path to config file> --InputFile <path_to_yuv> -s widthxheight -fr <framerate> -f <number_frame_to_code> -q <qp> --NumPasses 1 -qpa 1 -t 1 -b <output_bin_file> --mr_path <location_output_partition> --mr <ratio_between_representations> --TraceRule="D_PART_STAT:poc>=0"  > output_text_file
```

For example:

```
./vvencFFapp -c C:\Desktop\VVenc_multiprofile_coding\cfg\randomaccess_medium.cfg --InputFile E:\JVET_CTC\RaceHorses_416x240p_30Hz_iyuv.yuv -s 416x240 -fr 30 -f 16 -q 22 --NumPasses 1 -qpa 1 -t 1 -b C:\output\out.bin  --mr_path "C:\mr_folder" --mr 2 --TraceRule="D_PART_STAT:poc>=0" > C:\output\ref_mr_2_RaceHorses_416x240p_30Hz_iyuv_qp_22.txt
```

Specifically, the option --mr represents the ratio between the dependent resolution and reference resolution. For example, we use the encoding of sequence 240p to accelerate the encoding of the same sequence at 480p. In such case, the mr option should equal to 2.  

3. The output of encoding contains two files: one CSV file named as CUshape_xxxx.csv, it is the partition file for multi-rate senario. The other one named as mr_xxxx.csv is the partition file for multi-resolution senario.



## Csv file process:
 
We have wrote two python files, csv_process_multi_rate.py and csv_process_multi_reso.py respectively for multi-rate and multi-reso.
  
Call script csv_process_multi_rate.py as follows: 

```
python csv_process_multi_rate.py -w <width_frame> -h <height_frame> -f <number_frames> -p <path_CUshape_files> --ctu_size <ctu size>
```
 
It is worthmentioning the size of CTU differs between various coding presets for VVenc. 
  
Call script csv_process_multi_reso.py as follows: 

``` 
python csv_process_multi_reso.py -w <width_frame> -h <height_frame> -f <number_frames> -p <path_mr_files> --ctu_size <ctu size> -m <scale_multi_reso>
```
 
The option -m here corresponds the same value as --mr in the previous step. 
 
The processing by script will generate two csv files: ShapeMap_xxxx.csv and Mr_part_xxxx.csv respectively for multi-rate and multi-reso. 




## Load csv files for acceleration: 
 
 
1. Set values of macros correctly for Dep multi-rate and Dep multi-reso encodings.
 
2. Build the encoder and call it as follows:



For multi-rate case:

```
./vvencFFapp -c <path to config file> --InputFile <path_to_yuv> -s widthxheight -fr <framerate> -f <number_frame_to_code> -q <qp> --NumPasses 1 -qpa 1 -t 1 -b <output_bin_file> --mr_path <location_output_partition> --mr_metric <choose_max_or_min> --mr_qp <QP_value_ref_encoding>  > output_text_file
```
 
For example:

```
./vvencFFapp -c C:\Desktop\VVenc_multiprofile_coding\cfg\randomaccess_medium.cfg --InputFile  E:\JVET_CTC\RaceHorses_832x480p_30Hz_iyuv.yuv -s 832x480 -fr 30 -f 16 -q 22 --NumPasses 1 -qpa 1 -t 1 -b C:\output\out.bin  --mr_path "C:\mr_folder" --mr_metric max --mr_qp 37  > C:\output\mr_qp37_RaceHorses_832x480p_30Hz_iyuv_qp_22.txt
```



For multi-reso case:

```
./vvencFFapp -c <path to config file> --InputFile <path_to_yuv> -s widthxheight -fr <framerate> -f <number_frame_to_code> -q <qp> --NumPasses 1 -qpa 1 -t 1 -b <output_bin_file> --mr_path <location_output_partition> --mr_width <frame_width_ref_encoding> --mr_height <frame_height_ref_encoding>  > output_text_file
```

For example:

```
./vvencFFapp -c C:\Desktop\VVenc_multiprofile_coding\cfg\randomaccess_medium.cfg --InputFile  E:\JVET_CTC\RaceHorses_832x480p_30Hz_iyuv.yuv -s 832x480 -fr 30 -f 16 -q 22 --NumPasses 1 -qpa 1 -t 1 -b C:\output\out.bin  --mr_path "C:\mr_folder" --mr_width 416 --mr_height 240  > C:\output\mr_2_RaceHorses_832x480p_30Hz_iyuv_qp_22.txt
```



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

**The main repository has moved to: https://gitlab.tugraz.at/ibi/mrirecon/miscellaneous/bloch-moba-misc**

**Please check there for updates.**


# Quantitative Multi-Parameter Mapping in Magnetic Resonance Imaging

This repository includes the scripts to create the Figures for chapter 5 of

> #### Quantitative Multi-Parameter Mapping in Magnetic Resonance Imaging
> Scholand, N. Doctoral thesis, 2023.
> [doi: 10.53846/goediss-10028](http://dx.doi.org/10.53846/goediss-10028)

The scripts for the figures of chapter 4 can be found on [Github](https://github.com/mrirecon/bloch-moba).

## Requirements
This repository has been tested on Debian 11, but is assumed to work on other Linux-based operating systems, too.

### Reconstruction
Pre-processing, reconstruction and post-processing is performed with the [BART toolbox](https://github.com/mrirecon/bart).
The provided scripts are compatible with commit `f1192bc` or later.
If you experience any compatibility problems with later BART versions please contact us!

[//]: <> (FIXME: Add DOI for BART version including the Bloch model-based reconstruction)

For running the reconstructions access to a GPU is recommended.
If the CPU should be used, please remove `-g` flags from `bart moba ...`, `bart pics ...` and `bart rtnlinv ...` calls.

### Visualization
The visualizations have been tested with Python on version 3.9.2 and require numpy, copy, matplotlib, mpl_toolkits, sys, os, math, time, and scipy. Ensure to have set a DISPLAY variable, when the results should be visualized.

## Data
The data is hosted on [ZENODO](https://zenodo.org/) and must be downloaded first.

* Manual download: https://zenodo.org/record/7837312
* Download via script: Run the download script in the `./data` folder.
  * **All** files: `bash load-all.sh`
  * **Individual** files: `bash load.sh 7654462 <FILENAME> . ` or `bash load.sh 6992763 <FILENAME> . ` for the scripts in the folder `init_test`

Note: The data must be stored in the `./data` folder!


## Folders
Each folder contains a README file explaining how the figure can be reproduced.


[//]: <> (FIXME: Add Runtime!)

## Feedback
Please feel free to send us feedback about this scripts!
We would be happy to learn how to improve this and future script publications.


## License
This work is licensed under a **Creative Commons Attribution 4.0 International License**.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.

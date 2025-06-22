# README

## Overview

Due to the urgency of the current development schedule, no exhaustive comments are added to the source code except for necessary notes in key locations. It is planned to gradually refine the comments in subsequent development to improve the readability of the code.

In addition, this project is mainly focused on the development of graphical user interfaces (GUI), so no test code is included at this time. In a future release, a comprehensive test suite will be introduced to ensure the stability and reliability of the project.

The project uses a relatively simple MVC (Model-View-Controller) structure. It is planned to continuously optimize the MVC structure by adding API interfaces and optimizing communication between modules.

As my first standalone project, the code quality may leave much to be desired.

Thank you for your understanding and support! Your feedback and suggestions will be my motivation to keep improving.

## Core Components & Features

- **MVC Pattern**: The project follows the MVC (Model-View-Controller) architecture, which implements loose coupling between modules, and improves the maintainability and extensibility of the code.
- **Core Methods**: The model/config_loader.py module contains a number of key methods, such as `get_text`, `get_image`, `get_key`, and `get_tip`, etc., which provide necessary data support for the operation of the project.

## Running Instructions

The following is an example command:

```shell
> git clone https://github.com/pyheight/ttk-file-explorer.git
> cd ttk-file-explorer/src
> pip install -r requirements.txt
> python main.py
> python script/package.py
```

## Icon Source  
  
All icons used in this project are from [Icons8](https://icons8.com/). 

This project would like to express our heartfelt gratitude to Icons8 for providing high-quality icon resources.

## License  
  
This project is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). 
  
This means that you are free to use, modify, distribute, and sublicense the project, subject to the Apache License.

THE DETAILED TERMS AND CONDITIONS OF THE LICENSE CAN BE FOUND IN THE `LICENSE` FILE IN THE PROJECT. At the same time, a brief description of the license is included in the `main.py` document.

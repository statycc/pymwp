# pymwp

Implementation of MWP analysis on C code in Python.


### How to run the analysis

1. Clone the repository

    ```bash
    git clone https://github.com/seiller/pymwp.git
    ``` 

2. Set up Python environment

    install required packages

    ```bash
    pip install -q -r requirements.txt
    ``` 

3. Run the analysis

    From project root run:
    
    ```bash
    python -m pymwp path/to/c/file
    ```

    for example:
    
    ```bash
    python -m pymwp c_files/infinite_2.c
    ```
    
    to see all available options see help
    
    ```bash
    python -m pymwp
    ```
    
    Earlier version of analysis can be called by replacing `-m pymwp` with 
    `Analysis.py`.
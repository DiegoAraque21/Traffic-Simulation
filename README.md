# Traffic Simulation

## Manual de Instalación

#### Repository

Press the code button and copy the htttps link

- Enter a terminal and clone the repository with the following command:

- git clone link-copied

#### Packages

To run this project you will need miniconda or anaconda, and we are using version 3.8 of python. Also to run the simulation on unity it's necessary to have version 2021.3.12f1 installed.

For everything to work accordingly, and if you met the requirements above you will need to follow this steps:

- Create a virtual environment: conda create --name traffic-sim python=3.8
- After creating your environment, activated from the terminal: conda activate traffic-sim
- At the moment we have the virtual environment, we just need to intall flask and mesa now
- Flask: pip install flask
- Mesa: pip install mesa

After installing everything you are ready to run the simulation

#### Run the simulation

If you are in the parent folder, redirect yourself to the folder 2D_SImulation with the following command: cd 2D_SImulation

When you are in this new folder just run python server.py to run the server flask for it to work in unity. Or run server_2D.py, to run the simulation on html and in 2D.

If you decided to run the flask server, you will need to open the unity project and play the scene called BuildCity

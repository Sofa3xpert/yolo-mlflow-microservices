# UPD.: Obsolete, non-scalable version

This project allows you to run a YOLOv5 model for image classification.

## Weights folder

    yolov5s.pt # old or 'big' weigths

Added new version of weights for more efficient performance and time execution
    
    yolov5n.pt #smaller version
Transfer any custom or newest weights in this folder

## main.py 

Responsible for FastAPI setup, including '/status', '/version', '/predict'.
Includes MLFlow integration

## MLFLow integration
Before running MLFLow, uncomment related parts of the code
To run MLFLow in terminal do:

    mlflow ui

Then in another window type, to reload the page and proceed to the url

    uvicorn main:app --reload

## config.yaml

Added .yaml file for robust and flexible connection between MLFlow and FastAPI

## cat.jpeg 

Testing image

##


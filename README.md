# Accumulator

Calculate accumulating parameters in a given agricultural season at Oklahoma Mesonet sites.  

The application currently calculates Chill Hours for each station, and resulting data are stored in NetCDF format via an EFS mount. This application could
potentially expand to include other accumulation models such as Grape Black Rot or Peanut Leaf Spot. The intention is 
for this model to run in AWS Lambda on an hourly schedule and store the resulting data in a NetCDF4 dataset via EFS.

## Environment Variables

```
ACCUM_DATASET_PATH=<path to NetCDF4 dataset mounted via EFS>
DATASERVER_HOST=<private IP address of DataServer EC2 instance>
DATASERVER_PORT=<default for DataServer is 10000>
```
Currently, _**lambda_execution_role_dev**_ permissions will not allow connecting to DataServer via the public IP address, therefore the private IP address of its EC2 instance is required for the DATASERVER_HOST.

## Building
AWS Lambda requires containers to be built using **amd64** architecture and to have the **Lambda Runtime Environment** installed inside the container. To initialize the function inside the container, set the location of the Lambda Runtime Environment as the **ENTRYPOINT** in your Dockerfile, and the function handler as the **CMD**. The function handler must take two arguments, _**event**_ and _**context**_. The _**event**_ is a json object that triggers the function, and the _**context**_ "provides methods and properties that provide information about the invocation, function, and execution environment"([per the AWS docs](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html)).

After building, the image must be tagged and pushed to ECR. From ECR, Lambda can pull the image and use it in a function. The application requires access to DataServer for pulling data from various Mesonet datasets and EFS for storing the Accumulator dataset.

Command for building amd64 image:
```bash
docker buildx build --platform linux/amd64 -t sysdev/pyaccumulator .
```

This repo synced from the following GitHub repo:
https://github.com/AdamSlay/Accumulator

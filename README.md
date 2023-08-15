# Accumulator

This is a simple application designed to be run on a schedule and calculate the total Chill Hours accumulated in a given season. 
The model used is the Utah Model (Richardson et al. 1974) and resulting data are stored in NetCDF format. This application could
potentially expand to include other accumulation models for other crops such as Grape Black Rot or Peanut Leaf Spot. The intention is 
for this model to run in AWS Fargate on a schedule and store the resulting data via EFS.
# Panthera_interview_gcm
This repo contains the code and static data used to create a [COVID-19 dashboard for South Africa](http://3.140.191.119:8050).
This was done as part of the interviewing process at Panthera.

### Data source
The Dynamic data for this project is sourced from the [Data Science for Social Impact Research Group](https://github.com/dsfsi/covid19za/tree/master/data).
A lot of insipiration was also taken from their own [dashboard](https://datastudio.google.com/u/0/reporting/1b60bdc7-bec7-44c9-ba29-be0e043d8534/page/hrUIB).
The static data was obtained from [Stats SA](http://www.statssa.gov.za/).

### Notable statistics
On this dashboard we display multiple statistics that describe COVID-19.
The aim of the dashboard is to aid in travel decision making when travelling within South Africa.

### How to use the dashboard
[UPDATE] To run it locally [download the COVID_RSA.rar file.](https://github.com/ChristopherMarais/Panthera_interview_gcm/blob/main/COVID_RSA.rar) unzip it and follow the instructions in the READM.txt file.

A statistic to view is selected from the buttons above each plot. Further selection of what data to view can be done by clicking and double-clicking on the legend of each plot. This may help with singling out specific lines in the line charts. To overcome the current bug with the mobility line graphs you have to drag a window over the section of the plot that contains the data. This way the data will be fitted to the plot. Just remember that double-clicking on the plot will reset it to the normal zoom level. The plots could also be manipulated and then saved as images locally for offline use. Alternatively the dashboard can also be accessed as a docker image to be run locally by pulling the image from [Docker Hub](https://hub.docker.com/r/gcmarais/panthera_interview). This is done with the following command: "docker pull gcmarais/panthera_interview"

#### Notable statistics on the dashboard map:
* Please note that all displays on the dashboard map currently only display information as a summary of the past week (7 days). This data is also dependent on how often the data is updated by the [Data Science for Social Impact Research Group](https://github.com/dsfsi/covid19za/tree/master/data).
- Infection Probability Estimate (IPE) = An estimate of how likely one is to contract COVID-19. This is a very rough estimate that is based on the number of infections per square kilometer, the mean public mobility of people, and the rate of change in cumulative cases.
- Number of Active cases = The estimated number of people that actively have COVID-19 that ahve not yet recovered or passed away.
- Citizen mobility = This is a score based on google mobility data that indicates how much people move relative to what was considered normal. A score of 0.5 on this dashboard is considered normal. Higher than 0.5 is above normal movement and below 0.5 is below normal movement.
- Infections per square kilometer = This is a statisitic that summarizes how many people are infected in a certain area. The idea is to incorporate popualtion density in the equation when investigating COVID cases.

#### Notable statistics in dashboard table:
- Current active carriers = National estimate of active COVID cases
- Current Estimated Slope of Carrier Growth = The rate at which cases increased in the past 7 days nationally

#### Notable statistics in dashboard line graphs:
* Please note that we are aware of th bug that makes the mobility plot containing line graphs be compressed to the one side. Please refer to the *How to use the dashboard* section to manually adjust the view of the plot.
- Mobility lines all show the mobility of people as estimated by Google on how much people moved to places relative to what was normal before COVID. The places are categorized into Retail and Recreation, Grocery and Pharmacy, Parks, Transit stations, Workplaces, Residential. Refer to [their page](https://www.google.com/covid19/mobility/) for further explanations.
- The deaths, recoveries and cases data of COVID are shown as line graphs with the cumulative data normalized to the population size of each province.

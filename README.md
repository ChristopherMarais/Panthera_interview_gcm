# Panthera_interview_gcm
This repo contains the code and static data used to create a [COVID-19 dashboard for South Africa]().
This was done as part of the interviewing process at Panthera.

### Data source
The Dynamic data for this project is sourced from the [Data Science for Social Impact Research Group](https://github.com/dsfsi/covid19za/tree/master/data).
A lot of insipiration was also taken from their own [dashboard](https://datastudio.google.com/u/0/reporting/1b60bdc7-bec7-44c9-ba29-be0e043d8534/page/hrUIB).
The static data was obtained from [Stats SA](http://www.statssa.gov.za/).

### Notable statistics
On this dashboard we display multiple statistics that describe COVID-19.
The aim of the dashboard is to aid in travel decision making when travelling within South Africa.

#### Notable statistics on the dashboard map:
- Infection Probability Estimate (IPE) = An estimate of how likely one is to contract COVID-19. This is a very rough estimate that is based on the number of infections per square kilometer, the mean public mobility of people, and the rate of change in cumulative cases.
- Number of Active cases = The estimated number of people that actively have COVID-19 that ahve not yet recovered or passed away.
- Citizen mobility = This is a score based on google mobility data that indicates how much people move relative to what was considered normal. A score of 0.5 on this dashboard is considered normal. hanger than 0.5 is above normal movement and below 0.5 is below normal movement.
- Infections per square kilometer = This is a statisitic that summarizes how many people are infected in a certain area. The idea is to incorporate popualtion density in the equation when investigating COVID cases.

* Please note that all displays on the dashboard map currently only display information as a summary of the past week (7 days). This data is also dependent on how often the data is updated by the [Data Science for Social Impact Research Group](https://github.com/dsfsi/covid19za/tree/master/data).

#### Notable statistics in dashboard table:
- 

# Aviation Accident Analysis

This project analyzed U.S. aviation accidents from 1948 to 2023 on behalf of an aircraft and airline insurer. The goal was to identify aircraft types and conditions most likely to result in total losses of the aircraft and of passengers. The following sections describe the data preparation and the analysis, with results for the most recent 40 years (1983 to 2023) assuming a typical aircraft lifetime of 40 years.

---

## **Directory Structure**

```
├── AviationData.csv                          # Raw NTSB accident data, available from 1983 on
├── USState_Codes.csv                         # Reference for US State codes used in NTSB data
├── Aviation_Accidents_Cleaning.ipynb         # Data loading, filtering, and cleaning
├── Aviation_Accidents_Data_Analysis.ipynb    # EDA, statistics, and visualizations
├── data/
│   └── aviation_accidents_cleaned.csv        # Cleaned dataset, output of cleaning script
└── images/                                   # Key visualizations
```

---

## **Methodology**

- **Timeframe:** Filtered to accidents from 1983 onward (40-year assumed aircraft lifetime) and non-amateur-built aircraft, reflecting those that could be in service today.

- **Passenger Risk:** Computed estimated total passengers per flight using the fatal, serious, minor and uninjured passenger counts that NTSB reports for each accident. Used fraction of passengers suffering serious or fatal injuries as our proxy for risk to humans.

- **Airframe Loss:** Used the `Aircraft.damage` data element to derive a `destroyed = (true|false)` flag as our proxy for total loss of the airframe.

- **Data Cleaning:** Cleaned the aircraft Make and Model fields, including normalizing spaces and capitalization, and combining several variants known to be of the same aircraft (e.g., Cessna 150 vs. 150).

- **Aircraft Grouping:** Constructed a `Plane.Type` field by joining Make with Model, since Model name alone is not unique, for grouping and filtering of results.

- **Aircraft Size:** Split aircraft by size, where Small < 20 passengers and Large >= 20, to fulfill the customer request to separate commercial from general aircraft.

- **Statistical Significance:** Only compared groups that had 10 to 15+ total recorded accidents, to yield statistically significant results on the sample.

---

## **Results and Recommendations**

### **Aircraft Makes with the Lowest Passenger Injury and Airframe Destruction Rates**

**Large Aircraft:** The McDonnell Douglas, Bombardier and Boeing makes have the lowest injury rates, all below 14% and each with 22+ recorded accidents.

**Small Aircraft:** The Luscombe, Grumman Acft Eng Cor-Schweizer and Stinson makes have the lowest airframe destruction rates, all below 2.5% and each with 58+ recorded accidents.

---

### **Aircraft Models with the Lowest Passenger Injury and Airframe Destruction Rates**

**Large Aircraft:** The Boeing 777, 757 and 787 models stand out as having near-zero injury rates across a large number of recorded accidents.

**Small Aircraft:** Among the 12 safest make-model combinations (only makes of which all four smallest aircraft have 10+ accidents), three make-model pairs have low injury rates and are based on a sufficiently large number of accidents to yield statistically-significant conclusions.

---

### **Operating Conditions Most Associated With Accident Severity**

**Weather Conditions:** IMC (i.e., "Instrument" flight conditions, meaning poor visibility conditions and requiring instrument flying proficiency to avoid accidents) have the highest severity, with a mean of 63% of passengers receiving serious or fatal injuries, and 35% of aircraft destroyed. VMC (i.e., Visual Meteorological Conditions, meaning good weather with adequate visibility), has 23% of passengers receiving serious or fatal injuries, and 7% of aircraft destroyed.

**Engine Type:** Engine type also correlates with higher injury rates. Aircraft powered by turbofan engines have the lowest mean rates of injuries (9%) and destruction (5%). Reciprocating and turboprop engine types, which typically have smaller passenger capacities than turbofans, have notably higher rates of injuries (25 to 32%) and aircraft destruction (8 to 18%).

---

## **Conclusions and Recommendations**

- **Large Aircraft Selection:** If an airline is choosing among large aircraft types with a 40-year lifetime and has sufficient accidents recorded for each aircraft to make a statistically meaningful recommendation, the best safety record by injury rate would be McDonnell Douglas and Boeing 777/757/787 models, which have near-zero serious/fatal injury rates across their lifetimes.

- **Small Aircraft Selection:** Of the aircraft types that have sufficiently many accidents recorded to yield statistically meaningful conclusions, of those with the smallest total number of fatalities, the safest are the Luscombe, Grumman Acft Eng Cor-Schweizer and Stinson aircraft with respect to airframe destruction, which is the most relevant criterion to most insurers.

- **Non-Aircraft Factors:** Regardless of whether the operator chooses large or small, commercial or general aircraft, weather and engine type appear as the two most significant non-aircraft factors most likely to be associated with accident severity. Therefore, weather conditions and engine types should have significant influence on any insurance risk model for flight, along with the make and model.

---

## **Notes / Reproducibility**

1. Run the `Aviation_Accidents_Cleaning.ipynb` from top to bottom to produce the cleaned data file: `data/aviation_accidents_cleaned.csv`.

2. Run the `Aviation_Accidents_Data_Analysis.ipynb` from top to bottom to reproduce all of the above results and visualizations.

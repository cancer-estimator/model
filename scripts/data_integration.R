#### BEGIN: PACKAGE + INSTALLING HANDLING
# Package names
packages <- c("readr", "dplyr", "tidyr")


# Install packages not yet installed
installed_packages <- packages %in% rownames(installed.packages())
if (any(installed_packages == FALSE)) {
    install.packages(packages[!installed_packages])
}

# Packages loading
invisible(lapply(packages, library, character.only = TRUE))
#### END: PACKAGE + INSTALLING HANDLING

hsearch= function (string, t1,t2,t3){
    paste("1.", grep(string,c(names(t1)),value=TRUE),
          "2.", grep(string,c(names(t2)),value=TRUE),
          "3.",  grep(string,c(names(t3)),value=TRUE),sep="   ")
}



ds1 <- read_csv("datasets/lung-cancer/survey_lung_cancer.csv")
ds2 <- read_csv("datasets/lung-cancer/cancer_patient_data_sets.csv")
ds3 <- read_csv("datasets/lung-cancer/covid_dataset.csv")
#### Padronizacao basica dos datasets

names(ds2)=toupper(names(ds2)) #headers com nome maisculo
names(ds3)=toupper(names(ds3)) #headers com nome maisculo

ds1$source=1
ds2$source=2
ds3$source=3

set.seed(666)
ds1[3:15]=ds1[3:15]-1
ds2[5:25]=ifelse(ds2[5:25]>3,1,0)
names(ds3)=gsub("[-+ ]","_",names(ds3))
names(ds2)=gsub("[-+ ]","_",names(ds2))
names(ds1)=gsub("[-+ ]","_",names(ds1))

ds1$LUNG_CANCER <- ifelse(ds1$LUNG_CANCER == "YES", 1, 0)


  ##### features

  ######## 1 AGE_0_9, AGE_10_19, AGE_20_24, AGE_25_59, AGE_60_
  ds2$AGE_0_9 <- as.numeric(ds2$AGE <= 9)
  ds2$AGE_10_19 <- as.numeric(ds2$AGE >= 10 & ds2$AGE <= 19)
  ds2$AGE_20_24 <- as.numeric(ds2$AGE >= 20 & ds2$AGE <= 24)
  ds2$AGE_25_59 <- as.numeric(ds2$AGE >= 25 & ds2$AGE <= 59)
  ds2$AGE_60_ <- as.numeric(ds2$AGE >= 60)
  ds1$AGE_0_9 <- as.numeric(ds1$AGE <= 9)
  ds1$AGE_10_19 <- as.numeric(ds1$AGE >= 10 & ds1$AGE <= 19)
  ds1$AGE_20_24 <- as.numeric(ds1$AGE >= 20 & ds1$AGE <= 24)
  ds1$AGE_25_59 <- as.numeric(ds1$AGE >= 25 & ds1$AGE <= 59)
  ds1$AGE_60_ <- as.numeric(ds1$AGE >= 60)

  ######## 2 GENDER_FEMALE, GENDER_MALE
  ds1$GENDER_FEMALE<- as.numeric(ds1$GENDER =="F")
  ds1$GENDER_MALE<- as.numeric(ds1$GENDER =="M")
  ds1=ds1 %>% select(-GENDER)
  ds2$GENDER_FEMALE<- as.numeric(ds2$GENDER ==2)
  ds2$GENDER_MALE<- as.numeric(ds2$GENDER ==1)
  ds2=ds2 %>% select(-GENDER)


  ######## 3 SMOKING


ds3$SMOKING=NA
#As of 2022, the WHO estimated that around 20% of the global population aged 15
#and over were smokers.

 ######## 4 FATIGUE
hsearch("FATIGUE",ds1,ds2,ds3)
names(ds3)[which(names(ds3)=="TIREDNESS")]="FATIGUE"


 ######## 5 DIFFICULTY_IN_BREATHING
hsearch("BREATH",ds1,ds2,ds3)
names(ds3)[which(names(ds3)=="DIFFICULTY_IN_BREATHING")]="SHORTNESS_OF_BREATH"

######## 6 SWALLOWING_DIFFICULTY (SORE_THROAT)
hsearch("THROAT",ds1,ds2,ds3)
hsearch("SWALLOWING",ds1,ds2,ds3)

names(ds3)[which(names(ds3)=="SORE_THROAT")]="SWALLOWING_DIFFICULTY"

######## 7 CHEST_PAIN
hsearch("CHEST",ds1,ds2,ds3)
ds3$CHEST_PAIN=as.numeric(ds3$PAINS & ds3$NASAL_CONGESTION)


######## 8 COUGHING (In the case couch with blood score 2, var assumes 0,1,5,10)
hsearch("COUGH",ds1,ds2,ds3)
names(ds3)[which(names(ds3)=="DRY_COUGH")]="COUGHING"
ds2$COUGHING=(ds2$COUGHING_OF_BLOOD+ds2$DRY_COUGH)*5

################  ARTIFICIAL #######################################

##### 9 COLD_SYMPTOMNS
ds1$COLD_SYMPTOMNS=ds1$FATIGUE+ds1$SHORTNESS_OF_BREATH+ds1$SWALLOWING_DIFFICULTY+ds1$WHEEZING
ds2$COLD_SYMPTOMNS=ds2$DUST_ALLERGY+ds2$WHEEZING+ds2$DRY_COUGH+ds2$FREQUENT_COLD
ds3$COLD_SYMPTOMNS=ds3$NASAL_CONGESTION+ds3$RUNNY_NOSE+ds3$COUGHING+ds3$FATIGUE



##### 10 RESPIRATORY_SYMPTOMNS

ds1$RESPIRATORY_SYMPTOMNS=ds1$SMOKING+ds1$YELLOW_FINGERS+ds1$COUGHING+
  ds1$SHORTNESS_OF_BREATH+ds1$SWALLOWING_DIFFICULTY

ds2$RESPIRATORY_SYMPTOMNS=ds2$DRY_COUGH+3*ds2$COUGHING_OF_BLOOD+ds2$FREQUENT_COLD

ds3$RESPIRATORY_SYMPTOMNS=ds3$NASAL_CONGESTION+ds3$COUGHING+
2*ds3$SHORTNESS_OF_BREATH+ds3$RUNNY_NOSE

##### 11 OTHER_SYMPTOMS
ds1$OTHER_SYMPTOMS=ds1$ANXIETY+ds1$CHRONIC_DISEASE+ds1$ALCOHOL_CONSUMING
ds2$OTHER_SYMPTOMS=ds2$SNORING+2*ds2$OBESITY+ds2$DUST_ALLERGY-ds2$BALANCED_DIET
ds3$OTHER_SYMPTOMS=2*ds3$FEVER+ds3$DIARRHEA

##### 12 SNORING
hsearch("SNORING",ds1,ds2,ds3)
ds3$SNORING=as.numeric(ds3$SHORTNESS_OF_BREATH & ds3$NASAL_CONGESTION)
ds1$SNORING=as.numeric(ds1$FATIGUE &ds1$SHORTNESS_OF_BREATH)


####### 13  SEVERITY (LIFE RISK)

ds3$SEVERITY=1*ds3$SEVERITY_MILD+
              2*ds3$SEVERITY_MODERATE+
               4*ds3$SEVERITY_SEVERE

ds2$SEVERITY=ds2$GENETIC_RISK+ds2$CHRONIC_LUNG_DISEASE+3*ds2$COUGHING_OF_BLOOD+ds2$CLUBBING_OF_FINGER_NAILS

ds1$SEVERITY=4*ds1$YELLOW_FINGERS+ds1$CHRONIC_DISEASE+ds1$ALCOHOL_CONSUMING


##### 14 POLUTION (to be implemented)


##### 15 YELLOW_FINGER
hsearch("YELLOW",ds1,ds2,ds3)
hsearch("FINGER",ds1,ds2,ds3)
names(ds2)[which(names(ds2)=="CLUBBING_OF_FINGER_NAILS")]="YELLOW_FINGERS"

#### 16 TARGET: LUNG_CANCER
hsearch("CANCER",ds1,ds2,ds3)
ds2$LUNG_CANCER=ifelse(ds2$LEVEL=="High",1,0)
ds3$LUNG_CANCER=NA
  #he chance that a man will develop lung cancer in his lifetime is about 1 in 16;
  #for a woman, the risk is about 1 in 17.
#### 16  ASYMPTOMATIC( to be implemented)


df=bind_rows(ds1,ds2)
df=bind_rows(df,ds3)

names(df)[which(names(df)=="LUNG_CANCER")]="LUNG_CANCER_RISK"
df=df %>% select(-LEVEL,-CONTACT_NO, -CONTACT_YES,-INDEX, -PATIENT_ID)

write.csv(df,"datasets/lung-cancer/dataset_integrated.csv",na="", row.names=F)

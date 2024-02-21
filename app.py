#Importing Libraries
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_dynamic_filters import DynamicFilters
from streamlit_extras.stylable_container import stylable_container
#Call the functions for the Vis
from Deiktes_Ygeias_app_Functions import *

def main():
  #######################################################################################################################################################################
  #######################################################################################################################################################################

  #Σετάρισμα Σελίδας:
  st.set_page_config(
          page_title="Δείκτες Υγείας",
          page_icon="chart_with_upwards_trend",
          layout="wide",
          initial_sidebar_state="expanded"
      )
  
  role=get_url_params()
  st.write(role)
  #######################################################################################################################################################################
  #######################################################################################################################################################################

  #Read the data:
  # Export from vidavo:
  df=pd.read_excel("C:\\Users\\Vagelis\\Desktop\\str_app\\test_for_cat_creations.xlsx")
  #st.write(df)

  # Lista Ergazomenwn:
  lista_erg=pd.read_excel("C:\\Users\\Vagelis\\Desktop\\str_app\\lista_ergazomenwn.xlsx")
  #st.write(lista_erg)

  #Merging df with lista ergazomenwn
  df=df.merge(lista_erg,on="id_ergazomenou",how="left")
  #st.write(df)

  ###################################################################################################################################################
  ###################################################################################################################################################

  #Calculation of "Hlikiakes klaseis - Eti Ekthesis" in Categorical Format:

  #Ηλικιακές Κλάσεις
  df["age_group"]=np.where((df["patient_age"]>=18)&(df["patient_age"]<=34),"18-34",np.where((df["patient_age"]>=35)&(df["patient_age"]<=44),"35-44",np.where((df["patient_age"]>=45)&(df["patient_age"]<=54),"45-54",np.where((df["patient_age"]>=55)&(df["patient_age"]<=64),"55-64",np.where(df["patient_age"]>=65,"65+",np.where(df["patient_age"].isna(),np.nan,np.nan))))))
  #Έτη έκθεσης
  #ΠΡΟΣΟΧΗ: Τώρα βάζω τυχαία την στήλη date να αλλαχτεί με την σωστή όταν θα έχω την λίστα εργαζομένων:
  df["hmeromhnia_enarksis_trexousas_thesis"] = pd.to_datetime(df["hmeromhnia_enarksis_trexousas_thesis"])
  df["ekthesi(years)"] = (pd.to_datetime("today") - df["hmeromhnia_enarksis_trexousas_thesis"]).astype("<m8[Y]")
  #df["ekthesi(years)"]=df["ekthesi(years)"].astype(int)
  #Έτη έκθεσης σε κλάσεις
  df["eth_ekthesis"]=np.where(df["ekthesi(years)"]<1,"<1 έτος",np.where((df["ekthesi(years)"]>=1)&(df["ekthesi(years)"]<=2),"1-2 έτη",np.where((df["ekthesi(years)"]>2)&(df["ekthesi(years)"]<=5),"3-5 έτη",np.where((df["ekthesi(years)"]>5)&(df["ekthesi(years)"]<=10),"6-10 έτη",np.where((df["ekthesi(years)"]>10)&(df["ekthesi(years)"]<=15),"11-15 έτη",np.where(df["ekthesi(years)"]>15,">15 έτη",np.where(df["ekthesi(years)"].isna(),np.nan,np.nan)))))))

  ###################################################################################################################################################
  ###################################################################################################################################################

  #Calculation of "Ergasthriakoi Deiktes" in Categorical Format:

  #Αρτηριακή Πίεση - Συστολική
  df["systoliki_piesi_CAT"]=np.where(df["systoliki_piesi"]>140,"ΑΡΤΗΡΙΑΚΗ ΥΠΕΡΤΑΣΗ",np.where(df["systoliki_piesi"].isna(),np.nan,"ΦΥΣΙΟΛΟΓΙΚΗ"))
  #Αρτηριακή Πίεση - Διαστολική
  df["diastoliki_piesi_CAT"]=np.where(df["diastoliki_piesi"]>90,"ΑΡΤΗΡΙΑΚΗ ΥΠΕΡΤΑΣΗ",np.where(df["diastoliki_piesi"].isna(),np.nan,"ΦΥΣΙΟΛΟΓΙΚΗ"))
  #Αιματοκρίτης (HT%)
  df["ht_aimatokritis_CAT"]=np.where(((df["gender"]=="man") & ((df["ht_aimatokritis"]>=40)&(df["ht_aimatokritis"]<=54))),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(((df["gender"]=="woman") & ((df["ht_aimatokritis"]>=36)&(df["ht_aimatokritis"]<=48))),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["ht_aimatokritis"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ")))
  #Αιμοσφαιρίνη (Hb)
  df["hb_aimosfairini_CAT"]=np.where(((df["gender"]=="man") & ((df["hb_aimosfairini"]>=13.5)&(df["hb_aimosfairini"]<=15.5))),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(((df["gender"]=="woman") & ((df["hb_aimosfairini"]>=11.5)&(df["hb_aimosfairini"]<=15.5))),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["hb_aimosfairini"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ")))
  #Αιμοπετάλια (PLT)
  df["plt_aimopetalia_CAT"]=np.where((df["plt_aimopetalia"]>=150)&(df["plt_aimopetalia"]<=400) ,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["plt_aimopetalia"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Λευκά Αιμοσφαίρια (WBC)
  df["wbc_leyka_aimosferia_CAT"]=np.where((df["wbc_leyka_aimosferia"]>=4)&(df["wbc_leyka_aimosferia"]<=11) ,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["wbc_leyka_aimosferia"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Γλυκοζυλιωμένη αιμοσφαιρίνη (HbA1c)
  df["glukoziliomeni_aimosferini_CAT"]=np.where(df["glukoziliomeni_aimosferini"]<=6.1 ,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["glukoziliomeni_aimosferini"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Ειδικό βάρος ούρων
  df["eidiko_baros_ouron_CAT"]=np.where((df["eidiko_baros_ouron"]>=1015)&(df["eidiko_baros_ouron"]<=1025) ,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["eidiko_baros_ouron"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Νιτρώδη
  df["nitrwdh_CAT"]=np.where(df["nitrwdh"]=="Αρνητικό" ,"ΑΡΝΗΤΙΚΟ",np.where(df["nitrwdh"]=="Θετικό","ΘΕΤΙΚΟ",np.nan))
  #Λέυκωμα ούρων
  df["leukvma_ouron_CAT"]=np.where(df["leukvma_ouron"]=="Αρνητικό" ,"ΑΡΝΗΤΙΚΟ",np.where(df["leukvma_ouron"]=="Θετικό","ΘΕΤΙΚΟ",np.nan))
  #Ερυθρά αιμοσφαίρια
  df["erithra_aimosferia_CAT"]=np.where((df["erithra_aimosferia"]>=0)&(df["erithra_aimosferia"]<=4) ,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["erithra_aimosferia"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Πυοσφαίρια
  df["puosfairia_CAT"]=np.where((df["puosfairia"]>=0)&(df["puosfairia"]<=4) ,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["puosfairia"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Γλυκόζη
  df["glukozi_CAT"]=np.where((df["glukozi"]>=74) & (df["glukozi"]<=106),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["glukozi"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ" ))
  #Χοληστερόλη υψηλής περιεκτικότητας λιποπρωτεινων(HDL-C)
  df["xolhsteroli_ipsilis_periektikotitas_CAT"]=np.where(df["xolhsteroli_ipsilis_periektikotitas"]<40,"ΧΑΜΗΛΗ",np.where((df["xolhsteroli_ipsilis_periektikotitas"]>=40)&(df["xolhsteroli_ipsilis_periektikotitas"]<=60),"ΕΠΙΘΥΜΗΤΗ",np.where(df["xolhsteroli_ipsilis_periektikotitas"].isna(),np.nan,"ΥΨΗΛΗ")))
  #Χοληστερόλη χαμηλής περιεκτικότητας λιποπρωτεινων(LDL-C)
  df["xolh_xamilis_periektikotitas_CAT"]=np.where(df["xolh_xamilis_periektikotitas"]<100,"ΙΔΑΝΙΚΗ",np.where((df["xolh_xamilis_periektikotitas"]>=100)&(df["xolh_xamilis_periektikotitas"]<=129),"ΣΧΕΔΟΝ ΙΔΑΝΙΚΗ",np.where((df["xolh_xamilis_periektikotitas"]>129)&(df["xolh_xamilis_periektikotitas"]<=159),"ΟΡΙΑΚΑ ΥΨΗΛΗ",np.where(df["xolh_xamilis_periektikotitas"].isna(),np.nan,"ΥΨΗΛΗ"))))
  #Ολική χοληστερόλη (TC)
  df["oliki_xolisteroli_CAT"]=np.where(df["oliki_xolisteroli"]<200,"ΕΠΙΘΥΜΗΤΗ",np.where((df["oliki_xolisteroli"]>=200)&(df["oliki_xolisteroli"]<=239),"ΟΡΙΑΚΑ ΥΨΗΛΗ",np.where(df["oliki_xolisteroli"].isna(),np.nan,"ΥΨΗΛΗ")))
  #Τριγλυκερίδια
  df["triglykeridia_CAT"]=np.where(df["triglykeridia"]<=150,"ΒΕΛΤΙΣΤΗ ΤΙΜΗ",np.where((df["triglykeridia"]>150) & (df["triglykeridia"]<=199),"ΟΡΙΑΚΑ ΥΨΗΛΗ",np.where((df["triglykeridia"]>199) & (df["triglykeridia"]<=499),"ΥΨΗΛΑ ΕΠΙΠΕΔΑ",np.where(df["triglykeridia"].isna(),np.nan,"ΠΟΛΥ ΥΨΗΛΑ ΕΠΙΠΕΔΑ"))))
  #Θυρεοειδοτρόπος ορμόνη(TSH)
  df["thuroeidotropos_ormoni_CAT"]=np.where((df["thuroeidotropos_ormoni"]>=0.35) & (df["thuroeidotropos_ormoni"]<=4.45),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["thuroeidotropos_ormoni"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ" ))
  #Ελεύθερη τριιωδοθυρονίνη(fT3)
  df["eleutheri_triiodothironini_CAT"]=np.where((df["eleutheri_triiodothironini"]>=3.5) & (df["eleutheri_triiodothironini"]<=6.5),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["eleutheri_triiodothironini"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ" ))
  #Ελεύθερη θυροξίνη (fT4)
  df["eleutheri_thuroksini_CAT"]=np.where((df["eleutheri_thuroksini"]>=10) & (df["eleutheri_thuroksini"]<=23),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["eleutheri_thuroksini"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Αντισώματα έναντι θυρεοειδικής υπεροξειδάσης (anti-TPO)
  df["antiswmata_anti_tpo_CAT"]=np.where(df["antiswmata_anti_tpo"]<60,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["antiswmata_anti_tpo"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Ουρία(Ur)
  df["ouria_CAT"]=np.where(df["ouria"]<=50,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["ouria"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Κρεατινίνη(Cr)
  df["kreatinh_CAT"]=np.where(df["kreatinh"]<=1.3,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["kreatinh"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Ασπαρτική αμινοτρανφεράση(AST/SGOT)
  df["aspartikh_aminotranferasi_CAT"]=np.where(df["aspartikh_aminotranferasi"]<=40,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["aspartikh_aminotranferasi"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Αμινοτρανσφεράση αλανίνης(ALT/SGPT)
  df["aminotranferasi_alaninis_CAT"]=np.where(df["aminotranferasi_alaninis"]<=35,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["aminotranferasi_alaninis"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #γ-Γλουταμυλοτρανφεράση (γ-GT)
  df["g_gloutamylotranferasi_CAT"]=np.where(df["g_gloutamylotranferasi"]<=61,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["g_gloutamylotranferasi"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Αλκαλική φωσφατάση(ALP)
  df["alkaliki_fosfatasi_CAT"]=np.where(df["alkaliki_fosfatasi"]<=129,"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where(df["alkaliki_fosfatasi"].isna(),np.nan,"ΠΑΘΟΛΟΓΙΚΗ"))
  #Αυστραλιανό αντιγόνο επιφανείας(HBsAg)
  df["hbsag_CAT"]=np.where(df["hbsag"]<1,"ΑΡΝΗΤΙΚΟ",np.where(df["hbsag"].isna(),np.nan,"ΘΕΤΙΚΟ"))
  #Ολικά αντισώματα ένταντι του Αυστραλιανού αντιγόνου (total anti-HBsAg)
  df["australiano_antigono_CAT"]=np.where(df["australiano_antigono"]<10,"ΑΡΝΗΤΙΚΟ",np.where(df["australiano_antigono"].isna(),np.nan,"ΕΠΑΡΚΕΙΑ ΕΜΒΟΛΙΑΣΤΙΚΗΣ ΚΑΛΥΨΗΣ"))
  #Ολικά αντισώματα ένταντι του πυρηνικού αντιγόνου HBV(total anti-HBc)
  df["olika_anti_hbv_CAT"]=np.where(df["olika_anti_hbv"]<1,"ΑΡΝΗΤΙΚΟ",np.where(df["olika_anti_hbv"].isna(),np.nan,"ΘΕΤΙΚΟ"))
  #Ολικά αντισώματα ένταντι του ιού της ηπατίτιδας Α (total anti-HAV)
  df["olika_anti_a_ipatitidas_CAT"]=np.where(df["olika_anti_a_ipatitidas"]<1,"ΑΡΝΗΤΙΚΟ",np.where(df["olika_anti_a_ipatitidas"].isna(),np.nan,"ΘΕΤΙΚΟ"))

  ####################################################################################################################################################
  ####################################################################################################################################################

  #Calculation of "Loipoi Deiktes" in Categorical Format:

  #Δείκτης μάζας/σώματος (BMI index)
  df["diktis_mazas_somatos_bmi_CAT"]=np.where(df["diktis_mazas_somatos_bmi"].isna(),np.nan,np.where(df["diktis_mazas_somatos_bmi"]<20,"ΛΙΠΟΒΑΡΕΙΣ",np.where((df["diktis_mazas_somatos_bmi"]>=20)&(df["diktis_mazas_somatos_bmi"]<25),"ΦΥΣΙΟΛΟΓΙΚΟΙ",np.where((df["diktis_mazas_somatos_bmi"]>=25)&(df["diktis_mazas_somatos_bmi"]<30),"ΥΠΕΡΒΑΡΟΙ",np.where(df["diktis_mazas_somatos_bmi"]>=30,"ΠΑΧΥΣΑΡΚΟΙ",np.nan)))))
  #Καπνιστικές Συνήθειες
  df["kapnistikes_synithies_devided_by_20_CAT"]=np.where(df["kapnistikes_synithies_devided_by_20"]<1,"ΜΗ ΚΑΠΝΙΣΤΗΣ",np.where((df["kapnistikes_synithies_devided_by_20"]>=1)&(df["kapnistikes_synithies_devided_by_20"]<=20),"ΗΠΙΟΣ ΚΑΠΝΙΣΤΗΣ",np.where((df["kapnistikes_synithies_devided_by_20"]>20)&(df["kapnistikes_synithies_devided_by_20"]<=40),"ΜΕΤΡΙΟΣ ΚΑΠΝΙΣΤΗΣ",np.where(df["kapnistikes_synithies_devided_by_20"]>40,"ΒΑΡΥΣ ΚΑΠΝΙΣΤΗΣ",np.where(df["kapnistikes_synithies_devided_by_20"].isna(),np.nan,np.nan)))))
  #Καρδιαγγειακός κίνδυνος
  df["kardiagiakos_kindynos_CAT"]=np.where(df["kardiagiakos_kindynos"]<1,"ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ",np.where((df["kardiagiakos_kindynos"]>=1)&(df["kardiagiakos_kindynos"]<5),"ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ",np.where((df["kardiagiakos_kindynos"]>=5)&(df["kardiagiakos_kindynos"]<10),"ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ",np.where(df["kardiagiakos_kindynos"]>=10,"ΠΟΛΥ ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ",np.where(df["kardiagiakos_kindynos"].isna(),np.nan,np.nan)))))
  #Ακοολογικός έλεγχος (Ακουόγραμα)
  df["akouograma_CAT"]=np.where((df["akouograma"]>=0)&(df["akouograma"]<=25),"ΦΥΣΙΟΛΟΓΙΚΗ ΑΚΟΗ",np.where((df["akouograma"]>25)&(df["akouograma"]<=55),"ΜΙΚΡΟΥ-ΜΕΤΡΙΟΥ ΒΑΘΜΟΥ ΒΑΡΗΚΟΙΑ",np.where((df["akouograma"]>55)&(df["akouograma"]<=90),"ΜΕΤΡΙΟΥ-ΣΟΒΑΡΟΥ ΒΑΘΜΟΥ ΒΑΡΗΚΟΙΑ",np.where(df["akouograma"]>90,"ΚΩΦΩΣΗ",np.where(df["akouograma"].isna(),np.nan,np.nan)))))
  #Λειτουργικός έλεγχος αναπνοής (σπιρομέτρηση)
  df["spirometrisi_CAT"]=np.where((df["spirometrisi_fvc"]>80)&(df["spirometrisi_fev1"]>80)&(df["spirometrisi_fev1_fvc"]>70),"ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ",np.where((df["spirometrisi_fvc"]>80)&(df["spirometrisi_fev1_fvc"]<70),"ΣΥΜΒΑΤΟ ΜΕ ΑΠΟΦΡΑΚΤΙΚΟ ΣΥΝΔΡΟΜΟ",np.where((df["spirometrisi_fvc"]<80)&(df["spirometrisi_fev1_fvc"]>70),"ΣΥΜΒΑΤΟ ΜΕ ΠΕΡΙΟΡΙΣΤΙΚΟ ΣΥΝΔΡΟΜΟ",np.nan)))
  #Nordic Muscoloskeletal Questionnaire (εκτίμηση μυοσκελετικών παθήσεων) score
  df["ektimisi_myoskeletikon_pathiseon_CAT"]=np.where(df["ektimisi_myoskeletikon_pathiseon"]==0,"ΧΩΡΙΣ MSDS",np.where((df["ektimisi_myoskeletikon_pathiseon"]>=1)&(df["ektimisi_myoskeletikon_pathiseon"]<=4),"ΗΠΙΟ-ΜΕΤΡΙΟ MSDS",np.where((df["ektimisi_myoskeletikon_pathiseon"]>4)&(df["ektimisi_myoskeletikon_pathiseon"]<=8),"ΣΟΒΑΡΟ MSDS",np.where((df["ektimisi_myoskeletikon_pathiseon"]>8)&(df["ektimisi_myoskeletikon_pathiseon"]<=16),"ΠΟΛΥ ΣΟΒΑΡΟ MSDS",np.where(df["ektimisi_myoskeletikon_pathiseon"].isna(),np.nan,np.nan)))))

  ######################################################################################################################################################
  ######################################################################################################################################################

  #Calculation of "Ergatika Atiximata" in Categorical Format:

  #Broadford factor (Β):
  df["broadford_factor_CAT"]=np.where(df["broadford_factor"]<50,"ΤΥΠΙΚΗ ΒΑΘΜΟΛΟΓΙΑ",np.where((df["broadford_factor"]>=50)&(df["broadford_factor"]<=100),"ΟΡΙΟ ΑΝΗΣΥΧΙΑΣ Ή ΠΑΡΑΚΟΛΟΥΘΗΣΗΣ",np.where((df["broadford_factor"]>100)&(df["broadford_factor"]<=200),"ΑΝΗΣΥΧΙΑ, ΣΤΕΝΟΤΕΡΗ ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΚΑΙ ΠΙΘΑΝΗ ΠΡΟΦΟΡΙΚΗ ΠΡΟΕΙΔΟΠΟΙΗΣΗ",np.where(df["broadford_factor"]>200,"ΑΠΑΙΤΟΥΝΤΑΙ ΠΕΡΑΙΤΕΡΩ ΕΝΕΡΓΕΙΕΣ",np.where(df["broadford_factor"].isna(),np.nan,np.nan)))))

  ######################################################################################################################################################
  ######################################################################################################################################################

  #Calculation of "Ergasiakh Ikanopoihsh / Agxos" in Categorical Format:

  #Εκτίμηση εργασιακής ικανοποίησης (Job Satisfaction Survey questionnaire)
  df["ektimisi_ergasiakis_ikanopioisis_CAT"]=np.where((df["ektimisi_ergasiakis_ikanopioisis"]>=36)&(df["ektimisi_ergasiakis_ikanopioisis"]<108),"ΔΥΣΑΡΕΣΚΕΙΑ",np.where((df["ektimisi_ergasiakis_ikanopioisis"]>=108)&(df["ektimisi_ergasiakis_ikanopioisis"]<144),"ΑΜΦΙΘΥΜΙΑ",np.where((df["ektimisi_ergasiakis_ikanopioisis"]>=144)&(df["ektimisi_ergasiakis_ikanopioisis"]<216),"ΙΚΑΝΟΠΟΙΗΣΗ",np.where(df["ektimisi_ergasiakis_ikanopioisis"].isna(),np.nan,np.nan))))
  #Εκτίμηση εργασιακού άγχους (Questionario di Valutazione dello Stress Occupazionale) Συνολικό σκορ
  df["ektimisi_agxous_sunolo_CAT"]=np.where(df["ektimisi_agxous_sunolo"]<70,"ΑΠΟΥΣΙΑ ΕΡΓΑΣΙΑΚΟΥ ΑΓΧΟΥΣ",np.where((df["ektimisi_agxous_sunolo"]>=70)&(df["ektimisi_agxous_sunolo"]<95),"ΗΠΙΟ ΕΡΓΑΣΙΑΚΟ ΑΓΧΟΣ",np.where((df["ektimisi_agxous_sunolo"]>=95)&(df["ektimisi_agxous_sunolo"]<120),"ΜΕΤΡΙΟ ΕΡΓΑΣΙΑΚΟ ΑΓΧΟΣ",np.where(df["ektimisi_agxous_sunolo"]>=120,"ΣΟΒΑΡΟ ΕΡΓΑΣΙΑΚΟ ΑΓΧΟΣ",np.where(df["ektimisi_agxous_sunolo"].isna(),np.nan,np.nan)))))

  ######################################################################################################################################################
  ######################################################################################################################################################


  #Αντικατάσταση με κατάλληλες τιμές NaN
  df=df.replace("nan",np.nan)
  #st.write(df)

  ######################################################################################################################################################################
  ######################################################################################################################################################################

  #Sidebar Creation - Section:
  with st.sidebar:
      st.image("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBQRDxUPFBIYEhISEhIYGREYEhIcGhkRGhQdGRwcFhgdIC4oHSwrHx4YJzgmKy80NUM2Hic9QDwzPzA0NTEBDAwMEA8QHhISHjQsJCg0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NP/AABEIAKQBNAMBIgACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAABQYBBAcDAgj/xABKEAABAwICBQQOBwYEBwAAAAABAAIDBBEFEgYhMUFREyJhcQcUFzI1QlJTgZGTobHSFiNUcnN0sxUkM4LB8ENiksM0Y6KywuHx/8QAGQEBAAMBAQAAAAAAAAAAAAAAAAECAwUE/8QAMBEBAQABAgQDBgQHAAAAAAAAAAECAxESITFRFEGhMmFxgdHwYpGxwQQiI0JS4fH/2gAMAwEAAhEDEQA/AOzIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAtWuq2QRPnecrI2lznWJs0bTYaytpQmmHgyq/LyfBEZXaWtH6fYf58+xn+VPp9h/nz7Gf5VxRZWfHXM8bqdo7V9PcP8+fYz/Kn0+w/wA+fYzfKuKonHTxup2jtX0+w/z59jP8qfT3D/Pn2M/yriiynHTxup2jtX0+w/z59jP8qfT7D/Pn2M/yriqJx08bqdo7V9PsP8+fYz/Kn0+w/wA+fYz/ACriqJx08bqdo/Q2GYhHUwieJ2aN97OyuF7OLTqIB2grdVY7HfgqDrm/WcrOtI6WGXFjKIiIsIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgKF0v8G1X4EnwU0oXS/wbVfgSfBL0Vy9muCoiLBwRFlb+F4PPVZzFHdkbSXvJDWNAF9bjqvbcpWktu0R6ICihAiIgLKwiIdt7HfgqDrm/VcrOqx2O/BUHXN+s5WdbTo7ml7GPwgiIpaCIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiIChdL/AAbVfgSfBTShNMPBlV+Xk+CVXP2a4MiK26IaLicGsqvq6SMZru1Z7dPk9O/YFjJu4mGFzu0eei+i3bDTV1DuRo2AuLybF4HkncOn0Bb8ks2KSdoULBBQxHaAQ0jypDtN9oZt49G6DNjc4jjBgw2BwBAFs9rarDeRsGxt77VZ8bxSnwelDY42tc64jhbYXd5Tt9hvKtJHuw08eG/4+d7/AEiqaSYDh2H0ZjeXSVb2cx2Y5s/lZRqa2/HqXPrq9YBovPiUprqxzmxP132OeNwaPEaP/nFemmeNUkdP+zaWKNzQec8C7WPB8Uja7bc39aWb82Opp8U49uGeU86oKL2fTPaxspY4RyEhry0hriNuU714qjyiyiAEkAC5JAAAuSTuARDtfY78FQdcv6zlK4bi8dTJNHHmPa8mRziOaX2ucp32VS7dfhmEQUYF62cObHENrXveTc/dzD0qxaPYY3D6EMc7W0OklkJ2vPOe4no2dQW0dnTyvLHtOadCyoLRuZ8sb6t5IbUPL42EnmU4AazbszAZz95TgKltLvN2URESIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAoTTHwZVfl5PgptQmmAvhlUALkwP1dNkqufs34OXaC6O9u1OZ7SaeKxfwc/xWf1PR1q14uDitW3DobtoqUjl5GagXgWDG7jbZ6zuC+6kuwrC4qWIXrKkhoA1nlnWzu/luAPQp3DKWLCsPGdwAiYXySW1ukOtx6bnUPQqSctnk0tKTHgvxy+j5xbEYMJo2hrNhDIoG9895954k/1UPgWjL55TiOIgOldYsgNssbRszDo4bt+teuj2Fvq6kYvUi1x+705N+Tj3OPSRr9N+C09LMYmq6j9lUZN7kTSg80C2tpcL5QN546uKm918rLOLKcvKff3sjtLtMnzyGhojmY6zDIwEue47WstsG4lQ0uFQ4bldU2nqi0OZSNPMZwM7t/3Rt6VI19RFgzO1qdzZK5zfraqwORvBjTex6PSdypMsjnvLnOLnOJLnE3Jcd5KrbzePVz575c8vSNjEMQkqHl8j8x3NGpjRwY3Y0dS1FlelPA6V7Y2ML3vNmtaLknbq9F1V5udrzAJIAFyTYADWTwAXRsIwmHCKcYhWc6pP8OEG9nEamtG93E7B8fjDcPpsGjFXVOElYW3ZALEscRu6eLzq4dMpovhE1XN+1K4Xcf4EDhqYw7HZd3Rv3ncrSPZo6Nxy/F+nvrd0Wwd7nnE6sA1UwGRltUUXitaNxt/e1YxetFfU/suEl0bHNdVSA80Rg/wgd5cbA9F+lfWP44+WQ4bRnNUv1PlHewM8Zzj5XQtumpabB6Jzr2a0ZnyON3ySW38STsCs9ck24Z0nW/fq8tJZOU5PCojZ1RYPy+JRt789F+9HWrJEwNaGjY0ADqAsq5ofRP5N1dOD2zVkPcD4kXiMbwAGu3EqzqzTDn/NfP8AQRERoIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAvKWIOaWkXB2j03XqvCrqGxRukccrGi7ncBxQR8+FCSujq3EOEMTmsZbvXuPOdf7oAHpUXibW19e2j76npLSTjxXyu/hsPG2txHUrQDcKKwbCG0ccga50jpJJJHPdYOc9xvbV6Ao2Z3Hfl5XnUXpZi8jHMw+k11U+8W+ri3vPDo6upVrFq5mDQdpUxz1coBmqDrLSRt69ZsN203upSCY4bSTYjUtDq2qcTkJ1g+JGLbABrNvfqXLaqpdLI6V5zPe4uc7i4m+pVyrxa+rcefnfSfWvhzi4lziXOJJLibkk7STvWFMYPozVVeuOItZ5192stxBPfei6sowXDcOGarnFVO237uzZm+4D/3G3QqzGvNjo5ZTfpO9VvR/Ruorn/Vsyxg86Z2pg6vKPQPcrFUYhS4Tmp6NvbFYea6pcLhh4NA2nXsHpJ2LwqMbrcUPatJEYYBzcseoBv/ADJBqAt4o96naHC6LBGCoqH8pUkWAAuQTt5NnD/Mfcpkb6eEnPD55X9t3nozok5zxiVe/PIbPDHnYQNTpTs1ADm7B7lsYtpPJWyihw7nFwIkqrODWM4sPr53q4iDqsQrMcmMEI5KlaRmB70C+2Rw742IOQf+1b3Oo8EpdQs5w7293yvA/voF1MbY7cNmPLHzvds4dR0+FUnOe1o758zrB0kh1k8SeAUFhdPJi9QK6cFtFE8mCnIHPcNWd3EXH9Nl76FBhtRjcraupPJ0jHHJE3xhfWB8C4+hdJijaxoY0BrWgANAsABsACmc2uE49uW2M6e//T7AX0orHcchoY2yTFwa9+UZWFxzZSdg6AVGUGm9HUTMp43PL5DYXieBexOs7titvGt1MZeG3mtCKEx3SSnoSwTucDIHFoaxztTbXvbZtC2cUxeKlp+2ZCRHzNbWknnEAah1hE8ePPn0SSKn90Wg8uT2L1v1ullNDUtpHucJXGMDmOLefbLd3pUbqzVwvSxYUURPj8EdYyhcXcvI0Oa0MOW1nHW7YO9cmOY9DQsbJO4ta92VuVhcc1idg6ApW4sed36JdFrUVU2aJkzDdkjGuaf8rhcXC2UWEREBERAREQEREBERAREQEREBERAUJpj4Mqvy8nwU2oXS/wAG1X4EnwSq5+zXMdH9OailAjf+8QtFgHGz2jg1+/qKtkXZMpSLuimYeAaw+/MuULdwieGOYOqITPGAbxh5br3G42216llMq5On/EamO03/ADWDSjSiGtq4XuifJSxNdeJzsjnudtN2nVsb6isRaXwwt+ow2GN/lvJefeAeG9bHbmBu5xpp2k68oe+wPAWeviPGcJhOaOgfI5pu0ySEj1Fx+Cnf3tN8t7lx48/vs0HYviOJPMLXySX1mOMBjAOki2rrKlabQqOlYKjEZ2xxgAmFhOYuPilw1n+X1rVxLT+qk5sWWlZYDKwNLv8AU4fABamG6J1ta7OWOYHG5mmJF+kA84+pR6qzht5b5339EtX6ctjibTYfEKeNoIzuALtfktudfSbleWj+hdRWv7ZqXPjjcblzyTI8bdQPejpPoC3mMw3CDnMnbtWy9mi2Vj+oamdZJKiqvSCuxaUU0QLGu/wozYZeMjzrt6h0Kfivltv/AFLvfLGLNjelVPhsXaVG1r5Gat5aw8XHxndF+tRFBgD5r4nispZFqdkebOcNwyjvG/5RrPQvgUtJg2V0uWrrhYiEH6uPXtJtt4E6+gbVWMbxmatmMsrr6zlYCcjG8Gj+u0pb3NTU29vn+GdJ8fo7lgtbFUUzJYBaJwIaMuWwaS22XdaykFWOx34Kg65f1XKzrR0NO74y+5Quy3/wUX4/+25emBYZhAnifTvY6pbzmtFRI458hvzS6x1XXn2WzaiiPCf/AG3LYwDQaKlniq2zSOcwE5HBmU5mFpvYX3qvm89lutdpL06+Sr9kt7psQ5NusU9MHO6ASXOPqLVahSnEMAZGDz3QMy9MsZ1A9bm2UHhNP29iWKP2jkZIh/NzG8N0ak+xpiLW4XJndlbTSSFxO5hAff3uUTqrp89S29Mt/RWdAsKo6t0lPUREzN5zDykrbsGpzSGuGtpt6+hePZDY79qSZdrIonX4BrL39CkNA6d1XiktfbIyNz32AsM0mYNb/pJJ9C3sUpRPpE6B2ySmew/zUzgnkymHFoyTzu2/d5msFRj2H1A/xKZjvSYpbj13Weyg501TTUrNbhHM8j0XHuY5V3Q17v2rSRv2wuljtws2QkeguKmsZxmGPH3zTZjHCzkwGtDjmMVth6XuTfknj49O78t8v2n0W3seVXKYXDxjzsP8rzb/AKbK0LnvYnqRyE9ODcRyNe2/kvbb/wAF0JWnR7NDLfTxvuERFLUREQEREBERAREQEREBERAREQFC6X+Dar8CT4KaULph4Mqvy8nwS9Fc/ZrgqysIsHBbVAYM55cSFmXVyRYHZr78wta11YaWswdo51LUPc3WM018x4ENcB7lVFIYdWQx/wASkbUHNe7ppWc3hZpsfUpla4Z7dvnN1gdpnFCLUmHww28d4DnbuFvivMYhi2Ighhkew7mNEbdvl6vivlmlcMdjDhsEbhaz3uc8gjfrA6d68a/Taumbk5URN4RNDdX3tZ9RVt+9bXUnnnflNkjFojBRtEuIVLWjV+7xm7nHhca/UPStGt0rLGuhoom0cJtzmD611vKd/fWq09xc4ucS5x2uJJJ6yVhV37Mrq+WE2/X8xxJJcSSSbkk3JPEneiwihi7b2OvBUHXN+q5WdVfsdeCYOub9ZytC2nR3NL2MfhFK7JtBLUUkTIo3yuE1y1jSSBybhcgdJChsHxfF+XjEsUnIgOzDtZo1BhIFw2+0BdNslk257q5aW+fHMrHFsGGK0mcw08rTKQXXpw67hfiNW0r7w/D65lHWw9rTNdOIHW5IjMRLzwNXku2cAuzWSyjhZz+Fk/uv/XGcKkxejiMUFPIxpcXEdrNcS4jaSW3OwK0w0Uxx+OpdE/IYAHS5CGh/IEEE7NupX2yWUyLYaHDNuK+Xo5ozA5YtIhM2J5gMrn8oGnIM8LiQXbO+J9a+9HdGhVVdZUVtM8NfJdgeHsuHOeSRYi+rKF0iyWTaJmhjL87dlB0XwuSjxipY2F7aV8YyPs7JqyuaA7XxeNu5X9YsspJs0wwmE2giIpXEREBERAREQEREBERAREQEREBQmmHgyq/LyfBTa0MYoe2aWWnzZeVjc3Na9rjbbeiuU3lj89Iuldy0faz7AfOs9y0fbD7AfOsuGuV4XV7ermqwul9y0fbD7AfOncuH2s+wHzpw1HhdXt6xzVF0ruWj7WfYD507lo+1n2A+dOGp8Lq9vWOaIul9y0faz7AfOnctH2s+wHzpw08Lq9vWOaLK6V3LR9sPsB86x3LR9rPsB86cNPC6vb1WPsd+CoOuX9Vys6itHcK7TpWU2fPyefn5bXzPLtlzxUqtZHU05ZhJewiIi4iIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIg//Z",width=200)
      if role=="admin":

        choose = option_menu(menu_title="Δείκτες Υγείας", options=["Overview Dashboard","Εργαστηριακοί Δείκτες","Βαρέα Μέταλα", "Λοιποί Δείκτες", "Εργασιακή Ικανοποίηση", "Εργατικά Ατυχήματα-Απουσιασμός","Συγκρίσεις Δεικτών","Πίνακας Δεδομένων"],
                            icons=['pie-chart','capsule','exclamation-octagon','clipboard-heart', 'emoji-smile', 'exclamation-triangle','bar-chart','table'],
                            menu_icon="activity", default_index=0,
                            #  styles={
                            #         "container": {"padding": "5!important", "background-color": "#fafafa"},
                            #         "icon": {"color": "orange", "font-size": "30px"}, 
                            #         "nav-link": {"font-size": "20px", "text-align": "left", "margin":"5px", "--hover-color": "#eee"},
                            #         "nav-link-selected": {"background-color": "#02ab21"},
                            #       }
                            )
      else:
        choose = option_menu(menu_title="Δείκτες Υγείας", options=["Overview Dashboard","Εργαστηριακοί Δείκτες","Βαρέα Μέταλα", "Λοιποί Δείκτες", "Εργασιακή Ικανοποίηση", "Εργατικά Ατυχήματα-Απουσιασμός","Συγκρίσεις Δεικτών"],
                            icons=['pie-chart','capsule','exclamation-octagon','clipboard-heart', 'emoji-smile', 'exclamation-triangle','bar-chart'],
                            menu_icon="activity", default_index=0,
                            #  styles={
                            #         "container": {"padding": "5!important", "background-color": "#fafafa"},
                            #         "icon": {"color": "orange", "font-size": "30px"}, 
                            #         "nav-link": {"font-size": "20px", "text-align": "left", "margin":"5px", "--hover-color": "#eee"},
                            #         "nav-link-selected": {"background-color": "#02ab21"},
                            #       }
                            )
      
      if choose=="Συγκρίσεις Δεικτών":
        #Header
        #st.sidebar.header("Επιλέξτε Φίλτρα:")
        #Create an instance of the DynamicFilters class
        #dynamic_filters = DynamicFilters(df, filters=['gender', 'age_group', 'space','eth_ekthesis'])
        #Display the filters in your app:
        #dynamic_filters.display_filters(location="sidebar")
        #Assign a filtered dataframe to a variable:
        #df_filtered = dynamic_filters.filter_df()
        #link of creator
        st.sidebar.markdown('''
    ---
    Created by [CmtProoptiki](https://cmtprooptiki.gr/)
                            ''')

      else:
        #Header
        st.sidebar.header("Επιλέξτε Φίλτρα:")
        #Create an instance of the DynamicFilters class
        dynamic_filters = DynamicFilters(df, filters=['gender', 'age_group', 'xoros_ergasias','eth_ekthesis'])
        #Display the filters in your app:
        dynamic_filters.display_filters(location="sidebar")
        #Assign a filtered dataframe to a variable:
        df_filtered = dynamic_filters.filter_df()
        #link of creator
        st.sidebar.markdown('''
    ---
    Created by [CmtProoptiki](https://cmtprooptiki.gr/)
                            ''')

  ###################################################################################################################################################################
  ###################################################################################################################################################################   

  #Prostasia Proswpikwn Dedomenwn Filtra:
  privacy_limit=5
  warning_message="Για λόγους προστασίας προσωπικών δεδομένων, παρακαλώ επιλέξτε διαφορετικό συνδυασμό φίλτρων"

  ###################################################################################################################################################################
  ################################################################################################################################################################### 

  #Overview Dashboard - Section:
  if choose == "Overview Dashboard":
    with stylable_container(
      key="OverView",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Overview Dashboard:")
    #dynamic_filters.display_df()

    #1: Overview Dashboard:
    col1,col2=st.columns(2)


    #Gender
    with col1:
      with stylable_container(
        key="Overview-Fylo",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 0.5% 2% 0.5%;
                    
                }
                """,
        ):
        st.subheader("Φύλο Εργαζομένων:")
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "indicator"}, {"type": "pie"}]])
        fig.add_trace(go.Indicator(
                      value=df_filtered["id_ergazomenou"].nunique(),
                      align="center",
                      number={"font": {"size": 50,"color":"#379683"}},
                      title={"text":"Αρ.Εργαζομένων","font":{"size":35,"color":"gray"},"align":"center"}
                      ),row=1,col=1)
        fig.add_trace(go.Pie(
                            values= df_filtered["gender"].value_counts().values,
                            labels=df_filtered["gender"].value_counts().index,
                            hole=0,
                            #textinfo='none',
                            #hoverinfo="none",
                            marker_colors=px.colors.qualitative.Set3,
                            direction='clockwise',
                            textfont_size=16
                            ), row=1, col=2)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        fig.update_layout(hoverlabel_font_size=16)
        fig.update_layout(legend_title_font_size=15, legend_font_size=15)
        st.plotly_chart(fig, use_container_width=False,config={'displayModeBar': False})
    #Working Section
    with col2:
      with stylable_container(
        key="Overview-Working-Section",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 0.5% 3% 0.5%;
                    
                }
                """,
        ):
        st.subheader("Χώροι Εργασίας:")
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "indicator"}, {"type": "pie"}]])
        fig.add_trace(go.Indicator(
                      value=df_filtered["xoros_ergasias"].nunique(),
                      align="center",
                      number={"font": {"size": 50,"color":"#379683"}},
                      title={"text":"Χώροι Εργασίας","font":{"size":35,"color":"gray"},"align":"center"}
                      ),row=1,col=1)
        fig.add_trace(go.Pie(
                            values= df_filtered["xoros_ergasias"].value_counts().values,
                            labels=df_filtered["xoros_ergasias"].value_counts().index,
                            hole=0,
                            #textinfo='none',
                            #hoverinfo="none",
                            marker_colors=px.colors.qualitative.Set3,
                            direction='clockwise',
                            textfont_size=16
                            ), row=1, col=2)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        fig.update_layout(hoverlabel_font_size=16)
        fig.update_layout(legend_title_font_size=15, legend_font_size=15)
        st.plotly_chart(fig, use_container_width=False,config={'displayModeBar': False})
    #Hlikiakh katanomh
    with stylable_container(
        key="Overview-Hlikia",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 0.5% 2% 0.5%;
                    
                }
                """,
        ):
        st.subheader("Ηλικιακή Κατανομή Εργαζομένων:")
        fig_extra_kpis_hist = make_subplots(
        rows=2, cols=7,
        #column_widths=[0.6, 0.4],
        row_heights=[0.05, 0.95],
        specs=[[{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"},{"type": "indicator"}],
            [{"type": "Histogram","colspan":5},None,None,None,None,None,None,]])
        #Set the color:
        color='rgb(141,211,199)'
        
        #Set the KPIS and the Hist:
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=df_filtered["patient_age"].count(),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"Εργαζόμενοι","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=1)
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=round(df_filtered["patient_age"].mean(),1),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"Μέσος όρος","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=2)
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=round(df_filtered["patient_age"].min(),1),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"Min","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=3)
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=round(df_filtered["patient_age"].quantile(0.25),1),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"25%","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=4)
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=round(df_filtered["patient_age"].median(),1),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"Διάμεσος","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=5)
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=round(df_filtered["patient_age"].quantile(0.75),1),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"75%","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=6)
        fig_extra_kpis_hist.add_trace(go.Indicator(
                      value=round(df_filtered["patient_age"].max(),1),
                      align="left",
                      number={"font": {"size": 40,"color":"#379683"}},
                      title={"text":"Max","font":{"size":20,"color":"gray"},"align":"left"}
                      ),row=1,col=7)
        fig_extra_kpis_hist.add_trace(go.Histogram(
                      x=df_filtered["patient_age"],
                      #xbins=go.XBins(size=1),
                      autobinx=True,
                      opacity=0.8,
                      #nbinsx=4,
                      #xaxis="x1",
                      #yaxis="y1",
                      marker=go.Marker(color=color,line=dict(color="white", width=1))
                      #name="Test"
                      #histnorm="density"
                      ),row=2,col=1)
        name=df_filtered["patient_age"].name
        fig_extra_kpis_hist.update_xaxes(title_text=name, row=2, col=1)
        fig_extra_kpis_hist.update_yaxes(title_text="Πλήθος Εργαζομένων", row=2, col=1)
        fig_extra_kpis_hist.update_layout(hoverlabel_font_size=16)
        fig_extra_kpis_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        fig_extra_kpis_hist.update_layout(showlegend=False)

        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})

    #Deiktes Ygeias
    with stylable_container(
        key="Overview-Hlikia",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 0.5% 2% 0.5%;
                    
                }
                """,
        ):
        st.subheader("Δείκτες Υγείας:")
        fig = make_subplots(rows=1, cols=3,column_widths=[0.3,0.3,0.4], specs=[[{"type": "indicator"},{"type": "indicator"}, {"type": "pie"}]])
        fig.add_trace(go.Indicator(
                      value=60,
                      align="center",
                      number={"font": {"size": 50,"color":"#379683"}},
                      title={"text":"Αρ.Δεικτών Υγείας","font":{"size":35,"color":"gray"},"align":"center"}
                      ),row=1,col=1)
        fig.add_trace(go.Indicator(
                      value=5,
                      align="center",
                      number={"font": {"size": 50,"color":"#379683"}},
                      title={"text":"Κατηγορίες Δεικτών Υγείας","font":{"size":35,"color":"gray"},"align":"center"}
                      ),row=1,col=2)
        fig.add_trace(go.Pie(
                            values= [29,12,11,2,6],
                            labels=["Εργαστηριακοί Δείκτες","Βαρέα Μέταλα","Λοιποί Δείκτες","Εργασιακή Ικανοποίηση","Εργατικά Ατυχήματα-Απουσιασμός"],
                            hole=0,
                            #textinfo='none',
                            #hoverinfo="none",
                            marker_colors=px.colors.qualitative.Set3,
                            direction='clockwise',
                            textfont_size=16
                            ), row=1, col=3)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
        fig.update_layout(hoverlabel_font_size=16)
        fig.update_layout(legend_title_font_size=15, legend_font_size=15)
        st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})

  ###################################################################################################################################################################
  ###################################################################################################################################################################

  #Εργαστηριακοί Δείκτες - Section:
  elif choose == "Εργαστηριακοί Δείκτες":
    with stylable_container(
      key="Ergastiriakes_title",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Εργαστηριακοί Δείκτες:")
    if (df_filtered["id_ergazomenou"].nunique()<privacy_limit):
      st.warning(warning_message,icon="⚠️")
    else:
      #dynamic_filters.display_df()
  ######################################################################################################################################################################
      #ΕΞΕΤΑΣΗ 2:
      with stylable_container(
        key="Ergastiriakes1",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αιματοκρίτης (HT%):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["ht_aimatokritis_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["ht_aimatokritis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["ht_aimatokritis_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["ht_aimatokritis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          #dataframe=df_filtered
          value=df_filtered["ht_aimatokritis"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
        
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 3:
      with stylable_container(
        key="Ergastiriakes3",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αιμοσφαιρίνη (Hb):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["hb_aimosfairini_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["hb_aimosfairini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["hb_aimosfairini_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["hb_aimosfairini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["hb_aimosfairini"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 4:
      with stylable_container(
        key="Ergastiriakes4",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αιμοπετάλια (PLT):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["plt_aimopetalia_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["plt_aimopetalia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["plt_aimopetalia_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["plt_aimopetalia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["plt_aimopetalia"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 5:
      with stylable_container(
        key="Ergastiriakes5",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Λευκά αιμοσφαίρια (WBC):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["wbc_leyka_aimosferia_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["wbc_leyka_aimosferia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["wbc_leyka_aimosferia_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["wbc_leyka_aimosferia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["wbc_leyka_aimosferia"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 6:
      with stylable_container(
        key="Ergastiriakes6",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Γλυκοζυλιωμένη αιμοσφαιρίνη (HbA1c):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["glukoziliomeni_aimosferini_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["glukoziliomeni_aimosferini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["glukoziliomeni_aimosferini_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["glukoziliomeni_aimosferini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["glukoziliomeni_aimosferini"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 7:
      with stylable_container(
        key="Ergastiriakes7",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ειδικό βάρος ούρων:")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["eidiko_baros_ouron_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["eidiko_baros_ouron_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["eidiko_baros_ouron_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["eidiko_baros_ouron_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["eidiko_baros_ouron"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 8,9:
      col1,col2 = st.columns(2)
      with col1:
        with stylable_container(
          key="Ergastiriakes8",
              css_styles="""
                  {
                      background-color: white;
                      border: 1px solid #DCDCDC;
                      border-radius: 10px;
                      padding: 0.5% 2.5% 0.5% 0.5%;
                      
                  }
                  """,
          ):
        #with st.container(border=True):
          st.subheader("Νιτρώδη:")
          #Times gia synartisi
          try:
            val=round((df_filtered["nitrwdh_CAT"].value_counts().loc["ΑΡΝΗΤΙΚΟ"]/df_filtered["nitrwdh_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["nitrwdh_CAT"].value_counts().loc["ΘΕΤΙΚΟ"]/df_filtered["nitrwdh_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΑΡΝΗΤΙΚΟ", x=0.15, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΘΕΤΙΚΟ", x=0.825, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
      with col2:
        with stylable_container(
        key="Ergastiriakes9",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
        #with st.container(border=True):
          st.subheader("Λεύκωμα ούρων:")
          #Times gia synartisi
          try:
            val=round((df_filtered["leukvma_ouron_CAT"].value_counts().loc["ΑΡΝΗΤΙΚΟ"]/df_filtered["leukvma_ouron_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["leukvma_ouron_CAT"].value_counts().loc["ΘΕΤΙΚΟ"]/df_filtered["leukvma_ouron_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΑΡΝΗΤΙΚΟ", x=0.15, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΘΕΤΙΚΟ", x=0.825, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
      
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 10:
      with stylable_container(
        key="Ergastiriakes10",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ερυθρά αιμοσφαίρια:")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["erithra_aimosferia_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["erithra_aimosferia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["erithra_aimosferia_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["erithra_aimosferia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["erithra_aimosferia"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 11:
      with stylable_container(
        key="Ergastiriakes11",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Πυοσφαίρια:")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["puosfairia_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["puosfairia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["puosfairia_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["puosfairia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["puosfairia"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 12:
      with stylable_container(
        key="Ergastiriakes12",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Γλυκόζη (Glu):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["glukozi_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["glukozi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["glukozi_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["glukozi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["glukozi"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 13:
      with stylable_container(
        key="Ergastiriakes13",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Χοληστερόλη υψηλής περιεκτικότητας λιποπρωτεϊνών (HDL-C):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["xolhsteroli_ipsilis_periektikotitas_CAT"].value_counts().loc["ΕΠΙΘΥΜΗΤΗ"]/df_filtered["xolhsteroli_ipsilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["xolhsteroli_ipsilis_periektikotitas_CAT"].value_counts().loc["ΧΑΜΗΛΗ"]/df_filtered["xolhsteroli_ipsilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["xolhsteroli_ipsilis_periektikotitas_CAT"].value_counts().loc["ΥΨΗΛΗ"]/df_filtered["xolhsteroli_ipsilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          #Call of the function
          fig_three_cat_pie=three_cat_pie (val,val2,val3)

          # Customazation of the fig
          fig_three_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.09, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΕΠΙΘΥΜΗΤΗ", x=0.07, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.5, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΧΑΜΗΛΗ", x=0.495, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.92, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΥΨΗΛΗ", x=0.9009, y=0.45, font_size=20, showarrow=False),
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_three_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
            #Times gia sinartisi
            value=df_filtered["xolhsteroli_ipsilis_periektikotitas"]
          
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 14:
      with stylable_container(
        key="Ergastiriakes14",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Χοληστερόλη χαμηλής περιεκτικότητας λιποπρωτεϊνών (LDL-C):")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().loc["ΙΔΑΝΙΚΗ"]/df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().loc["ΣΧΕΔΟΝ ΙΔΑΝΙΚΗ"]/df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().loc["ΟΡΙΑΚΑ ΥΨΗΛΗ"]/df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().loc["ΥΨΗΛΗ"]/df_filtered["xolh_xamilis_periektikotitas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie_v2=four_cat_pie_v2 (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie_v2.update_layout(annotations=[dict(text=str(val) + "%", x=0.05, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΙΔΑΝΙΚΗ", x=0.051, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.375, y=0.55, font_size=30,font=dict(color="rgba(113,209,145,0.6)"), showarrow=False),
                                          dict(text="ΣΧΕΔΟΝ ΙΔ.", x=0.3, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΟΡ. ΥΨΗΛΗ", x=0.63, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΥΨΗΛΗ", x=0.94, y=0.45, font_size=20, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie_v2, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["xolh_xamilis_periektikotitas"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 15:
      with stylable_container(
        key="Ergastiriakes15",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ολική χοληστερόλη (TC):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["oliki_xolisteroli_CAT"].value_counts().loc["ΕΠΙΘΥΜΗΤΗ"]/df_filtered["oliki_xolisteroli_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["oliki_xolisteroli_CAT"].value_counts().loc["ΟΡΙΑΚΑ ΥΨΗΛΗ"]/df_filtered["oliki_xolisteroli_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["oliki_xolisteroli_CAT"].value_counts().loc["ΥΨΗΛΗ"]/df_filtered["oliki_xolisteroli_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          #Call of the function
          fig_three_cat_pie=three_cat_pie (val,val2,val3)

          # Customazation of the fig
          fig_three_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.09, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΕΠΙΘΥΜΗΤΗ", x=0.07, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.5, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΟΡΙΑΚΑ ΥΨΗΛΗ", x=0.495, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.92, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΥΨΗΛΗ", x=0.9009, y=0.45, font_size=20, showarrow=False),
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_three_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
            #Times gia sinartisi
            value=df_filtered["oliki_xolisteroli"]
          
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################

      #ΕΞΕΤΑΣΗ 16:
      with stylable_container(
        key="Ergastiriakes16",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Τριγλυκερίδια:")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["triglykeridia_CAT"].value_counts().loc["ΒΕΛΤΙΣΤΗ ΤΙΜΗ"]/df_filtered["triglykeridia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["triglykeridia_CAT"].value_counts().loc["ΟΡΙΑΚΑ ΥΨΗΛΗ"]/df_filtered["triglykeridia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["triglykeridia_CAT"].value_counts().loc["ΥΨΗΛΑ ΕΠΙΠΕΔΑ"]/df_filtered["triglykeridia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["triglykeridia_CAT"].value_counts().loc["ΠΟΛΥ ΥΨΗΛΑ ΕΠΙΠΕΔΑ"]/df_filtered["triglykeridia_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.05, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΒΕΛΤΙΣΤΗ", x=0.045, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.375, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΟΡΙΑΚΑ ΥΨ.", x=0.3, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.6)"), showarrow=False),
                                          dict(text="ΥΨΗΛΗ", x=0.63, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΟΛΥ ΥΨΗΛΗ", x=0.972, y=0.45, font_size=20, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["triglykeridia"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
      ######################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 17:
      with stylable_container(
        key="Ergastiriakes17",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Θυρεοειδοτρόπος ορμόνη (TSH):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["thuroeidotropos_ormoni_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["thuroeidotropos_ormoni_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["thuroeidotropos_ormoni_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["thuroeidotropos_ormoni_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["thuroeidotropos_ormoni"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 18:
      with stylable_container(
        key="Ergastiriakes18",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ελεύθερη τριιωδοθυρονίνη (fT3):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["eleutheri_triiodothironini_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["eleutheri_triiodothironini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["eleutheri_triiodothironini_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["eleutheri_triiodothironini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["eleutheri_triiodothironini"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 19:
      with stylable_container(
        key="Ergastiriakes19",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ελεύθερη θυροξίνη (fT4):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["eleutheri_thuroksini_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["eleutheri_thuroksini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["eleutheri_thuroksini_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["eleutheri_thuroksini_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["eleutheri_thuroksini"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 20:
      with stylable_container(
        key="Ergastiriakes20",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αντισώματα έναντι θυρεοειδικής υπεροξειδάσης (anti-TPO):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["antiswmata_anti_tpo_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["antiswmata_anti_tpo_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["antiswmata_anti_tpo_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["antiswmata_anti_tpo_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["antiswmata_anti_tpo"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
        
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 21:
      with stylable_container(
        key="Ergastiriakes21",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ουρία (Ur):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["ouria_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["ouria_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["ouria_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["ouria_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["ouria"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 22:
      with stylable_container(
        key="Ergastiriakes22",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Κρεατινίνη (Cr):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["kreatinh_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["kreatinh_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["kreatinh_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["kreatinh_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False)
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["kreatinh"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 23:
      with stylable_container(
        key="Ergastiriakes23",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ασπαρτική αμινοτρανφεράση (AST/SGOT):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["aspartikh_aminotranferasi_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["aspartikh_aminotranferasi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["aspartikh_aminotranferasi_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["aspartikh_aminotranferasi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["aspartikh_aminotranferasi"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 24:
      with stylable_container(
        key="Ergastiriakes24",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αμινοτρανσφεράση αλανίνης(ALT/SGPT):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["aminotranferasi_alaninis_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["aminotranferasi_alaninis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["aminotranferasi_alaninis_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["aminotranferasi_alaninis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["aminotranferasi_alaninis"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 25:
      with stylable_container(
        key="Ergastiriakes25",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("γ-Γλουταμυλοτρανφεράση (γ-GT):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["g_gloutamylotranferasi_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["g_gloutamylotranferasi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["g_gloutamylotranferasi_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["g_gloutamylotranferasi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["g_gloutamylotranferasi"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 26:
      with stylable_container(
        key="Ergastiriakes26",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αλκαλική φωσφατάση(ALP):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["alkaliki_fosfatasi_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["alkaliki_fosfatasi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["alkaliki_fosfatasi_CAT"].value_counts().loc["ΠΑΘΟΛΟΓΙΚΗ"]/df_filtered["alkaliki_fosfatasi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.165, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΘΟΛΟΓΙΚΗ", x=0.86, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["alkaliki_fosfatasi"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 27:
      with stylable_container(
        key="Ergastiriakes27",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αυστραλιανό αντιγόνο επιφανείας(HBsAg):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["hbsag_CAT"].value_counts().loc["ΘΕΤΙΚΟ"]/df_filtered["hbsag_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["hbsag_CAT"].value_counts().loc["ΑΡΝΗΤΙΚΟ"]/df_filtered["hbsag_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.17, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΘΕΤΙΚΟ", x=0.175, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΑΡΝΗΤΙΚΟ", x=0.836, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["hbsag"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 28:
      with stylable_container(
        key="Ergastiriakes28",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ολικά αντισώματα ένταντι του Αυστραλιανού αντιγόνου (total anti-HBsAg):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["australiano_antigono_CAT"].value_counts().loc["ΕΠΑΡΚΕΙΑ ΕΜΒΟΛΙΑΣΤΙΚΗΣ ΚΑΛΥΨΗΣ"]/df_filtered["australiano_antigono_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["australiano_antigono_CAT"].value_counts().loc["ΑΡΝΗΤΙΚΟ"]/df_filtered["australiano_antigono_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.17, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΕΠΑΡΚΕΙΑ", x=0.168, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΑΡΝΗΤΙΚΟ", x=0.836, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["australiano_antigono"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 29:
      with stylable_container(
        key="Ergastiriakes29",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ολικά αντισώματα ένταντι του πυρηνικού αντιγόνου HBV (total anti-HBc):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["olika_anti_hbv_CAT"].value_counts().loc["ΘΕΤΙΚΟ"]/df_filtered["olika_anti_hbv_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["olika_anti_hbv_CAT"].value_counts().loc["ΑΡΝΗΤΙΚΟ"]/df_filtered["olika_anti_hbv_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.17, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΘΕΤΙΚΟ", x=0.175, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΑΡΝΗΤΙΚΟ", x=0.836, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["olika_anti_hbv"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 30:
      with stylable_container(
        key="Ergastiriakes30",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ολικά αντισώματα ένταντι του ιού της ηπατίτιδας Α (total anti-HAV):")
        col1,col2 = st.columns(2)

        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["olika_anti_a_ipatitidas_CAT"].value_counts().loc["ΘΕΤΙΚΟ"]/df_filtered["olika_anti_a_ipatitidas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["olika_anti_a_ipatitidas_CAT"].value_counts().loc["ΑΡΝΗΤΙΚΟ"]/df_filtered["olika_anti_a_ipatitidas_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.17, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΘΕΤΙΚΟ", x=0.175, y=0.43, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΑΡΝΗΤΙΚΟ", x=0.836, y=0.43, font_size=20, showarrow=False),
                                          ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
        #Times gia sinartisi
          value=df_filtered["olika_anti_a_ipatitidas"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)

          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

  ###################################################################################################################################################################
  ###################################################################################################################################################################  

  #Βαρέα Μέταλα - Section:
  elif choose== "Βαρέα Μέταλα":
    with stylable_container(
      key="Varea_metala_title",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Βαρέα Μέταλα:")
    if (df_filtered["id_ergazomenou"].nunique()<privacy_limit):
      st.warning(warning_message,icon="⚠️")
    else:

  ###############################################################################################################################################
    
      #ΕΞΕΤΑΣΗ 1:
      with stylable_container(
        key="Varea_Metala",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Μόλυβδος, ολικό αίμα (Pb):")
        #Times gia sinartisi
        value=df_filtered["molubdos"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 2:
      with stylable_container(
        key="Varea_Metala2",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Δ-Αμινολεβουλινικό οξύ (δ-ΑLA):")
        #Times gia sinartisi
        value=df_filtered["d_ala_aminoleboyliniko_oksi"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 3:
      with stylable_container(
        key="Varea_Metala3",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ψευδαργυρική Πρωτοπορφυρίνη (ZPP):")
        #Times gia sinartisi
        value=df_filtered["pseudargiriki_protoporfirini"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 4:
      with stylable_container(
        key="Varea_Metala4",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Μόλυβδος ούρων (PBU):")
        #Times gia sinartisi
        value=df_filtered["molubdos_ourwn"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 5:
      with stylable_container(
        key="Varea_Metala5",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Χρώμιο, ολικό αίμα (Cr):")
        #Times gia sinartisi
        value=df_filtered["xrvmio_oliko_aima_cr"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 6:
      with stylable_container(
        key="Varea_Metala6",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Χρώμιο  ούρων (CrU):")
        #Times gia sinartisi
        value=df_filtered["xrwmio_ouron_cru"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 7:
      with stylable_container(
        key="Varea_Metala7",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Κάδμιο, ολικό αίμα (Cd):")
        #Times gia sinartisi
        value=df_filtered["kadmio_oliko_aima_cd"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 8:
      with stylable_container(
        key="Varea_Metala8",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Κάδμιο  ούρων (CdU):")
        #Times gia sinartisi
        value=df_filtered["kadmio_ouron_cdu"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 9:
      with stylable_container(
        key="Varea_Metala9",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αρσενικό, ολικό αίμα (As):")
        #Times gia sinartisi
        value=df_filtered["arseniko_oliko_as"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 10:
      with stylable_container(
        key="Varea_Metala10",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αρσενικό  ούρων (AsU):")
        #Times gia sinartisi
        value=df_filtered["arseniko_ouron_asu"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 11:
      with stylable_container(
        key="Varea_Metala11",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Υδράργυρος, ολικό αίμα (Hg):")
        #Times gia sinartisi
        value=df_filtered["udrargyros_oliko_aim_hg"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})
    ######################################################################################################################################

    #ΕΞΕΤΑΣΗ 12:
      with stylable_container(
        key="Varea_Metala12",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 1% 2% 1% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Υδράργυρος ούρων τυχαίας ούρησης (HgU):")
        #Times gia sinartisi
        value=df_filtered["udrargyros_ouron_hgu"]
            
        #Call of the function
        fig_extra_kpis_hist=kpis_extra_hist(value)

        #Show the plot:
        st.plotly_chart(fig_extra_kpis_hist, use_container_width=True,config={'displayModeBar': False})

  ###################################################################################################################################################################
  ###################################################################################################################################################################  
    
  #Λοιποί Δείκτες - Section:
  elif choose== "Λοιποί Δείκτες":
    with stylable_container(
      key="Loipoi_Deiktes_title",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Λοιποί Δείκτες:")
    if (df_filtered["id_ergazomenou"].nunique()<privacy_limit):
      st.warning(warning_message,icon="⚠️")
    else:
      #dynamic_filters.display_df()

    ################################################################################################################################################################
      #ΕΞΕΤΑΣΗ 1.1:
      with stylable_container(
        key="Loipoi_Deiktes",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αρτηριακή Πίεση (Bp) - Συστολική:")

        col1,col2=st.columns(2)

        with col1:
            
          #Times gia synartisis
          try:
            val = round((df_filtered["systoliki_piesi_CAT"].value_counts().loc["ΦΥΣΙΟΛΟΓΙΚΗ"] / df_filtered["systoliki_piesi_CAT"].value_counts().sum()) * 100, 1)
          except KeyError:
            val=00.00

          try:
            val2=round((df_filtered["systoliki_piesi_CAT"].value_counts().loc["ΑΡΤΗΡΙΑΚΗ ΥΠΕΡΤΑΣΗ"]/df_filtered["systoliki_piesi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.17, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                        dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                        dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                        dict(text="ΑΡΤΗΡΙΑΚΗ ΥΠΕΡΤΑΣΗ", x=0.91, y=0.43, font_size=20, showarrow=False),
                                        ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
            
          #Times gia sinartisi
          value=df_filtered["systoliki_piesi"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)
          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
      ################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 1.2:
      with stylable_container(
        key="Loipoi_Deiktess",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Αρτηριακή Πίεση (Bp) - Διαστολική:")

        col1,col2=st.columns(2)

        with col1:
            
          #Times gia synartisis
          try:
            val = round((df_filtered["diastoliki_piesi_CAT"].value_counts().loc["ΦΥΣΙΟΛΟΓΙΚΗ"] / df_filtered["diastoliki_piesi_CAT"].value_counts().sum()) * 100, 1)
          except KeyError:
            val=00.00

          try:
            val2=round((df_filtered["diastoliki_piesi_CAT"].value_counts().loc["ΑΡΤΗΡΙΑΚΗ ΥΠΕΡΤΑΣΗ"]/df_filtered["diastoliki_piesi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.17, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                        dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.143, y=0.43, font_size=20, showarrow=False),
                                        dict(text=str(val2) + "%", x=0.84, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                        dict(text="ΑΡΤΗΡΙΑΚΗ ΥΠΕΡΤΑΣΗ", x=0.91, y=0.43, font_size=20, showarrow=False),
                                        ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
            
          #Times gia sinartisi
          value=df_filtered["diastoliki_piesi"]
          
          #Call of the function
          fig_kpis_hist=kpis_hist(value)
          #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
    ###################################################################################################################################################################
    
      #ΕΞΕΤΑΣΗ 2:
      with stylable_container(
        key="Loipoi_Deiktes1",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Δείκτης μάζας/σώματος (BMI index):")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().loc["ΛΙΠΟΒΑΡΕΙΣ"]/df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().loc["ΦΥΣΙΟΛΟΓΙΚΟΙ"]/df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().loc["ΥΠΕΡΒΑΡΟΙ"]/df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().loc["ΠΑΧΥΣΑΡΚΟΙ"]/df_filtered["diktis_mazas_somatos_bmi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie_v2=four_cat_pie_v2 (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie_v2.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΛΙΠΟΒΑΡΕΙΣ", x=0.03, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(113,209,145,0.8)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΟΙ", x=0.28, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΥΠΕΡΒΑΡΟΙ", x=0.63, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΑΧΥΣΑΡΚΟΙ", x=0.97, y=0.45, font_size=19, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie_v2, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["diktis_mazas_somatos_bmi"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

    ################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 3:
      with stylable_container(
        key="Loipoi_Deiktes2",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Καπνιστικές Συνήθειες:")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().loc["ΜΗ ΚΑΠΝΙΣΤΗΣ"]/df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().loc["ΗΠΙΟΣ ΚΑΠΝΙΣΤΗΣ"]/df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().loc["ΜΕΤΡΙΟΣ ΚΑΠΝΙΣΤΗΣ"]/df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().loc["ΒΑΡΥΣ ΚΑΠΝΙΣΤΗΣ"]/df_filtered["kapnistikes_synithies_devided_by_20_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΜΗ ΚΑΠΝΙΖΩΝ", x=0.018, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΗΠΙΟΣ", x=0.37, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΜΕΤΡΙΟΣ", x=0.63, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΒΑΡΥΣ", x=0.94, y=0.45, font_size=20, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["kapnistikes_synithies_devided_by_20"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

  ##################################################################################################################################################################
    
      #ΕΞΕΤΑΣΗ 4:
      with stylable_container(
        key="Loipoi_Deiktes3",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Καρδιαγγειακός κίνδυνος:")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["kardiagiakos_kindynos_CAT"].value_counts().loc["ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"]/df_filtered["kardiagiakos_kindynos_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["kardiagiakos_kindynos_CAT"].value_counts().loc["ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"]/df_filtered["kardiagiakos_kindynos_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["kardiagiakos_kindynos_CAT"].value_counts().loc["ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"]/df_filtered["kardiagiakos_kindynos_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["kardiagiakos_kindynos_CAT"].value_counts().loc["ΠΟΛΥ ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"]/df_filtered["kardiagiakos_kindynos_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΧΑΜΗΛΟΣ", x=0.049, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΜΕΤΡΙΟΣ", x=0.37, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΥΨΗΛΟΣ", x=0.63, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΟΛΥ ΥΨ.", x=0.95, y=0.45, font_size=20, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["kardiagiakos_kindynos"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

  ##################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 5:
      with stylable_container(
        key="Loipoi_Deiktes4",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Ακοολογικός έλεγχος (Ακουόγραμα):")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["akouograma_CAT"].value_counts().loc["ΦΥΣΙΟΛΟΓΙΚΗ ΑΚΟΗ"]/df_filtered["akouograma_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["akouograma_CAT"].value_counts().loc["ΜΙΚΡΟΥ-ΜΕΤΡΙΟΥ ΒΑΘΜΟΥ ΒΑΡΗΚΟΙΑ"]/df_filtered["akouograma_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["akouograma_CAT"].value_counts().loc["ΜΕΤΡΙΟΥ-ΣΟΒΑΡΟΥ ΒΑΘΜΟΥ ΒΑΡΗΚΟΙΑ"]/df_filtered["akouograma_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["akouograma_CAT"].value_counts().loc["ΚΩΦΩΣΗ"]/df_filtered["akouograma_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛ.", x=0.055, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΜΙΚΡΗ-ΜΕΤΡΙΑ<br>ΒΑΡΗΚ.", x=0.37, y=0.4, font_size=17, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΜΕΤΡΙΑ-ΣΟΒΑΡΗ<br>ΒΑΡΗΚ.", x=0.63, y=0.4, font_size=17, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΚΩΦΩΣΗ", x=0.95, y=0.45, font_size=19, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["akouograma"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
  ##################################################################################################################################################################
    
      #ΕΞΕΤΑΣΗ 6:
      with stylable_container(
        key="Loipoi_Deiktes5",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Εκτίμηση μυοσκελετικών παθήσεων (Nordic Muscoloskeletal Questionnaire score):")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().loc["ΧΩΡΙΣ MSDS"]/df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().loc["ΗΠΙΟ-ΜΕΤΡΙΟ MSDS"]/df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().loc["ΣΟΒΑΡΟ MSDS"]/df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().loc["ΠΟΛΥ ΣΟΒΑΡΟ MSDS"]/df_filtered["ektimisi_myoskeletikon_pathiseon_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΧΩΡΙΣ MSDS", x=0.03, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΗΠΙΟ-ΜΕΤΡΙΟ<br>MSDS", x=0.37, y=0.4, font_size=19, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΣΟΒΑΡΟ<br>MSDS", x=0.63, y=0.4, font_size=19, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΟΛΥ ΣΟΒΑΡΟ<br>MSDS", x=0.98, y=0.4, font_size=19, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["ektimisi_myoskeletikon_pathiseon"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

    ################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 7:
      with stylable_container(
        key="Loipoi_Deiktes6",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.05%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Λειτουργικός έλεγχος αναπνοής (Σπιρομέτρηση):")
        with st.container(border=True):
          #Times gia sinartisi me filtro giati einai polles sthn spirometrisi
          value=st.selectbox("Επιλέξτε Παράμετρο Ιστογράμματος:",options=["spirometrisi_fvc","spirometrisi_fev1","spirometrisi_fev1_fvc"])
        col1,col2 = st.columns(2)

        with col1:
          # #Times gia sinartisi me filtro giati einai polles sthn spirometrisi
          # value=st.selectbox("Επιλέξτε παράμετρο",options=["spir-FVC","spir-FEV1","spir-FEV1/FVC"])
          #Times gia synartisi
          try:
            val=round((df_filtered["spirometrisi_CAT"].value_counts().loc["ΕΝΤΟΣ ΦΥΣΙΟΛΟΓΙΚΩΝ ΟΡΙΩΝ"]/df_filtered["spirometrisi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["spirometrisi_CAT"].value_counts().loc["ΣΥΜΒΑΤΟ ΜΕ ΑΠΟΦΡΑΚΤΙΚΟ ΣΥΝΔΡΟΜΟ"]/df_filtered["spirometrisi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["spirometrisi_CAT"].value_counts().loc["ΣΥΜΒΑΤΟ ΜΕ ΠΕΡΙΟΡΙΣΤΙΚΟ ΣΥΝΔΡΟΜΟ"]/df_filtered["spirometrisi_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          #Call of the function
          fig_three_cat_pie_v2=three_cat_pie_v2 (val,val2,val3)

          # Customazation of the fig
          fig_three_cat_pie_v2.update_layout(annotations=[dict(text=str(val) + "%", x=0.09, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΦΥΣΙΟΛΟΓΙΚΗ", x=0.06, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.5, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΑΠΟΦΡΑΚΤΙΚΟ<br>ΣΥΝΔΡΟΜΟ", x=0.495, y=0.4, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.92, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΠΕΡΙΟΡΙΣΤΙΚΟ<br>ΣΥΝΔΡΟΜΟ", x=0.945, y=0.4, font_size=20, showarrow=False),
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_three_cat_pie_v2, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
          # #Times gia sinartisi me filtro giati einai polles sthn spirometrisi
          # value=st.selectbox("Επιλέξτε Παράμετρο:",options=["spir-FVC","spir-FEV1","spir-FEV1/FVC"])
          
          # #Call of the function
          fig_kpis_hist=kpis_hist(df_filtered[value])

          # #Show the plot:
          st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
      ################################################################################################################################################################
      
      #ΕΞΕΤΑΣΗ 8,9,10:
      col1,col2,col3=st.columns(3)
      with col1:
        with stylable_container(
          key="Loipoi_Deiktes7",
              css_styles="""
                  {
                      background-color: white;
                      border: 1px solid #DCDCDC;
                      border-radius: 10px;
                      padding: 0.5% 2.5% 0.5% 0%;
                      
                  }
                  """,
          ):
          st.subheader("Εμβολιασμός για HAV:") 
          #Times gia synartisis
          try:
            val = round((df_filtered["embolio_hav"].value_counts().loc["yes"] / df_filtered["embolio_hav"].value_counts().sum()) * 100, 1)
          except KeyError:
            val=00.00

          try:
            val2=round((df_filtered["embolio_hav"].value_counts().loc["no"]/df_filtered["embolio_hav"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.145, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                        dict(text="ΝΑΙ", x=0.18, y=0.43, font_size=25, showarrow=False),
                                        dict(text=str(val2) + "%", x=0.875, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                        dict(text="ΟΧΙ", x=0.82, y=0.43, font_size=25, showarrow=False),
                                        ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=True,config={'displayModeBar': False})
      with col2:
        with stylable_container(
          key="Loipoi_Deiktes8",
              css_styles="""
                  {
                      background-color: white;
                      border: 1px solid #DCDCDC;
                      border-radius: 10px;
                      padding: 0.5% 2.5% 0.5% 0.05%;
                      
                  }
                  """,
          ):
          st.subheader("Εμβολιασμός για HBV:") 
          #Times gia synartisis
          try:
            val = round((df_filtered["embolio_hbv"].value_counts().loc["yes"] / df_filtered["embolio_hbv"].value_counts().sum()) * 100, 1)
          except KeyError:
            val=00.00

          try:
            val2=round((df_filtered["embolio_hbv"].value_counts().loc["no"]/df_filtered["embolio_hbv"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.145, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                        dict(text="ΝΑΙ", x=0.19, y=0.43, font_size=25, showarrow=False),
                                        dict(text=str(val2) + "%", x=0.875, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                        dict(text="ΟΧΙ", x=0.82, y=0.43, font_size=25, showarrow=False),
                                        ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=True,config={'displayModeBar': False})
      with col3:
        with stylable_container(
          key="Loipoi_Deiktes9",
              css_styles="""
                  {
                      background-color: white;
                      border: 1px solid #DCDCDC;
                      border-radius: 10px;
                      padding: 0.5% 2.5% 0.5% 0.05%;
                      
                  }
                  """,
          ):
          st.subheader("Εμβολιασμός για Τέτανο:") 
          #Times gia synartisis
          try:
            val = round((df_filtered["embolio_tetano"].value_counts().loc["yes"] / df_filtered["embolio_tetano"].value_counts().sum()) * 100, 1)
          except KeyError:
            val=00.00

          try:
            val2=round((df_filtered["embolio_tetano"].value_counts().loc["no"]/df_filtered["embolio_tetano"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          #Call of the function
          fig_two_cat_pie=two_cat_pie (val,val2)

          # Customazation of the fig
          # Customazation of the fig
          fig_two_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.145, y=0.55, font_size=35,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                        dict(text="ΝΑΙ", x=0.19, y=0.43, font_size=25, showarrow=False),
                                        dict(text=str(val2) + "%", x=0.875, y=0.55, font_size=35,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                        dict(text="ΟΧΙ", x=0.82, y=0.43, font_size=25, showarrow=False),
                                        ], showlegend=False)
          #Show the plot
          st.plotly_chart(fig_two_cat_pie, use_container_width=True,config={'displayModeBar': False})
  ################################################################################################################################################################

  ##################################################################################################################################################################
  ##################################################################################################################################################################
    
  #Εργασιακή Ικανοποίηση - Section:
  elif choose== "Εργασιακή Ικανοποίηση":
    with stylable_container(
      key="Loipoi_Deiktes_title",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Εργασιακή Ικανοποίηση:")
    if (df_filtered["id_ergazomenou"].nunique()<privacy_limit):
      st.warning(warning_message,icon="⚠️")
    else:
      #dynamic_filters.display_df()
  #################################################################################################################################################################
      
      # 1:
      with stylable_container(
        key="Ergasiaki_Ikanopoihsh",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Εκτίμηση εργασιακής ικανοποίησης (Job Satisfaction Survey questionnaire):")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["ektimisi_ergasiakis_ikanopioisis_CAT"].value_counts().loc["ΙΚΑΝΟΠΟΙΗΣΗ"]/df_filtered["ektimisi_ergasiakis_ikanopioisis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["ektimisi_ergasiakis_ikanopioisis_CAT"].value_counts().loc["ΑΜΦΙΘΥΜΙΑ"]/df_filtered["ektimisi_ergasiakis_ikanopioisis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["ektimisi_ergasiakis_ikanopioisis_CAT"].value_counts().loc["ΔΥΣΑΡΕΣΚΕΙΑ"]/df_filtered["ektimisi_ergasiakis_ikanopioisis_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          #Call of the function
          fig_three_cat_pie=three_cat_pie (val,val2,val3)

          # Customazation of the fig
          # Customazation of the fig
          fig_three_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.09, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΙΚΑΝΟΠΟΙΗΣΗ", x=0.055, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.5, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΑΜΦΙΘΥΜΙΑ", x=0.497, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.92, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΔΥΣΑΡΕΣΚΕΙΑ", x=0.935, y=0.45, font_size=20, showarrow=False),
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_three_cat_pie, use_container_width=False,config={'displayModeBar': False})
          
        with col2:
            #Times gia sinartisi
            value=df_filtered["ektimisi_ergasiakis_ikanopioisis"]
          
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
      #################################################################################################################################################################
      
      # 1:
      with stylable_container(
        key="Ergasiaki_Ikanopoihsh2",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    padding: 0.5% 2.5% 0.5% 0.5%;
                    
                }
                """,
        ):
      #with st.container(border=True):
        st.subheader("Εκτίμηση εργασιακού άγχους (Questionario di Valutazione dello Stress Occupazionale) - Συνολικό Σκορ:")
        col1,col2=st.columns(2)
        with col1:
          #Times gia synartisi
          try:
            val=round((df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().loc["ΑΠΟΥΣΙΑ ΕΡΓΑΣΙΑΚΟΥ ΑΓΧΟΥΣ"]/df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val=00.00
          
          try:
            val2=round((df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().loc["ΗΠΙΟ ΕΡΓΑΣΙΑΚΟ ΑΓΧΟΣ"]/df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val2=00.00

          try:
            val3=round((df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().loc["ΜΕΤΡΙΟ ΕΡΓΑΣΙΑΚΟ ΑΓΧΟΣ"]/df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val3=00.00

          try:
            val4=round((df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().loc["ΣΟΒΑΡΟ ΕΡΓΑΣΙΑΚΟ ΑΓΧΟΣ"]/df_filtered["ektimisi_agxous_sunolo_CAT"].value_counts().sum())*100,1)
          except KeyError:
            val4=00.00

          #Call of the function
          fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

          # Customazation of the fig
          fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                          dict(text="ΑΠΟΥΣΙΑ", x=0.05, y=0.45, font_size=19, showarrow=False),
                                          dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                          dict(text="ΗΠΙΟ", x=0.365, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΜΕΤΡΙΟ", x=0.63, y=0.45, font_size=20, showarrow=False),
                                          dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                          dict(text="ΣΟΒΑΡΟ", x=0.95, y=0.45, font_size=20, showarrow=False)
                                          ], showlegend=False)

          #Show the plot
          st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

          with col2:
            #Times gia sinartisi
            value=df_filtered["ektimisi_agxous_sunolo"]
            
            #Call of the function
            fig_kpis_hist=kpis_hist(value)

            #Show the plot:
            st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})

  #################################################################################################################################################################
  #################################################################################################################################################################

  #Εργατικά Ατυχήματα-Απουσιασμός - Section:
  elif choose== "Εργατικά Ατυχήματα-Απουσιασμός":
    #Ypologismos Deiktwn Ergatikwn Atyximatwn:

    #Δείκτης συχνότητας (ΔΣ) εργατικών ατυχημάτων
    DS=(df_filtered["plhthos_ergatikvn_atyximaton"].sum()/df_filtered["sunolo_anthropooron_ergazomenou"].sum())*1000000

    #Δείκτης επίπτωσης (ΔΕ) εργατικών ατυχημάτων
    DE=(df_filtered["plhthos_ergatikvn_atyximaton"].sum()/df_filtered["id_ergazomenou"].nunique())*1000

    #Δείκτης σοβαρότητας (ΔΣΟ) εργατικών ατυχημάτων
    DSO=(df_filtered["plhthos_xamenwn_anthropooron"].sum()/df_filtered["sunolo_anthropooron_ergazomenou"].sum())*1000

    #Ποσοστό απουσιών
    apousies_percentage=(df_filtered["synolikos_arithmos_hmervn_apousias"].sum()/df_filtered["synolikos_arithmos_ergasimon_hmeron"].sum())*100

    #Ρυθμός απουσιών
    rithmos_apousiwn=(df_filtered["synolikos_arithmos_hmervn_apousias"].sum()/df_filtered["id_ergazomenou"].nunique())*100

    with stylable_container(
      key="Atiximata",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Εργατικά Ατυχήματα-Απουσιασμός:")
    if (df_filtered["id_ergazomenou"].nunique()<privacy_limit):
      st.warning(warning_message,icon="⚠️")
    else:
      #dynamic_filters.display_df()
      col1,col2=st.columns([0.3,0.7])
      with col1:
        with stylable_container(
        key="Ergatika",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:pading:0% 0% 0% 0% 0%;
                }
                """,
        ):
          fig=go.Figure(go.Indicator(
                        value=df_filtered["plhthos_ergatikvn_atyximaton"].sum(),
                        align="center",
                        number={"font": {"size": 60,"color":"#379683"}},
                        title={"text":"Πλήθος εργατικών<br>ατυχημάτων:","font":{"size":25,"color":"gray"},"align":"center"}
                        ))
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
          st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})
      with col2:
        with stylable_container(
        key="Ergatika2",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:0% 5% 0% 0% 5%;
                }
                """,
        ):
          fig=px.bar(df_filtered,
                    x="xoros_ergasias",
                    y="plhthos_ergatikvn_atyximaton",
                    text_auto=True,
                    width=900,
                    hover_data={"xoros_ergasias":True,"plhthos_ergatikvn_atyximaton":True},
                    labels={"xoros_ergasias":"Χώρος Εργασίας","plhthos_ergatikvn_atyximaton":"Πλήθος Εργατικών Ατυχημάτων"}
                    )
          fig.update_traces(marker_color='#379683',opacity=0.8)
          fig.update_traces(textfont_size=16)
          fig.update_layout(hoverlabel_font_size=16)
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
          fig.update_layout(xaxis_title="Χώρος Εργασίας",yaxis_title="Πλήθος Εργατικών Ατυχημάτων",title="")
          st.write(fig)

      col1,col2,col3,col4,col5=st.columns(5)
      with col1:
        with stylable_container(
        key="Ergatika1",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:pading:0% 0% 0% 0% 0%;
                }
                """,
        ):
          fig=go.Figure(go.Indicator(
                        value=DS,
                        align="center",
                        number={"font": {"size": 50,"color":"#379683"}},
                        title={"text":"Δείκτης συχνότητας<br>εργατικών ατυχημάτων<br>(ΔΣ):","font":{"size":25,"color":"gray"},"align":"center"}
                        ))
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
          st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})
      with col2:
        with stylable_container(
        key="Ergatika2",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:0% 0% 0% 0% 0%;
                }
                """,
        ):
          fig=go.Figure(go.Indicator(
                        value=DE,
                        align="center",
                        number={"font": {"size": 50,"color":"#379683"}},
                        title={"text":"Δείκτης επίπτωσης<br>εργατικών ατυχημάτων<br>(ΔΕ):","font":{"size":25,"color":"gray"},"align":"center"}
                        ))
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
          st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})
      with col3:
        with stylable_container(
        key="Ergatika3",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:
                }
                """,
        ):
          fig=go.Figure(go.Indicator(
                        value=DSO,
                        align="center",
                        number={"font": {"size": 50,"color":"#379683"}},
                        title={"text":"Δείκτης σοβαρότητας<br>εργατικών ατυχημάτων<br>(ΔΣΟ):","font":{"size":25,"color":"gray"},"align":"center"}
                        ))
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
          st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})

      with col4:
        with stylable_container(
        key="Ergatika4",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:
                }
                """,
        ):
          fig=go.Figure(go.Indicator(
                        value=round(apousies_percentage,1),
                        align="center",
                        number={"font": {"size": 50,"color":"#379683"}},
                        title={"text":"Ποσοστό απουσιών<br>(%):","font":{"size":25,"color":"gray"},"align":"center"}
                        ))
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
          st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})
      with col5:
        with stylable_container(
        key="Ergatika5",
            css_styles="""
                {
                    background-color: white;
                    border: 1px solid #DCDCDC;
                    border-radius: 10px;
                    pading:
                }
                """,
        ):
          fig=go.Figure(go.Indicator(
                        value=rithmos_apousiwn,
                        align="center",
                        number={"font": {"size": 50,"color":"#379683"}},
                        title={"text":"Ρυθμός απουσιών:","font":{"size":25,"color":"gray"},"align":"center"}
                        ))
          fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white')
          st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})
      with stylable_container(
          key="Ergastiriakes1",
              css_styles="""
                  {
                      background-color: white;
                      border: 1px solid #DCDCDC;
                      border-radius: 10px;
                      padding: 0.5% 2.5% 0.5% 0.5%;
                      
                  }
                  """,
          ):
        #with st.container(border=True):
          st.subheader("Broadford factor (Β):")
          col1,col2=st.columns(2)
          with col1:
            #Times gia synartisi
            try:
              val=round((df_filtered["broadford_factor_CAT"].value_counts().loc["ΤΥΠΙΚΗ ΒΑΘΜΟΛΟΓΙΑ"]/df_filtered["broadford_factor_CAT"].value_counts().sum())*100,1)
            except KeyError:
              val=00.00
            
            try:
              val2=round((df_filtered["broadford_factor_CAT"].value_counts().loc["ΟΡΙΟ ΑΝΗΣΥΧΙΑΣ Ή ΠΑΡΑΚΟΛΟΥΘΗΣΗΣ"]/df_filtered["broadford_factor_CAT"].value_counts().sum())*100,1)
            except KeyError:
              val2=00.00

            try:
              val3=round((df_filtered["broadford_factor_CAT"].value_counts().loc["ΑΝΗΣΥΧΙΑ, ΣΤΕΝΟΤΕΡΗ ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΚΑΙ ΠΙΘΑΝΗ ΠΡΟΦΟΡΙΚΗ ΠΡΟΕΙΔΟΠΟΙΗΣΗ"]/df_filtered["broadford_factor_CAT"].value_counts().sum())*100,1)
            except KeyError:
              val3=00.00

            try:
              val4=round((df_filtered["broadford_factor_CAT"].value_counts().loc["ΑΠΑΙΤΟΥΝΤΑΙ ΠΕΡΑΙΤΕΡΩ ΕΝΕΡΓΕΙΕΣ"]/df_filtered["broadford_factor_CAT"].value_counts().sum())*100,1)
            except KeyError:
              val4=00.00

            #Call of the function
            fig_four_cat_pie=four_cat_pie (val,val2,val3,val4)

            # Customazation of the fig
            fig_four_cat_pie.update_layout(annotations=[dict(text=str(val) + "%", x=0.052, y=0.55, font_size=30,font=dict(color="rgb(113,209,145)"), showarrow=False),
                                            dict(text="ΤΥΠΙΚO ΣΚΟΡ", x=0.022, y=0.45, font_size=19, showarrow=False),
                                            dict(text=str(val2) + "%", x=0.373, y=0.55, font_size=30,font=dict(color="rgba(255, 127, 14,0.8)"), showarrow=False),
                                            dict(text="ΟΡΙΟ ΑΝΗΣΥΧ.", x=0.37, y=0.45, font_size=20, showarrow=False),
                                            dict(text=str(val3) + "%", x=0.635, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                            dict(text="ΑΝΗΣΥΧΙΑ", x=0.63, y=0.45, font_size=20, showarrow=False),
                                            dict(text=str(val4) + "%", x=0.955, y=0.55, font_size=30,font=dict(color="rgba(255,43,43,0.8)"), showarrow=False),
                                            dict(text="ΣΟΒΑΡΗ<br>ΑΝΗΣΥΧ.", x=0.95, y=0.4, font_size=20, showarrow=False)
                                            ], showlegend=False)

            #Show the plot
            st.plotly_chart(fig_four_cat_pie, use_container_width=False,config={'displayModeBar': False})

            with col2:
              #Times gia sinartisi
              value=df_filtered["broadford_factor"]
              
              #Call of the function
              fig_kpis_hist=kpis_hist(value)

              #Show the plot:
              st.plotly_chart(fig_kpis_hist, use_container_width=False,config={'displayModeBar': False})
        
  #################################################################################################################################################################
  #################################################################################################################################################################

  #Extra Statistics - Section:
  elif choose== "Συγκρίσεις Δεικτών":
    with stylable_container(
      key="ExtraStatistics",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Συγκρίσεις Δεικτών:")
    #dynamic_filters.display_df()

    #2: Container with overview statistics for Gender:
    with stylable_container(
      key="AnaFylo",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding: 0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.subheader("Συγκρίσεις Δεικτών ανά Φύλο:")
      
      #Selection of columns end with "_CAT":
      cat_columns=[]
      for col in df.columns:
        if col.endswith("_CAT"):
          cat_columns.append(col)
      
      #Creation of selectBox for the user:    
      with st.container(border=True):
        value=st.selectbox("Επιλέξτε Δείκτη:",options=cat_columns)
      
      #Set the color map for the Barplots:
      palette_colors = px.colors.qualitative.Set3
      #palette_colors = px.colors.sequential.Viridis
      
      #Creation of DataFrame per Gender:
      extra_stats_sex=df.groupby(["gender",value])[value].count()
      extra_stats_sex.name="count"
      extra_stats_sex_df=extra_stats_sex.to_frame()
      extra_stats_sex_df=extra_stats_sex_df.reset_index()
      total_counts_sex=extra_stats_sex_df.groupby("gender")["count"].transform("sum")
      extra_stats_sex_df["count(%)"]=round((extra_stats_sex_df["count"]/total_counts_sex)*100,1)
      st.write(extra_stats_sex_df)

      #Creation of Grouped Barplot according to Gender
      fig =px.histogram(
        extra_stats_sex_df,
        x="gender",
        y="count(%)",
        color=value,
        height=600,
        width=900,
        barmode="group",
        hover_data={"gender":True,"count(%)":True},
        labels={"gender":"Φύλο","count(%)":"Ποσοστό Εργαζομένων (%)"},
        text_auto=True,
        color_discrete_sequence=palette_colors)
      fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
      fig.update_layout(hoverlabel_font_size=16)
      fig.update_traces(textfont_size=16)
      fig.update_layout(legend_title_font_size=15, legend_font_size=15)
      fig.update_layout(xaxis_title=value,yaxis_title="Ποσοστό Εργαζομένων (%)",title="")
      st.write(fig,use_container_width=True) 
        
    #2: Container with overview statistics for Working Space:
    with stylable_container(
    key="AnaXwro",
        css_styles="""
            {
                background-color: white;
                border: 1px solid #DCDCDC;
                border-radius: 10px;
                padding: 0.5% 0.5% 2% 0.5%;
                
            }
            """,
    ):
      st.subheader("Συγκρίσεις Δεικτών ανά Χώρο Εργασίας:")
      with st.container(border=True):
        value=st.selectbox("Επιλέξτε Δείκτη: ",options=cat_columns)
      #Creation of DataFrame per Working Sector:
      extra_stats_space=df.groupby(["xoros_ergasias",value])[value].count()
      extra_stats_space.name="count"
      extra_stats_space_df=extra_stats_space.to_frame()
      extra_stats_space_df=extra_stats_space_df.reset_index()
      total_counts_space=extra_stats_space_df.groupby("xoros_ergasias")["count"].transform("sum")
      extra_stats_space_df["count(%)"]=round((extra_stats_space_df["count"]/total_counts_space)*100,1)
      st.write(extra_stats_space_df)

      #Creation of Grouped Barplot according to space:
      fig =px.histogram(
            extra_stats_space_df,
            x="xoros_ergasias",
            y="count(%)",
            color=value,
            height=600,
            width=900,
            barmode="group",
            hover_data={"xoros_ergasias":True,"count(%)":True},
            labels={"xoros_ergasias":"Χώρος Εργασίας","count":"Ποσοστό Εργαζομένων"},
            text_auto=True,
            color_discrete_sequence=palette_colors)
      fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
      fig.update_layout(xaxis_title=value,yaxis_title="Ποσοστό Εργαζομένων (%)",title="")
      fig.update_layout(hoverlabel_font_size=16)
      fig.update_traces(textfont_size=16)
      fig.update_layout(legend_title_font_size=15, legend_font_size=15)
      st.write(fig,use_container_width=True)

    #2: Container with overview statistics for exposure years:
    with stylable_container(
    key="AnaEkthesi",
        css_styles="""
            {
                background-color: white;
                border: 1px solid #DCDCDC;
                border-radius: 10px;
                padding: 0.5% 0.5% 2% 0.5%;
                
            }
            """,
    ):
      st.subheader("Συγκρίσεις Δεικτών ανά Έτη Έκθεσης στην παρούσα θέση:")
      with st.container(border=True):
        value=st.selectbox("Επιλέξτε Δείκτη:  ",options=cat_columns)
      #Creation of DataFrame per Working Sector:
      extra_stats_ekthesi=df.groupby(["eth_ekthesis",value])[value].count()
      extra_stats_ekthesi.name="count"
      extra_stats_ekthesi_df=extra_stats_ekthesi.to_frame()
      extra_stats_ekthesi_df=extra_stats_ekthesi_df.reset_index()
      total_counts_ekthesi=extra_stats_ekthesi_df.groupby("eth_ekthesis")["count"].transform("sum")
      extra_stats_ekthesi_df["count(%)"]=round((extra_stats_ekthesi_df["count"]/total_counts_ekthesi)*100,1)
      st.write(extra_stats_ekthesi_df)

      #Creation of Grouped Barplot according to space:
      fig =px.histogram(
            extra_stats_ekthesi_df,
            x="eth_ekthesis",
            y="count(%)",
            color=value,
            height=600,
            width=900,
            barmode="group",
            hover_data={"eth_ekthesis":True,"count(%)":True},
            labels={"eth_ekthesis":"Έτη έκθεσης","count(%)":"Ποσοστό Εργαζομένων (%)"},
            text_auto=True,
            color_discrete_sequence=palette_colors)
      fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
      fig.update_layout(xaxis_title=value,yaxis_title="Ποσοστό Εργαζομένων (%)",title="")
      fig.update_xaxes(categoryorder='array', categoryarray=["<1 έτος","3-5 έτη"])
      fig.update_layout(hoverlabel_font_size=16)
      fig.update_traces(textfont_size=16)
      fig.update_layout(legend_title_font_size=15, legend_font_size=15)
      st.write(fig,use_container_width=True)

  #################################################################################################################################################################
  #################################################################################################################################################################

  #Πίνακας Δεδομένων - Section:
  elif choose== "Πίνακας Δεδομένων":
    with stylable_container(
      key="Pinakas_Dedomenwn",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding:0.5% 0.5% 2% 0.5%;
                  
              }
              """,
      ):
      st.title("Πίνακας Δεδομένων:")
    with stylable_container(
      key="Expander",
          css_styles="""
              {
                  background-color: white;
                  border: 1px solid #DCDCDC;
                  border-radius: 10px;
                  padding:;
                  font-size:30px;
                  
              }
              """,
      ):
        with st.expander("Προβολή Αναλυτικού Πίνακα Δεδομένων:"):
          st.dataframe(df_filtered,use_container_width=True)
    csv=df_filtered.to_csv().encode("utf-8")
    if st.download_button("Κατέβασμα Δεδομένων σε csv format",csv,file_name="Δείκτες_Υγείας_data.csv",type="primary"):
      st.success("Το αρχείο κατέβηκε με επιτυχία!",icon="✅")
  #################################################################################################################################################################
  #################################################################################################################################################################
def get_url_params():
    query_params = st.experimental_get_query_params()
    role_received = query_params.get("role", [""])[0]
    return role_received
      
if __name__ == "__main__":
    main()
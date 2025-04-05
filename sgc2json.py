"""
File:    sgc2json.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Convert SGC shapefiles into JSON for source normalization
         Enforce single-table model

Created on: 2023-06-06
"""

import geopandas as gpd
import pandas as pd
import sys

# read subtype data

sub_df = pd.read_json(r"C:\Users\barisma\Documents\odhf\sources\HealthFacilities\sources_v2\sgc_subtypes.json", orient="records")

csd_df = gpd.read_file(r"\\fld6filer\fichiersGEOfiles\Geographie_2021_Geography\Spatial_Info_Products-Produits_d'info_spatiale\LatLongProjection\DBF\ENG\gcsd000a21a_e.zip")
csd_df = csd_df.drop_duplicates("DGUID")
csd_df.rename(columns={"DGUID": "dguid", "CSDUID": "sgc_uid", "CSDNAME": "sgc_name_en"}, inplace=True)

csd_df = csd_df.merge(sub_df[sub_df["sgc_type_uid"] == 6], left_on="CSDTYPE", right_on="sgc_subtype_abbr", how="left").fillna("")

#cds_df[["DGUID", "CDUID", "CDNAME", "CDTYPE"]].to_json("csd_2021.json", orient="records", force_ascii=False)

cd_df = gpd.read_file(r"\\fld6filer\fichiersGEOfiles\Geographie_2021_Geography\Spatial_Info_Products-Produits_d'info_spatiale\LatLongProjection\DBF\ENG\gcd_000a21a_e.zip")
cd_df = cd_df.drop_duplicates("DGUID")
cd_df.rename(columns={"DGUID": "dguid", "CDUID": "sgc_uid", "CDNAME": "sgc_name_en"}, inplace=True)

cd_df = cd_df.merge(sub_df[sub_df["sgc_type_uid"] == 5], left_on="CDTYPE", right_on="sgc_subtype_abbr", how="left").fillna("")

#cd_df[["DGUID", "CDUID", "CDNAME", "CDTYPE"]].to_json("cd_2021.json", orient="records", force_ascii=False)

cma_df = gpd.read_file(r"\\fld6filer\fichiersGEOfiles\Geographie_2021_Geography\Spatial_Info_Products-Produits_d'info_spatiale\LatLongProjection\DBF\ENG\gcma000a21a_e.zip")
cma_df = cma_df.drop_duplicates("DGUID")
cma_df.rename(columns={"DGUID": "dguid", "CMAUID": "sgc_uid", "CMANAME": "sgc_name_en"}, inplace=True)

# clean up multipart CMAs
cma_df.loc[cma_df["dguid"] == "2021S0504502", "sgc_name_en"] = "Hawkesbury"
cma_df.loc[cma_df["dguid"] == "2021S0504505", "sgc_name_en"] = "Ottawa - Gatineau"
cma_df.loc[cma_df["dguid"] == "2021S0504330", "sgc_name_en"] = "Campbellton"
cma_df.loc[cma_df["dguid"] == "2021S0504840", "sgc_name_en"] = "Lloydminster"


#cma_df.loc[cma_df["sgc_subtype"].isin(["B", "D"]), "sgc_type_uid"] = 13
#cma_df.loc[cma_df["sgc_subtype"] == "K", "sgc_type_uid"] = 14

cma_df = cma_df.merge(sub_df[sub_df["sgc_type_uid"].isin([13,14])], left_on="CMATYPE", right_on="sgc_subtype_abbr", how="left").fillna("")

#cma_df[["DGUID", "CMAUID", "CMANAME", "CMATYPE"]].to_json("cma_2021.json", orient="records", force_ascii=False)

pr_df = gpd.read_file(r"\\fld6filer\fichiersGEOfiles\Geographie_2021_Geography\Spatial_Info_Products-Produits_d'info_spatiale\LatLongProjection\DBF\ENG\gpr_000a21a_e.zip")
pr_df = pr_df.drop_duplicates("DGUID")
pr_df.rename(columns={"DGUID": "dguid", "PRUID": "sgc_uid", "PRENAME": "sgc_name_en", "PRFNAME": "sgc_name_fr"}, inplace=True)
#pr_df["sgc_type_uid"] = 2

pr_df.loc[pr_df["sgc_uid"].astype(int) < 60, "PRTYPE"] = "P"
pr_df.loc[pr_df["sgc_uid"].astype(int) >= 60, "PRTYPE"] = "T"

pr_df = pr_df.merge(sub_df[sub_df["sgc_type_uid"] == 2], left_on="PRTYPE", right_on="sgc_subtype_abbr", how="left").fillna("")

#print(pr_df.info())
#print(pr_df)

#pr_df[["DGUID", "PRUID", "PRENAME", "PRFNAME", "PREABBR", "PRFABBR"]].to_json("pr_2021.json", orient="records", force_ascii=False)

consolidated_df = pd.concat([pr_df, cd_df, cma_df, csd_df], ignore_index=True)

#print(consolidated_df[consolidated_df["sgc_type_uid"].isna()])

#sys.exit()


consolidated_df.sgc_type_uid = consolidated_df.sgc_type_uid.astype(int)

consolidated_df[["dguid", "sgc_uid", "sgc_name_en", "sgc_name_fr", "sgc_type_uid", "sgc_subtype_uid"]].to_json("sgc_consolidated_2021.json", orient="records", force_ascii=False)
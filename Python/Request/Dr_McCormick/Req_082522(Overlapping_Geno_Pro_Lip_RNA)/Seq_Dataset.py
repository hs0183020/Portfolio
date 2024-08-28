import pandas as pd
import datacompy
import pyodbc as pyodbc
from functools import reduce

def extract(database):
    """
    Createds a dataframe from access table IMPACTLAB_A with RRID and LABID.

    Parameters
    ----------
    database : Dataframe
        Access dataframe.

    Returns
    -------
    df : Dataframe
        Returns extracted dataframe from table IMPACTLAB_A with rrid and labid.

    """
    query = "SELECT rrid,labid FROM IMPACTLAB_A"
    cnxn = pyodbc.connect(database)
    df = pd.read_sql(query, cnxn)
    cnxn.close()
    return df
    

def create_main(df_cchc,df_covid,df_syv,df_drs):
    """
    Function that creates the main CCHC dataset

    Parameters
    ----------
    df_cchc : Dataframe
        Main access dataset for Brownsvill, Harlingen and Laredo.
    df_covid : Dataframe
        Covid dataset.
    df_syv : Dataframe
        Salud y Vida dataset.
    df_drs : Dataframe
        DRS dataset.

    Returns
    -------
    df_cchc : Dataframe
        Returns the combined dataset called main CCHC dataset.

    """
    
    df_cchc['labid'] = df_cchc['labid'].str.strip()
    df_cchc['labid'] = df_cchc['labid'].str.upper()
    
    df_cchc['rrid'] = df_cchc['rrid'].str.strip()
    df_cchc['rrid'] = df_cchc['rrid'].str.upper()
    
    df_covid=df_covid[['rrid','labid']]
    df_syv=df_syv[['rrid','labid']]
    #change column headers to lowercase
    df_drs.columns= df_drs.columns.str.lower()
    #keep rrid and labid from DRS dataset
    df_drs=df_drs[['rrid','labid']]
    df_cchc=pd.concat([df_cchc,df_covid,df_syv,df_drs],sort=True,ignore_index=True)
    
    
    return df_cchc

if __name__ == "__main__":
    #bring in all of the datasets into python
    constr_bro = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=\\Uthouston.edu\uthsc\SPH\Research\BrownsvilleSD\public\Diabetes_Core\New_CCHC\Server\BD\CCHC_SERVER_DB.ACCDB;Exclusive=1;Pwd=5167;ExtendedAnsiSQL=1;' 
    constr_har = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=\\UTHOUSTON.EDU\UTHSC\SPH\Research\CRU\Diabetes_Core\New_CCHC\HRL\CCHC_HD_SERVER_DB.ACCDB;Exclusive=1;Pwd=5167;ExtendedAnsiSQL=1;' 
    constr_lar = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=\\UTHOUSTON.EDU\UTHSC\SPH\Research\CRU\Diabetes_Core\New_CCHC\LD\CCHC_SERVER_DB.ACCDB;Exclusive=1;Pwd=5167;ExtendedAnsiSQL=1;'     
    df_covid=pd.read_sas(r'\\uthouston.edu\uthsc\SPH\Research\Studies Data\Covid\covid.sas7bdat',encoding='latin1')
    df_syv=pd.read_sas(r'\\uthouston.edu\uthsc\SPH\Research\Studies Data\SYV_Covid\syv_covid.sas7bdat',encoding='latin1')
    df_drs=pd.read_sas(r'\\uctnascifs.uthouston.edu\uthsc\sph\research\brownsvillesd\public\Diabetes_Core\MSAccess\TEMPDATA\DRS\crldata.sas7bdat',encoding='latin1')
    
    
    #extract only RRID and LABID from these datasets and combine
    df_cchc=pd.concat([extract(constr_bro),extract(constr_har),extract(constr_lar)],sort=True,ignore_index=True)
     

    df_cchc=create_main(df_cchc,df_covid,df_syv,df_drs)
    df_cchc=df_cchc.drop_duplicates(subset=['labid'])
    
    df_geno = pd.read_excel(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Input\CCHC_w_ref_SOL_1KG.4.admixture.xlsx',sheet_name='Sheet1')
    #df_rna = pd.read_excel(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\CCHC_RNAseq_batch_0718.xlsx',sheet_name='Sheet1')
    #used the information that was in the Teams folders
    df_rna2 = pd.read_excel(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Input\RNA manifest overall.xlsx',sheet_name='VU shipment till 2022')
    df_rna3 = pd.read_excel(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Input\RNA manifest overall.xlsx',sheet_name='Othershipment')
    df_lip = pd.read_excel(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Input\Copy of 2020_10_19_CCHC final dataset_corrected Dec 2021.xlsx',sheet_name='Species (pmol_L)')
    df_prot = pd.read_csv(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Input\Q-02751_McCormick_NPX_2022-07-11.csv',sep = ';')
    
    
    #split IID string into RRID and LABID
    df_geno['IID'] = df_geno['IID'].str.strip()
    df_geno['IID'] = df_geno['IID'].str.upper()
    df_temp=df_geno['IID'].str.split('_',n = -1, expand = True)
    df_geno['rrid']=df_temp[0]
    df_geno['labid']=df_temp[1]
    #create has genotype value in dataframe
    df_geno['has_dna_seq'] = 1
    df_geno=df_geno[['rrid','labid','has_dna_seq']]
    
    df_geno.loc[(df_geno['rrid'] == "HA0443") & (df_geno['labid'].isna()), ['rrid', 'labid']] = ["HD0443","HA0131"]
    df_geno.loc[(df_geno['rrid'] == "BD0237") & (df_geno['labid'] == 'BD04237'), "labid"] = "BD4237"
    df_geno.loc[(df_geno['rrid'] == "BD0315") & (df_geno['labid'] == 'BD04315'), "labid"] = "BD4315"
    df_geno.loc[(df_geno['rrid'] == "BD0471") & (df_geno['labid'] == 'DB4471'), "labid"] = "BD4471"
    df_geno.loc[(df_geno['rrid'] == "BD0476") & (df_geno['labid'] == 'BD0476'), "labid"] = "BD4476"
    df_geno.loc[(df_geno['rrid'] == "BD0224") & (df_geno['labid'] == 'BD0224'), "labid"] = "BD4224"
    df_geno.loc[(df_geno['rrid'] == "BD0224") & (df_geno['labid'] == 'BD0224'), "labid"] = "BD4224"
    df_geno.loc[(df_geno['rrid'] == "BD1215") & (df_geno['labid'] == 'BD5212'), "labid"] = "BD5215"
    df_geno.loc[(df_geno['rrid'] == "BD1798") & (df_geno['labid'] == 'BD5789'), "labid"] = "BD5798"
    df_geno.loc[(df_geno['rrid'] == "BD2809") & (df_geno['labid'] == 'BD6808'), "labid"] = "BD6809"
    df_geno.loc[(df_geno['rrid'] == "HD0417") & (df_geno['labid'] == 'HA0177'), "labid"] = "HA0117"
    df_geno.loc[(df_geno['rrid'] == "BD2575") & (df_geno['labid'] == 'BD6599'), "labid"] = "BD6575"
    df_geno.loc[(df_geno['rrid'] == "HD4042") & (df_geno['labid'].isna()), ['rrid', 'labid']] = ["HD0042","HD4042"]
    df_geno.loc[(df_geno['rrid'] == "HD4047") & (df_geno['labid'].isna()), ['rrid', 'labid']] = ["HD0047","HD4047"]
    df_geno.loc[(df_geno['rrid'] == "LD0586") & (df_geno['labid'] == 'LA0308'), "labid"] = "LA0309"

    df_dups=df_geno[df_geno.duplicated(['labid'],keep=False)]
    df_geno=df_geno.drop_duplicates(subset=['labid'])
    compare = datacompy.Compare(df_cchc,df_geno,join_columns=['RRID'])
    
    df_geno=df_geno[['rrid','has_dna_seq']]


    
    #clean up rna file dataset
    df_rna2.columns= df_rna2.columns.str.lower()
    df_rna3.columns= df_rna3.columns.str.lower()
    df_rna2['labid'] = df_rna2['labid'].str.strip()
    df_rna2['labid'] = df_rna2['labid'].str.upper()
    df_rna3['labid'] = df_rna3['labid'].str.strip()
    df_rna3['labid'] = df_rna3['labid'].str.upper()
    
    df_rna=pd.concat([df_rna2[['labid']],df_rna3[['labid']]],sort=True,ignore_index=True)
    df_dups=df_rna[df_rna.duplicated(['labid'], keep=False)]
    df_rna=df_rna.drop_duplicates(subset=['labid'])
    df_rna=df_rna.merge(df_cchc, how='left',on='labid')
    df_rna.loc[(df_rna['labid'] == "BD2767"), "rrid"] = "BD2767"
    df_rna.loc[(df_rna['labid'] == "BD2768"), "rrid"] = "BD2768"
    df_rna.loc[(df_rna['labid'] == "BD2790"), "rrid"] = "BD2790"
    df_rna.loc[(df_rna['labid'] == "BP0011"), ['rrid', 'labid']] = ['BD2891', 'BL0011']
    df_rna.loc[(df_rna['labid'] == "BP0013"), ['rrid', 'labid']] = ['BD2893', 'BL0013']
    df_rna.loc[(df_rna['labid'] == "BP0017"), ['rrid', 'labid']] = ['BD2897', 'BL0017']

    df_rna['has_rna_seq'] = 1
    df_norrid=df_rna[df_rna['rrid'].isna()]
    df_rna=df_rna[~df_rna['rrid'].isna()]

    df_dups=df_rna[df_rna.duplicated(['labid'],keep=False)]
    df_rna=df_rna.drop_duplicates(subset=['labid'])

    compare = datacompy.Compare(df_cchc,df_rna,join_columns=['RRID'])
    
    df_rna=df_rna[['rrid','has_rna_seq']]

    #important to find how many participants have rnaseq 
    #from the 2,499 specimen we only have around 1253 participants
    df_rna=df_rna.drop_duplicates(subset=['rrid'])
    

    
    #clean up lipidomics file dataset
    df_lip.columns= df_lip.columns.str.lower()
    df_lip['labid']=df_lip['sample id']
    df_lip=df_lip[['ms label','labid']]
    df_lip['labid'] = df_lip['labid'].str.strip()
    df_lip['labid'] = df_lip['labid'].str.upper()
    df_lip.loc[(df_lip['ms label'] == "CCHC_02-442_S_E02-V389_BD6766") & (df_lip['labid'] == "BD6766"), "labid"] = "BD6776"
    df_lip.loc[(df_lip['ms label'] == "CCHC_01-445_S_E01-V392_BD6767") & (df_lip['labid'] == "BD6767"), "labid"] = "BD6777"
    df_lip.loc[(df_lip['ms label'] == "CCHC_01-469_S_E01-V414_BD6768") & (df_lip['labid'] == "BD6768"), "labid"] = "BD6778"
    df_lip.loc[(df_lip['ms label'] == "CCHC_04-457_S_E04-V403_BD6768") & (df_lip['labid'] == "BD6768"), "labid"] = "BD6779"
    df_lip.loc[(df_lip['ms label'] == "CCHC_04-085_S_E04-V065_BA0480") & (df_lip['labid'] == "BA0480"), "labid"] = "BA0490"
    df_lip.loc[(df_lip['ms label'] == "CCHC_06-307_S_E06-V266_BA0490") & (df_lip['labid'] == "BA0490"), "labid"] = "BA0480"
    df_lip.loc[(df_lip['ms label'] == "CCHC_05-384_S_E05-V336_BD0622") & (df_lip['labid'] == "BD0622"), "labid"] = "BD0422"
    df_lip['has_lipidomics'] = 1
    df_dups=df_lip[df_lip.duplicated(['labid'], keep=False)]
    df_lip=df_lip.drop_duplicates(subset=['labid'])
    df_lip=df_lip.merge(df_cchc, how='left',on='labid')
    df_norrid=df_lip[df_lip['rrid'].isna()]
    df_lip=df_lip[~df_lip['rrid'].isna()]
    
    compare = datacompy.Compare(df_cchc,df_lip,join_columns=['LABID','RRID'])

    df_lip=df_lip[['rrid','has_lipidomics']]


    df_lip=df_lip.drop_duplicates(subset=['rrid'])
    
    #clean up proteomics file dataset
    df_prot.columns= df_prot.columns.str.lower()
    #drop duplicates
    df_prot=df_prot.drop_duplicates(subset=['sampleid'])    
    df_prot['rrid_len']=df_prot['sampleid'].apply(len)
    df_prot=df_prot[df_prot['rrid_len'] < 10]
    df_prot['labid']=df_prot['sampleid']
    df_prot=df_prot[['olinkid','labid']]
    df_prot['has_proteomics'] = 1
    df_prot=df_prot.merge(df_cchc, how='left',on='labid')
    df_norrid=df_prot[df_prot['rrid'].isnull()]
    
    df_prot=df_prot.drop_duplicates(subset=['rrid'])
    
    df_prot=df_prot[['rrid','has_proteomics']]

    df_temp1 = [df_geno, df_lip, df_prot, df_rna]
    
 
    #merge all DataFrames into one
    df_seq = reduce(lambda  left,right: pd.merge(left,right,on=['rrid'],how='outer'), df_temp1)

    
    #output to excel file
    writer = pd.ExcelWriter(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Output\All_Seq.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    #df_geno_lip.to_excel(writer, sheet_name='Genotype_Lipidomics')
    #df_geno_pro.to_excel(writer, sheet_name='Genotype_Proteomics')
    #df_geno_rna.to_excel(writer, sheet_name='Genotype_RNAseq')

    #df_rna_pro.to_excel(writer, sheet_name='RNAseq_Proteomics')
    #df_rna_lip.to_excel(writer, sheet_name='RNAseq_Lipidomics')
    
    df_seq.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    ######################################################################################
    #  Further Analysis for df_rna_lip. Dr McCormick stated that is seemed like the 
    #  dataset was rather small. I am using compare to further analyze both datasets
    ######################################################################################
    
    compare = datacompy.Compare(df_rna,df_lip,join_columns=['rrid'], 

          
        # Optional, defaults to 'df1'
        df1_name = 'Original',
          
        # Optional, defaults to 'df2'
        df2_name = 'New' 
        )
    
    df_rna_lip2=compare.intersect_rows
    df_rna_lip2=df_rna_lip2.drop_duplicates(subset=['rrid'])
    
    df_rna_not_in_lip=compare.df1_unq_rows
    df_rna_not_in_lip=df_rna_not_in_lip.drop_duplicates(subset=['rrid'])
    df_lip_not_in_rn=compare.df2_unq_rows
    df_lip_not_in_rn=df_lip_not_in_rn.drop_duplicates(subset=['rrid'])
    
    writer = pd.ExcelWriter(r'H:\Python\Req_082522(Overlapping_Geno_Pro_Lip_RNA)\Output\Req_082622(RNA_Lipidomics).xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    df_rna_not_in_lip.to_excel(writer, sheet_name='RNA_notIn_Lipidomics')
    df_lip_not_in_rn.to_excel(writer, sheet_name='Lipidomics_notIn_RNA')
    df_rna_lip2.to_excel(writer, sheet_name='RNAseq_Lipidomics')
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

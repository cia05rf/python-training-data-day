"""module outlining how to connect to abacus and query

"""
import pyodbc
import ibm_db
import ibm_db_dbi
import pandas as pd
from sqlalchemy import create_engine

# Establish connection variables
CONN = {
    "database": "BCUDB",
    "host": "abacusproddbcluster",
    "port": 50001,
    "usr": "",
    "pwd": ""
}

# CONNECT USING IBM-DB
# Create connection string
conn_str = f'DATABASE={CONN["database"]};' \
    f'HOSTNAME={CONN["host"]};' \
    f'PORT={CONN["port"]};' \
    f'PROTOCOL=TCPIP;UID={CONN["usr"]};' \
    f'PWD={CONN["pwd"]};'
# Create an ibm-db connection
ibm_db_conn = ibm_db.connect(
    conn_str, '', ''
)
# Create an ibm-db-dbi connection
ibm_db_dbi_conn = ibm_db_dbi.Connection(ibm_db_conn)
# Use connection to query abacus
df = pd.read_sql("select * from BDC.BROWSING_ORDER limit 100", ibm_db_dbi_conn)
display(df)

# CONNECT USING SQLALCHEMY
# Create connection string
conn_str = f'db2+ibm_db://' \
    f'{CONN["usr"]}:' \
    f'{CONN["pwd"]}@' \
    f'{CONN["host"]}:' \
    f'{CONN["port"]}/' \
    f'{CONN["database"]}'
# Build an engine
engine = create_engine(conn_str)
df = pd.read_sql("select * from BDC.BROWSING_ORDER limit 100", engine)
display(df)
# WARNING - IF ERROR
# NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:db2.ibm_db
# Install ibm-db-sa and then this should work

# CHUNKING
CHUNKSIZE = 1000
# Get a large list
sql = """
    SELECT 
        BTC_CODE,
        SAP_CODE_INT,
        SAP_CODE_VAR,
        SAP_CODE_VAR_P,
        ITEM_CODE,
        ITEM_DESCRIPTION,
        EAN_CODE,
        BRAND_CODE,
        BRAND_DESCRIPTION,
        SUB_BRAND_CODE,
        SUB_BRAND_DESCRIPTION,
        ITEM_INTRODUCTION_DATE,
        ITEM_DELETION_DATE,
        MERCHANDISE_CATEGORY_CODE,
        MERCHANDISE_CATEGORY_DESCRIPTION,
        WAITROSE_LINE_NUMBER,
        VENDOR_NUMBER,
        VENDOR_NAME,
        ITEM_HIERARCHY7_NUMBER,
        ITEM_HIERARCHY7_DESCRIPTION,
        ITEM_HIERARCHY6_NUMBER,
        ITEM_HIERARCHY6_DESCRIPTION,
        ITEM_HIERARCHY5_NUMBER,
        ITEM_HIERARCHY5_DESCRIPTION,
        ITEM_HIERARCHY4_NUMBER,
        ITEM_HIERARCHY4_DESCRIPTION,
        ITEM_HIERARCHY3_NUMBER,
        ITEM_HIERARCHY3_DESCRIPTION,
        ITEM_HIERARCHY2_NUMBER,
        ITEM_HIERARCHY2_DESCRIPTION,
        ITEM_HIERARCHY1_NUMBER,
        ITEM_HIERARCHY1_DESCRIPTION,
        EXCLUSIVE_FLAG,
        OWN_BRAND_CODE,
        STAFF_DISCOUNT_FLAG,
        ADVANTAGE_PROMOTIONS,
        GWP_FLAG,
        OCCASION_CODE,
        OCCASION_DESCRIPTION,
        RETAIL_STATUS,
        DROP_SHIP_FLAG,
        COLLECT_FROM_STORE_FLAG,
        ITEM_TYPE,
        VALID_FROM_DATE,
        VALID_FROM_TIME,
        LADDER,
        SUB_LADDER
    FROM OTH.BROWSING_PRODUCT_INFO
"""
# Run in one go
df = pd.read_sql(sql, engine)
# Now keep the info we want
df = df[["btc_code", "sap_code_var_p"]]
display(df)

# This can be done with chunking
final_df = pd.DataFrame([])
for df in pd.read_sql(sql, engine, chunksize=CHUNKSIZE):
    final_df = pd.concat([
        final_df, df[["btc_code", "sap_code_var_p"]]
    ])
    print("Ran a chunk")
display(final_df)
def xstl_query_term_level_campus(term: str, 
              level:str = 'PS', 
              campus: str = 'MAIN'): 
    """
    This query pulls the exact same information as a XSTL report

    Args: 
        term (str): Term of interest
        level (str): Academic level of interest (PS set as default)
        campus (str): Campus of interest (MAIN set as defaul)

    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.xstl_query_term_level_campus(term = '2022F',
                                            level = 'PS', 
                                            campus = 'MAIN')
    """
    
    query = """
    DECLARE @STAT_DATE AS DATETIME = GETDATE();

    SELECT STC_PERSON_ID AS studentid
        ,FIRST_NAME as first_name
        ,LAST_NAME as last_name
        ,BIRTH_DATE as birth_date
        ,GENDER as gender
        ,STC_ACAD_LEVEL as acad_level
        ,IMMIGRATION_STATUS AS imm_status
        ,CITY AS city
        ,ADDRESS.ZIP AS postal_code
        ,SCS_LOCATION AS location
        ,SUBSTRING(STC_COURSE_NAME, 6, 4) AS program
        ,STC_SECTION_NO AS AAL
        ,STTR_STUDENT_LOAD AS current_load
        ,STTR_USER1 AS tenth_day_load
        ,STC_STATUS AS curr_status
        ,BB.STC_STATUS_DATE AS status_date
    FROM STUDENT_ACAD_CRED AA
    JOIN STC_STATUSES BB ON AA.STUDENT_ACAD_CRED_ID = BB.STUDENT_ACAD_CRED_ID
        AND POS = (
            SELECT TOP 1 POS
            FROM STC_STATUSES
            WHERE STUDENT_ACAD_CRED_ID = AA.STUDENT_ACAD_CRED_ID
                AND STC_STATUS_DATE <= @STAT_DATE
            )
    JOIN STUDENT_COURSE_SEC SCS ON SCS.STUDENT_COURSE_SEC_ID = AA.STC_STUDENT_COURSE_SEC
    JOIN STUDENT_TERMS ON STUDENT_TERMS_ID = STC_PERSON_ID + '*' + STC_TERM + '*' + STC_ACAD_LEVEL
    JOIN PERSON P ON STC_PERSON_ID = P.ID
    JOIN ADDRESS ON ADDRESS_ID = PREFERRED_ADDRESS
    WHERE STC_TERM = '"""+term+"""'
        AND STC_SUBJECT = 'CTRL'
        AND STC_ACAD_LEVEL = '"""+level+"""'
        AND SCS_LOCATION = '"""+campus+"""'
        AND STC_STATUS IN ('A','D','N')
    ORDER BY STC_PERSON_ID
        ,STC_COURSE_NAME
    """
    return query


def xstl_query_term(term: str): 
    """
    This query pulls the exact same information as a XSTL report

    Args: 
        term (str): Term of interest

    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.xstl_query_term(term = '2022F')
    """
    
    query = """
     DECLARE @STAT_DATE AS DATETIME = GETDATE();

    SELECT STC_PERSON_ID AS studentid
        ,FIRST_NAME as first_name
        ,LAST_NAME as last_name
        ,BIRTH_DATE as birth_date
        ,GENDER as gender
        ,STC_ACAD_LEVEL as acad_level
        ,IMMIGRATION_STATUS AS imm_status
        ,CITY AS city
        ,ADDRESS.ZIP AS postal_code
        ,SCS_LOCATION AS location
        ,SUBSTRING(STC_COURSE_NAME, 6, 4) AS program
        ,STC_SECTION_NO AS AAL
        ,STTR_STUDENT_LOAD AS current_load
        ,STTR_USER1 AS tenth_day_load
        ,STC_STATUS AS curr_status
        ,BB.STC_STATUS_DATE AS status_date
    FROM STUDENT_ACAD_CRED AA
    JOIN STC_STATUSES BB ON AA.STUDENT_ACAD_CRED_ID = BB.STUDENT_ACAD_CRED_ID
        AND POS = (
            SELECT TOP 1 POS
            FROM STC_STATUSES
            WHERE STUDENT_ACAD_CRED_ID = AA.STUDENT_ACAD_CRED_ID
                AND STC_STATUS_DATE <= @STAT_DATE
            )
    JOIN STUDENT_COURSE_SEC SCS ON SCS.STUDENT_COURSE_SEC_ID = AA.STC_STUDENT_COURSE_SEC
    JOIN STUDENT_TERMS ON STUDENT_TERMS_ID = STC_PERSON_ID + '*' + STC_TERM + '*' + STC_ACAD_LEVEL
    JOIN PERSON P ON STC_PERSON_ID = P.ID
    JOIN ADDRESS ON ADDRESS_ID = PREFERRED_ADDRESS
    WHERE STC_TERM = '"""+term+"""' 
	AND SCS_LOCATION = 'MAIN'
    ORDER BY STC_PERSON_ID
        ,STC_COURSE_NAME
    """
    return query



def xstl_query_term_program(term: str, 
                            program: str): 
    """
    This query pulls the exact same information as a XSTL report

    Args: 
        term (str): Term of interest
        program (str): program of interest)

    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.xstl_query_term_level_campus(term = '2022F', 
                                            program = 'CPET')
    """
    
    query = """
    DECLARE @STAT_DATE AS DATETIME = GETDATE();

    SELECT STC_PERSON_ID AS studentid
        ,FIRST_NAME as first_name
        ,LAST_NAME as last_name
        ,BIRTH_DATE as birth_date
        ,GENDER as gender
        ,STC_ACAD_LEVEL as acad_level
        ,IMMIGRATION_STATUS AS imm_status
        ,CITY AS city
        ,ADDRESS.ZIP AS postal_code
        ,SCS_LOCATION AS location
        ,SUBSTRING(STC_COURSE_NAME, 6, 4) AS program
        ,STC_SECTION_NO AS AAL
        ,STTR_STUDENT_LOAD AS current_load
        ,STTR_USER1 AS tenth_day_load
        ,STC_STATUS AS curr_status
        ,BB.STC_STATUS_DATE AS status_date
    FROM STUDENT_ACAD_CRED AA
    JOIN STC_STATUSES BB ON AA.STUDENT_ACAD_CRED_ID = BB.STUDENT_ACAD_CRED_ID
        AND POS = (
            SELECT TOP 1 POS
            FROM STC_STATUSES
            WHERE STUDENT_ACAD_CRED_ID = AA.STUDENT_ACAD_CRED_ID
                AND STC_STATUS_DATE <= @STAT_DATE
            )
    JOIN STUDENT_COURSE_SEC SCS ON SCS.STUDENT_COURSE_SEC_ID = AA.STC_STUDENT_COURSE_SEC
    JOIN STUDENT_TERMS ON STUDENT_TERMS_ID = STC_PERSON_ID + '*' + STC_TERM + '*' + STC_ACAD_LEVEL
    JOIN PERSON P ON STC_PERSON_ID = P.ID
    JOIN ADDRESS ON ADDRESS_ID = PREFERRED_ADDRESS
    WHERE STC_TERM = '"""+term+"""'
        AND SUBSTRING(STC_COURSE_NAME, 6, 4) = '"""+program+"""'
        AND STC_SUBJECT = 'CTRL'
        AND STC_STATUS IN ('A','D','N')
    ORDER BY STC_PERSON_ID
        ,STC_COURSE_NAME
    """
    return query


def xstl_gi_query(term:str):
    """
    This query pulls the exact same information as a XSTL report for GI programs

    Args: 
        term (str): Term of interest

    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.xstl_gi_query(term = '2022F')
    """
    query = """
   DECLARE @STAT_DATE AS DATETIME = GETDATE();

    SELECT STC_PERSON_ID AS studentid
        ,FIRST_NAME as first_name
        ,LAST_NAME as last_name
        ,BIRTH_DATE as birth_date
        ,GENDER as gender
        ,STC_ACAD_LEVEL as acad_level
        ,IMMIGRATION_STATUS AS imm_status
        ,CITY AS city
        ,ADDRESS.ZIP AS postal_code
        ,SCS_LOCATION AS location
        ,SUBSTRING(STC_COURSE_NAME, 6, 4) AS program
        ,STC_SECTION_NO AS AAL
        ,STTR_STUDENT_LOAD AS current_load
        ,STTR_USER1 AS tenth_day_load
        ,STC_STATUS AS curr_status
        ,BB.STC_STATUS_DATE AS status_date
    FROM STUDENT_ACAD_CRED AA
    JOIN STC_STATUSES BB ON AA.STUDENT_ACAD_CRED_ID = BB.STUDENT_ACAD_CRED_ID
        AND POS = (
            SELECT TOP 1 POS
            FROM STC_STATUSES
            WHERE STUDENT_ACAD_CRED_ID = AA.STUDENT_ACAD_CRED_ID
                AND STC_STATUS_DATE <= @STAT_DATE
            )
    JOIN STUDENT_COURSE_SEC SCS ON SCS.STUDENT_COURSE_SEC_ID = AA.STC_STUDENT_COURSE_SEC
    JOIN STUDENT_TERMS ON STUDENT_TERMS_ID = STC_PERSON_ID + '*' + STC_TERM + '*' + STC_ACAD_LEVEL
    JOIN PERSON P ON STC_PERSON_ID = P.ID
    JOIN ADDRESS ON ADDRESS_ID = PREFERRED_ADDRESS
    WHERE STC_TERM = '"""+term+"""'
        AND STC_ACAD_LEVEL = 'GI'
        AND SCS_LOCATION = 'MAIN'
    ORDER BY STC_PERSON_ID
        ,STC_COURSE_NAME

    """
    return query


def xstl_query_term_level(term: str, 
              level:str = 'PS'): 
    """
    This query pulls the exact same information as a XSTL report

    Args: 
        term (str): Term of interest
        level (str): Academic level of interest (PS set as default)

    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.xstl_query_term_level_campus(term = '2022F',
                                            level = 'PS')
    """
    
    query = """
    DECLARE @STAT_DATE AS DATETIME = GETDATE();

    SELECT STC_PERSON_ID AS studentid
        ,FIRST_NAME as first_name
        ,LAST_NAME as last_name
        ,BIRTH_DATE as birth_date
        ,GENDER as gender
        ,STC_ACAD_LEVEL as acad_level
        ,IMMIGRATION_STATUS AS imm_status
        ,CITY AS city
        ,ADDRESS.ZIP AS postal_code
        ,SCS_LOCATION AS location
        ,SUBSTRING(STC_COURSE_NAME, 6, 4) AS program
        ,STC_SECTION_NO AS AAL
        ,STTR_STUDENT_LOAD AS current_load
        ,STTR_USER1 AS tenth_day_load
        ,STC_STATUS AS curr_status
        ,BB.STC_STATUS_DATE AS status_date
    FROM STUDENT_ACAD_CRED AA
    JOIN STC_STATUSES BB ON AA.STUDENT_ACAD_CRED_ID = BB.STUDENT_ACAD_CRED_ID
        AND POS = (
            SELECT TOP 1 POS
            FROM STC_STATUSES
            WHERE STUDENT_ACAD_CRED_ID = AA.STUDENT_ACAD_CRED_ID
                AND STC_STATUS_DATE <= @STAT_DATE
            )
    JOIN STUDENT_COURSE_SEC SCS ON SCS.STUDENT_COURSE_SEC_ID = AA.STC_STUDENT_COURSE_SEC
    JOIN STUDENT_TERMS ON STUDENT_TERMS_ID = STC_PERSON_ID + '*' + STC_TERM + '*' + STC_ACAD_LEVEL
    JOIN PERSON P ON STC_PERSON_ID = P.ID
    JOIN ADDRESS ON ADDRESS_ID = PREFERRED_ADDRESS
    WHERE STC_TERM = '"""+term+"""'
        AND STC_SUBJECT = 'CTRL'
        AND STC_ACAD_LEVEL = '"""+level+"""'
        AND STC_STATUS IN ('A','D','N')
    ORDER BY STC_PERSON_ID
        ,STC_COURSE_NAME
    """
    return query
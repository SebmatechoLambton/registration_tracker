import pandas as pd

def rooms_usage(term: str, 
                cnxn):
    """
    This functions retrieves the data from room ocupation and further information.

    Args: 
        term (str): Term of interest
    
    Returns: 
        dataframe (pd.DataFrame): DataFrame containing data of interest for term of interest
        cnxn (pyodbc.Connection): Conection to run the query (set as default to production)

    Example Usage: 
        rooms_usage(term = '2022F', 
                    cnxn = cnxn)
    """
    # Writing the query
    query = """
 WITH all_data
AS (
	SELECT css.COURSE_SECTIONS_ID AS section_id
		,CSM_BLDG AS building
        ,SEC_SCHOOLS as school
		,CSM_ROOM AS room
		,css.SEC_NAME AS full_sec_name
        ,SEC_FACULTY_INFO as faculty
		,css.SEC_SUBJECT AS subject
		,css.SEC_COURSE_NO AS course_no
		,css.SEC_NO AS section_no
		--,css.SEC_LOCATION AS location
		,crs.CRS_TITLE AS title
		,(
			CASE 
				WHEN SUBSTRING(crs.CRS_NO, 5, 1) = 'L'
					THEN 'Y'
				ELSE 'N'
				END
			) AS lab_flag
		,SEC_CAPACITY AS capacity
		,(
			SELECT COUNT(DISTINCT ls.SEC_ACTIVE_STUDENTS)
			FROM COURSE_SECTIONS_LS AS ls
			WHERE ls.COURSE_SECTIONS_ID = css.COURSE_SECTIONS_ID
				AND ls.SEC_ACTIVE_STUDENTS IS NOT NULL
			) AS student_count
		,SEC_ACAD_LEVEL AS academic_level
		,CSM_FREQUENCY AS frequency
		,CSM_MONDAY AS monday
		,CSM_TUESDAY AS tuesday
		,CSM_WEDNESDAY AS wednesday
		,CSM_THURSDAY AS thursday
		,CSM_FRIDAY AS friday
		,CSM_SATURDAY AS saturday
		,CSM_SUNDAY AS sunday
		,CSM_START_TIME AS start_time
		,CSM_END_TIME AS end_time
		,SEC_START_DATE AS start_date
		,SEC_END_DATE AS end_date
		,css.SEC_TERM AS term
	FROM COURSE_SECTIONS AS css
	LEFT JOIN COURSES AS crs ON (crs.COURSES_ID = css.SEC_COURSE)
	LEFT JOIN COURSE_SECTIONS_LS AS csm ON csm.COURSE_SECTIONS_ID = css.COURSE_SECTIONS_ID
	LEFT JOIN COURSE_SEC_MEETING ON SEC_MEETING = COURSE_SEC_MEETING_ID
	LEFT JOIN SEC_STATUSES sst ON sst.COURSE_SECTIONS_ID = css.COURSE_SECTIONS_ID
	WHERE css.SEC_TERM = '"""+term+"""'
		AND (
			css.SEC_SUBJECT IS NULL
			OR css.SEC_SUBJECT != 'CTRL'
			)
		/* code way of saying "take the numeric left side of SEC_NO and compare using that" */
		AND sst.POS = 1
		AND SEC_LOCATION = 'MAIN'
		AND CSM_ROOM IS NOT NULL
	)
	,waitlist
AS (
SELECT WAIT_COURSE_SECTION AS section_id
		,COUNT(*) AS waitlisted
	FROM WAIT_LIST
	WHERE WAIT_TERM = '"""+term+"""'
	AND WAIT_STATUS = 'A'
	GROUP BY WAIT_COURSE_SECTION
	)
SELECT building
	,room, full_sec_name, faculty, school, subject, course_no, section_no
	,title, lab_flag, capacity, student_count
	,ISNULL(waitlisted, 0) AS waitlisted
	,academic_level ,frequency
	,monday ,tuesday ,wednesday ,thursday ,friday ,saturday ,sunday
	,start_time ,end_time ,start_date ,end_date ,term
FROM all_data
LEFT JOIN waitlist ON all_data.section_id = waitlist.section_id
    """
    # Run query Query
    query = pd.read_sql(query, cnxn)
    
    return(query)

def xstl_query_term(term: str, 
                    cnxn): 
    """
    This query pulls the exact information as XSTL report for MAIN campus

    Args: 
        term (str): Term of interest
        cnxn (pyodbc.Connection): Conection to run the query (set as default to production)

    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.xstl_query_term(term = '2022F',
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
        AND SCS_LOCATION = 'MAIN'
        AND STC_STATUS IN ('A','D','N')
    ORDER BY STC_PERSON_ID
        ,STC_COURSE_NAME
    """
    # Run query Query
    query = pd.read_sql(query, cnxn)

    return query


def payments_query(term, cnxn):
    """
    This query retrieves student payments or waivers of interest
    
    Args: 
        term (str): Term of interest
        cnxn (pyodbc.Connection): Conection to run the query (set as default to production)
    Returns: 
        query (str): Output raw query to be passed through connection

    Example usage: 
        utils.payments_query(term = '2022F')
    
    """

    
    query = """
DECLARE @TERM AS VARCHAR(10) = '"""+term+"""';

WITH T1 (
	STC_PERSON_ID
	,IMMIGRATION_STATUS
	,program
	,aal
	,Course_Name
	,SCS_LOCATION
	,STNT
	,STNT_Date
	)
AS (
	SELECT STC_PERSON_ID
		,IMMIGRATION_STATUS
		,substring(STC_COURSE_NAME, 6, 4) AS program
		,STC_SECTION_NO AS aal
		,STC_COURSE_NAME + '-' + STC_SECTION_NO AS 'CTRL Course'
		,SCS_LOCATION
		,cast((
				SELECT STTN_NOTES + ' '
				FROM STTN_TERM_NOTES
				WHERE STUDENT_TERM_NOTES_ID = STC_PERSON_ID + '*' + STC_TERM
				FOR XML path('')
				) AS VARCHAR(100)) AS STNT
		,cast((
				SELECT STTN_DATES + ' '
				FROM STTN_TERM_NOTES
				WHERE STUDENT_TERM_NOTES_ID = STC_PERSON_ID + '*' + STC_TERM
				FOR XML path('')
				) AS VARCHAR(100)) AS STNT_Date
	FROM STUDENT_ACAD_CRED
	INNER JOIN STC_STATUSES ON STUDENT_ACAD_CRED.STUDENT_ACAD_CRED_ID = STC_STATUSES.STUDENT_ACAD_CRED_ID
	INNER JOIN STUDENT_COURSE_SEC ON STUDENT_COURSE_SEC_ID = STC_STUDENT_COURSE_SEC
	LEFT JOIN STTN_TERM_NOTES ON STUDENT_TERM_NOTES_ID = STC_PERSON_ID + '*' + STC_TERM
	LEFT JOIN PERSON ON ID = STC_PERSON_ID
	WHERE STC_TERM = @TERM
		AND STC_SUBJECT = 'CTRL'
		AND STC_STATUSES.POS = 1
		AND STC_STATUS IN (
			'N'
			,'A'
			,'D'
			)
		AND SCS_LOCATION = 'MAIN'
		AND STC_ACAD_LEVEL = 'PS'
	)
	,T3 (
	ARP_PERSON_ID
	,ARP_AMT
	,ARP_TERM
	,Pay_Methods
	,ARP_DATE
	,Pay_Methods_Deposit
	)
AS (
	SELECT ARP_PERSON_ID
		,ARP_AMT
		,ARP_TERM
		,cast((
				SELECT RCPT_PAY_METHODS + ' '
				FROM RCPT_NON_CASH
				WHERE CASH_RCPTS_ID = ARP_CASH_RCPT
				FOR XML path('')
				) AS VARCHAR(100)) AS Pay_Methods
		,ARP_DATE
		,cast((
				SELECT RCPT_PAY_METHODS + ' '
				FROM RCPT_NON_CASH
				WHERE CASH_RCPTS_ID = ARD_CASH_RCPT
				FOR XML path('')
				) AS VARCHAR(100)) AS Pay_Methods_Deposit
	FROM AR_PAYMENTS
	LEFT JOIN AR_DEPOSIT_ITEMS ON AR_DEPOSIT_ITEMS_ID = ARP_DEPOSIT_ITEM
	LEFT JOIN AR_DEPOSITS ON AR_DEPOSITS_ID = ARDI_DEPOSIT
	WHERE ARP_TERM = @TERM
		AND ARP_LOCATION = 'MAIN'
	)
	,T4 (
	STUDENT_ID
	,SPONSORSHIP
	,SPONSOR_APPLIED
	)
AS (
	SELECT SPNP_PERSON_ID
		,SPNP_SPONSORSHIP
		,SPONSORED_PERSON_ADDDATE
	FROM SPONSORED_PERSON_LS AA
	LEFT JOIN SPONSORED_PERSON BB ON AA.SPONSORED_PERSON_ID = BB.SPONSORED_PERSON_ID
	WHERE SPNP_TERMS = @TERM
	)
SELECT STC_PERSON_ID AS studentid
	,program
	,aal
	,SPONSORSHIP as sponsorship
	,SPONSOR_APPLIED as sponsorship_applied
	,STNT as stnt
	,STNT_Date as stnt_date
	,ARP_AMT AS payment_amount
	--,ARP_DATE AS payment_date
	--,ARP_TERM as arp_term
	--,Pay_Methods as pay_methods
	--,Pay_Methods_Deposit as pay_methods_deposit
FROM T1
LEFT JOIN T3 ON T1.STC_PERSON_ID = T3.ARP_PERSON_ID
LEFT JOIN T4 ON T1.STC_PERSON_ID = T4.STUDENT_ID
ORDER BY SPONSORSHIP DESC
    """
    query = pd.read_sql(query, cnxn)
    return(query)
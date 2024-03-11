import datetime
import models.task_result
import fastapi
from sqlalchemy import text
import db

router = fastapi.APIRouter(
    prefix='/task_result',
)


@router.get('/{task_result_id}')
async def get_task_result(task_result_id: int):
    query = text("""SELECT 
                tr.ID AS TASK_ID,
                tr.SERIAL_NUMBER,
                tr.START_TIME,
                tr.DURATION,
                tr.TEST_STATUS,
                tr.ACTOR,
                tpb.ID AS BASE_ID,
                tpb.NAME,
                tpb.PARAMETER_TYPE, 
                tpb.PARAMETER_START_TIME, 
                tpb.PARAMETER_DURATION, 
                tpb.COMPARATOR, 
                tpb.PARAMETER_STATUS,
                COALESCE(tpn.ID, tps.ID) AS PARAMETER_ID,
                tpn.VALUE AS VALUE_NUMERIC,
                tpn.LSL,
                tpn.USL,
                tps.VALUE AS VALUE_STRING,
                tps.EXPECTED_VALUE
            FROM task_result tr
            JOIN task_parameter_base tpb ON tr.ID=tpb.TASK_ID 
            LEFT JOIN task_parameter_numeric tpn ON tpb.ID=tpn.PARAMETER_ID 
            LEFT JOIN task_parameter_string tps ON tpb.ID=tps.PARAMETER_ID
            WHERE tr.ID=:task_result_id
            """)
    res = None
    task_result = None
    with db.engine.connect() as conn:
        res = conn.execute(query, {'task_result_id': task_result_id}).mappings()
        res = [x for x in res]
    if res:
        params = []
        task_result = models.task_result.TaskResult(
            id=res[0]['TASK_ID'],
            serial_number=res[0]['SERIAL_NUMBER'],
            start_time=datetime.datetime.fromtimestamp(res[0]['START_TIME']),
            duration=res[0]['DURATION'],
            test_status=res[0]['TEST_STATUS'],
            actor=res[0]['ACTOR'],
            task_parameters=[],
        )
        for row in res:
            task_param = models.task_result.TaskParameter(
                id=row['PARAMETER_ID'],
                task_id=row['TASK_ID'],
                base_id=row['BASE_ID'],
                name=row['NAME'],
                type=row['PARAMETER_TYPE'],
                start_time=row['PARAMETER_START_TIME'],
                duration=row['PARAMETER_DURATION'],
                value_numeric=row['VALUE_NUMERIC'],
                value_string=row['VALUE_STRING'],
                comparator=row['COMPARATOR'],
                lsl=row['LSL'],
                usl=row['USL'],
                expected_value=row['EXPECTED_VALUE'],
                status=row['PARAMETER_STATUS'],
            )
            params.append(task_param)
        task_result.task_parameters = params
    return task_result


@router.post('/')
async def submit_task_result(task_result: models.task_result.TaskResult):
    query = text("""INSERT INTO task_result (SERIAL_NUMBER, START_TIME, DURATION, TEST_STATUS, ACTOR) 
                    VALUES (:serial_number,:start_time,:duration,:test_status,:actor)""")
    base_query = text("""
        INSERT INTO task_parameter_base 
        (TASK_ID, NAME, PARAMETER_TYPE, PARAMETER_START_TIME, PARAMETER_DURATION, COMPARATOR, PARAMETER_STATUS) 
        VALUES (:task_id, :name, :parameter_type, :parameter_start_time, :parameter_duration, :comparator, :parameter_status)
        """)
    numeric_query = text("""
        INSERT INTO task_parameter_numeric
        (TASK_ID, PARAMETER_ID, VALUE, LSL, USL)
        VALUES (:task_id, :parameter_id, :value_numeric, :lsl, :usl)
        """)
    string_query = text("""
        INSERT INTO task_parameter_string
        (TASK_ID, PARAMETER_ID, VALUE, EXPECTED_VALUE)
        VALUES (:task_id, :parameter_id, :value_string, :expected_value)
        """)

    task_result_args = {
        'serial_number': task_result.serial_number,
        'start_time': task_result.start_time.timestamp(),
        'duration': task_result.duration,
        'test_status': task_result.test_status,
        'actor': task_result.actor
    }

    with db.engine.connect() as conn:
        with conn.begin():
            try:
                res = conn.execute(query, task_result_args)
                task_result_id = res.lastrowid
                for param in task_result.task_parameters:
                    param_args = {
                        'task_id': task_result_id,
                        'name': param.name,
                        'parameter_type': param.type,
                        'parameter_start_time': param.start_time.timestamp(),
                        'parameter_duration': param.duration,
                        'comparator': param.comparator,
                        'parameter_status': param.status,
                        'value_numeric': param.value_numeric,
                        'value_string': param.value_string,
                        'lsl': param.lsl,
                        'usl': param.usl,
                        'expected_value': param.expected_value
                    }
                    res = conn.execute(base_query, param_args)
                    base_id = res.lastrowid
                    param_args['parameter_id'] = base_id
                    if param.type == 'numeric':
                        conn.execute(numeric_query, param_args)
                    elif param.type == 'string':
                        conn.execute(string_query, param_args)
                    else:
                        raise RuntimeError('Invalid Type for parameter')
            except:
                conn.rollback()
    return task_result

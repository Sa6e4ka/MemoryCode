from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Users, dialogs
from Logging.LoggerConfig import logger

async def history(session: AsyncSession, data : dict):
    table = dialogs(
        block1_main_quest = data['block1_main_quest'],
        ans1= data['ans1'],
        block1_quest2= data['block1_quest2'],
        ans2= data['ans2'],
        block1_question3= data['block1_question3'],
        ans3= data['ans3'],
        block2_main_quest= data['block2_main_quest'],
        ans4= data['ans4'],
        block2_quest2= data['block2_quest2'],
        ans5= data['ans5'],
        block2_quest3= data['block2_quest3'],
        ans6= data['ans6'],
        block3_main_q= data['block3_main_q'],
        ans7= data['ans7'],
        block3_quest2= data['block3_quest2'],
        ans8= data['ans8'],
        block3_quest3= data['block3_quest3'],
        ans9= data['ans9'],
        ans10= data['ans10']
        )
    logger.info(f"Опрос для {data['name'], data['page_id']} Успешно пройден")
    session.add(table)
    await session.commit()
   


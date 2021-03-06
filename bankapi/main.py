from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import uvicorn

from .service import key
from .routers import account, admin, balance, transcation

app = FastAPI(title='은행 API')

app.include_router(account.router)
app.include_router(admin.router)
app.include_router(balance.router)
app.include_router(transcation.router)


@app.get('/')
def root():
    return {'message': '안녕하세요. 머니 클래스 프로젝트의 은행 API입니다.'}


register_tortoise(
    app,
    db_url=key.url,
    modules={'models': ['bankapi.models.model']},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

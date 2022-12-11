import uvicorn
from app.api import app


if __name__ == '__main__':

    # For server, using uvicorn
    # you can change it, if you have sth better
    uvicorn.run(app, host='0.0.0.0', port=80, log_level='info')

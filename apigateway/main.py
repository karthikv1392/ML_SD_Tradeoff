from apigateway import config

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('apigateway.app:app', host='0.0.0.0', port=int(config.PORT), reload=True)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('ml_engine.app:app', host='0.0.0.0', port=8002, reload=True)
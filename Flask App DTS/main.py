from Website import create_app

app = create_app()

if __name__ == '__main__': #making sure the right main.py file is running
    app.run(host='0.0.0.0', debug=True) #runs the 'app' and debug means update when changes are made
    


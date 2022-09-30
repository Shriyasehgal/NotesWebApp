from website import create_app

app = create_app()

if __name__ == '__main__': # only when we run this file, and not import the file, we are going to execute this file
    app.run(debug = True)  # We want this becuase if we didnot have the condition, this line would run every time we import the main.py file
                            # this line will run the flask application, debug = True means that every tim ewe make a change in the python code, it is going to rerun the webs server

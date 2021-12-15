from department_app import create_app, db

app = create_app()


if __name__ == "__main__":
    import logging
    # logging.basicConfig(filename='logs_rec.log', level=logging.DEBUG,
    #                     format='%(levelname)s %(name)s %(threadName)s : %(message)s @ %(asctime)s')

    # app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)

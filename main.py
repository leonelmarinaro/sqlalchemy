from library_app.scripts.query_data import query_data

class Main:
    def __init__(self):
        self.run()

    def run(self):
        self.data = query_data()
        self.display_data()
    
    def display_data(self):
        print(self.data)

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()
    
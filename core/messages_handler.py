class MessageBaseHandler():

    def check(self, message):
        pass


    def handle(self, message):
        pass
    
    def parse_command(self, text):
        command = text.split()

        if len(command) > 1:
            print(command[1:])
            return (command[0], command[1:])
        else:
            return (command[0], None)

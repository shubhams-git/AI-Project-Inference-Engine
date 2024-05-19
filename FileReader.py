class FileReader:
    """
    A utility class to read and parse the knowledge base (TELL) and query (ASK) statements from a text file.
    """

    @staticmethod
    def read(filename):
        """
        Reads a file and separates the TELL (knowledge base) and ASK (query) statements.

        Parameters:
        filename (str): The path to the input file containing TELL and ASK statements.

        Returns:
        tuple: A tuple containing two elements:
            - tell (list): A list of strings representing the knowledge base clauses.
            - ask (str): A string representing the query.
        """
        tell = []  # List to store the knowledge base clauses
        ask = ''  # String to store the query
        temp = []  # Temporary list for splitting lines
        ask_found = False  # Flag to indicate if ASK has been found

        with open(filename) as f:
            for line in f:
                # Remove newline characters and split statements by semicolon
                temp = line.strip().split(";")

                for x in temp:
                    x = x.lower()
                    if x != "" and x != "tell" and x != "ask":
                        # Check if ASK section has started
                        if ask_found:
                            ask = x.replace(" ", "")  # Remove spaces and assign to ask
                        else:
                            tell.append(x.replace(" ", ""))  # Remove spaces and add to tell

                    if x == "ask":
                        ask_found = True  # Set flag when ASK is found

        return tell, ask

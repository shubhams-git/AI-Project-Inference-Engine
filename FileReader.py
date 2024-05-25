class FileReader:
    """
    A utility class to read and parse the knowledge base (TELL) and query (ASK) statements from a text file.
    """

    @staticmethod
    def read(filename):
        """
        Reads a file and separates the TELL (knowledge base) and ASK (query) statements.

        Args:
            filename (str): The path to the input file containing TELL and ASK statements.

        Returns:
            tuple: A tuple containing two elements:
                - tell (list): A list of strings representing the knowledge base clauses.
                - ask (str): A string representing the query.
        """
        tell = []
        ask = ''
        temp = []
        ask_found = False

        with open(filename) as f:
            for line in f:
                temp = line.strip().split(";")

                for x in temp:
                    x = x.lower()
                    if x != "" and x != "tell" and x != "ask":
                        if ask_found:
                            ask = x.replace(" ", "")
                        else:
                            tell.append(x.replace(" ", ""))

                    if x == "ask":
                        ask_found = True

        return tell, ask

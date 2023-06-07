
        #search by last name
        query = "SELECT * FROM user where last_name = %s"
    if selected == "Middle Name":
        #search by middle name
        query = "SELECT * FROM user where middle_name = %s"
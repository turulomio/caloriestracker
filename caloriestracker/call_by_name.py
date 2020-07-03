## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README


## @param attribute str or list
## Class Person, has self.name, self.age(), self.age_years_ago(year) self.son (another Person object)
## manager_attributes of setDataFromManager must be called in a PersonManager
## - ["name", ["age",[]], ["age_years_ago", [year]], ["son.age",[]]
def call_by_name(o, string_or_tuple):
    ## Returns an object 
    def string_with_points(o, string_):
        for s in string_.split("."): # With .
            if "()" in s:#object.method1().attirbute
                o=getattr(o, s)()
            else:#object.attribute1
                o=getattr(o, s)
        return o
    # --------------------------------------
    if string_or_tuple.__class__.__name__=="str":
        return string_with_points(o, string_or_tuple)
    else:#List
        function=string_with_points(o, string_or_tuple[0])
        parameters=string_or_tuple[1]
        return function(*parameters)


if __name__ == '__main__':
    pass

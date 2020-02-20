## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

def remove_first_select(sql):
    """
        Esta función asume que el primer from están en mayúscula
        Devuelve una cadena en la que se ha quitado todo lo anterior al FROM
    """
    beforefirstfrom=sql.split("FROM")[0] 
    return sql.replace(beforefirstfrom," ")    

## Función que elimina la expresión AND si es la última de un SQL
##
## Cuando se generan sql con opciones de None en sus parametros, a veces sucede que se queda un AND suelto al final y falla es SQL. Con esta función se elimina solo si existe
##
## @param sql SQL string
## @return  string que se ha converftido a mayúsculas y se han quitado últimos espacios en blanco
def remove_last_and(sql):
    sql=sql.upper().rstrip()# Converts to upper and remove last white spaces
    if sql.endswith("AND"):
        sql=sql[:-3].rstrip()
    return sql

## Devuelve una cadena con el SQL formateado para ser mostrado en una línea
## @param sql SQL a formatear
## @return String Cadena formateada en una línea
def sql_in_one_line(sql):
    sql=sql.replace("\n", "")
    for i in range(20):
        sql=sql.replace("  ", " ")
    return sql

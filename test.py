def is_number(number): 
    try: 
        float(number)
        return True
    except: 
        return False

thing = '10, 0'
print(is_number(thing))
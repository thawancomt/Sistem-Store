def check_type(Type : type , ignoreSelf : bool = True, checkKwargs : bool = False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            #convert args to a list to handly it
            argsN = list(args)
            
            # Ignore self:
            if ignoreSelf:
                argsN.pop(0)

            for item in args:
                if not isinstance(item, Type):
                    raise TypeError(f'The argument {item, type(item)} does not correspond to the expected type: {Type.__name__} ')
                
            if checkKwargs:   
                for item, value in kwargs.items():
                    if not isinstance(value, Type):
                        raise TypeError(f'The value of named argument {item, type(item)} does not correspond to the expected type: {Type.__name__} ')
                
            return function(*args, **kwargs)
        return wrapper
    return decorator
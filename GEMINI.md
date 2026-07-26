Quero que use aqui dry, codigo limpo
Funções e variaveis limpas. 
e Early Returns também sempre que possivel;

def process_payment(user, amount):
    # Guard clauses at the top
    if user is None:
        return False
        
    if not user.is_active:
        return False
        
    if amount <= 0:
        return False

    # Happy path stands alone with zero nesting
    print("Processing payment...")
    return True

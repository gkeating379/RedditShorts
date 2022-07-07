import time
from fractions import Fraction
from fractions import gcd

def solution(m):

    def get_termination(m):
        '''Gets all states that terminate'''

        terminations = []
        for i in range(len(m)):
            state = m[i]
            total = 0
            for item in state:
                total += item            
            if total == 0:
                terminations.append(i)
        return terminations

    def make_stochastic(m, terms):
        '''Adds a 1 to the i slot in i termination'''
        for i in terms:
            m[i][i] = 1
        return m

    def put_in_standard_form(m, terms):
        '''Put m in standard form with terminating terms first
        returns m in standard form'''
        new_m = []
        #make column first
        for i in range(len(m)):
            temp = []
            for j in range(len(m)):
                temp.append(m[j][i])
            new_m.append(temp)
        temps = []
        for term in terms:
            temps.insert(0, new_m[term])

        for temp in temps:
            new_m.remove(temp)
            new_m.insert(0, temp)

        for i in range(len(new_m)):
            rotations = terms[0]
            for j in range(rotations):
                state = new_m[i]
                state.append(state.pop(0))            

        return new_m

    def get_S_and_R(m, end_of_terms):
        '''Returns the S and R box'''

        #S box
        S = []
        for i in range(end_of_terms + 1):
            state = m[i]
            temp = []
            for j in range(end_of_terms + 1, len(m)):
                temp.append(state[j])
            S.append(temp)

        R = []
        for i in range(end_of_terms + 1, len(m)):
            state = m[i]
            temp = []
            for j in range(end_of_terms + 1, len(m)):
                temp.append(state[j])
            R.append(temp)

        return S, R

    def sub_from_I(R):
        '''returns (I - R)'''
        I = make_identity_matrix(len(R) - 1)
        
        diff = []
        for i in range(len(R)):
            temp = []
            for j in range(len(R)):
                cur_diff = I[i][j] - R[i][j]
                temp.append(cur_diff)
            diff.append(temp)

        return diff

    def make_identity_matrix(size):
        I = []
        identity_index = 0
        for i in range(size + 1):
            temp = []
            for j in range(size + 1):
                if j == identity_index:
                    temp.append(1)
                else:
                    temp.append(0)
            I.append(temp)
            identity_index += 1
        return I

    def add_matrix(a, b):
        '''adds matrix a and b'''
        output = []
        for i in range(len(a)):
            temp = []
            for j in range(len(a)):
                temp.append(a[i][j] + b[i][j])
            output.append(temp)

        return output

    def scalar_multiplication(m ,c):
        '''Multiplies matrix m by scalar c'''
        output = []
        for i in range(len(m)):
            temp = []
            for j in range(len(m)):
                temp.append(m[i][j] * c)
            output.append(temp)
        
        return output
    
    def dot_product(a , b):
        '''returns a dot b'''
        output = 0
        for i in range(len(a)):
            output += (a[i] * b[i])

        return output
            

    def multiply_matrix(a, b):
        '''matrix a * matrix b'''
        output = []
        for i in range(len(a)):
            temp = []
            for j in range(len(b[0])):
                column_i = []
                for k in range(len(b)):
                    column_i.append(b[k][j])
                
                dot = dot_product(a[i], column_i)
                temp.append(dot)
            output.append(temp)

        return output

    def get_row_reduction_coeff(iden, red):
        '''Finds the solution to iden*x - red = 0'''
        return (-1 * red) / iden

    def get_inverse(diff):
        '''get the inverse of (I - R)'''
        I = make_identity_matrix(len(diff) - 1)

        #reduce down
        for i in range((len(I))):
            if diff[i][i] != 1:
                iden_inverse = diff[i][i] ** -1
                for k in range(len(diff)):
                    I[i][k] *= iden_inverse 
                    diff[i][k] *= iden_inverse
            for j in range(i + 1, len(I)):
                coeff = get_row_reduction_coeff(diff[i][i], diff[j][i])
                for k in range(len(diff)):
                    I[j][k] += I[i][k] * coeff 
                    diff[j][k] += diff[i][k] * coeff

        #reduce back and up
        for i in range((len(I)))[::-1]:
            if diff[i][i] != 1:
                iden_inverse = diff[i][i] ** -1
                for k in range(len(diff)):
                    I[i][k] *= iden_inverse 
                    diff[i][k] *= iden_inverse
            for j in range(i):
                coeff = get_row_reduction_coeff(diff[i][i], diff[j][i])
                for k in range(len(diff)):
                    I[j][k] += I[i][k] * coeff 
                    diff[j][k] += diff[i][k] * coeff

        return I
    
    def get_stable_matrix(m, P, end_of_terms):
        '''Stable matrix S(I - R)^-1'''
        output = []
        for i in range(len(m)):
            temp = []
            for j in range(len(m)):
                if i in range(end_of_terms + 1):
                    if j == i:
                        temp.insert(j, 1)
                    elif j <= end_of_terms: 
                        temp.insert(j, 0)
                    elif j + 1 :
                        temp.insert(j, P[i][j - (end_of_terms + 1)])
                    else:
                        temp.append(0)
                else:
                    temp.append(0)
            output.append(temp)
        return output

    def get_fractions(m, terms):
        '''Returns list of totals for each row'''
        output = []
        for i in range(len(m)):
            if i not in terms:
                temp = []
                denom = 0
                for item in m[i]:
                    denom += item
                for j in range(len(m)):
                    if denom == 0:
                        temp.append(0)
                    else:
                        temp.append(Fraction(m[i][j], denom))
            else:
                for j in range(len(m)):
                    if i == j:
                        temp.append(1)
                    else:
                        temp.append(0)
            output.append(temp)

        print(output)        
        return output

    def lcm(a, b):
        '''Lcm of a and b'''
        return a * b // gcd(a, b)

    def format_output(m, terms):
        num = []
        last_lcm = 1
        for i in range(len(m)):
            if m[i][0] != 0:
                last_lcm = lcm(last_lcm, m[i][0].denominator)
        for i in range(len(terms)):
            if m[i][0].denominator != last_lcm:
                num.append(m[i][0].numerator * (last_lcm // m[i][0].denominator))
            else:
                num.append(m[i][0].numerator)
       
        num.append(int(last_lcm))
        return num
    
    def quick_regular(m, terms):
        output = []
        for i in m:
            output.append([])

        original_indexs = []
        for term in terms:
            original_indexs.append(term)
        for i in range(len(m)):
            if i not in terms:
                original_indexs.append(i)

        for i in range(len(m)):
            for j in range(len(m)):
                if j < len(terms):
                    if i == j:
                        output[i].insert(j, Fraction(1,1))
                    else:
                        output[i].insert(j, Fraction(0,1))
                else:
                    denom = 0
                    pre_index = original_indexs[j]
                    for num in m[pre_index]:
                        denom += num
                    if denom == 0:
                        denom = 1  
                    frac = Fraction(m[pre_index][i], denom)
                    insert_index = (i + len(terms)) % len(m)
                    
                    output[insert_index].append(frac)
                
        return output

    def get_stable_distrubtion(m):
        '''P*X0'''
        terms = get_termination(m)
        # m = get_fractions(m, terms)
        # m = make_stochastic(m, terms)
        # m = put_in_standard_form(m, terms)
        m = quick_regular(m, terms)
        end_of_terms = len(terms) - 1
        S, R = get_S_and_R(m, end_of_terms)
        diff = sub_from_I(R)
        inverse = get_inverse(diff)
        P = multiply_matrix(S, inverse)
        stable_matrix = get_stable_matrix(m, P, end_of_terms)   

        #make input vector
        input = []
        for i in range(len(m)):
            if i == end_of_terms + 1:
                input.append([1])
            else:
                input.append([0])
        stable_distribution = multiply_matrix(stable_matrix, input)
        fractions_stable_distribution = format_output(stable_distribution, terms)
        
        return fractions_stable_distribution

    return get_stable_distrubtion(m)
            
start_time = time.time()
print(solution(([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])))
print(time.time() - start_time)

print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))
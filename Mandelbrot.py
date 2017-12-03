def testConv(c, maxiter):#test complex c for diverges
    n=0#count iterations
    z=c

    while(abs(z)<=2 and n< maxiter):
        z=z*z+c
        n+=1
        #print("iter:{},abs{}.".format(n,abs(z)))
    if(abs(z)>2):#catch diverging z on n=maxiter?
        return False
    return True

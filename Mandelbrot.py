
class Mandelbrot:
    def __init__(self):
        self.maxiter=100
        self.width=10
        self.z0=0

    def testConv(self, c):#test complex c for diverges
        n=0
        z=c
        while(abs(z)<=2 and n<self.maxiter):
            z=z*z+c
            n+=1
            #print("iter:{},abs{}.".format(n,abs(z)))
        if(abs(z)>2):
            return False
        return True

    def run(self,width):
        self.width=width
        halfwidth=width/2
        print("1/2 width={}".format(halfwidth))

        for i in range(width):
            for j in range(width):
                re=(i-halfwidth)/halfwidth
                im=(j-halfwidth)/halfwidth
                c = complex(re,im)
                if self.testConv(c):
                    print(c)

man = Mandelbrot()
man.run(100)
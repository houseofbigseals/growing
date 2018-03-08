# author: cratch_rider
# growing parameter optimization

import time
import numpy as np
from numpy import *
import pylab as pl
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import cm

def Functional(X1, X2, t):
    # X1 X2 - arrays with same sizes and shapes
    # t - one number
    # no noize now? mb in future
    ########################################
    # constants from experiment
    e1 = 10
    e2 = 1
    a_max = 0.00055
    a_min = 0.0014
    a = a_min
    b_max = 0.087
    b_min = 0.175
    b = b_min
    k = 0.15
    ########################################
    N = len(X1)

    #A = (np.ones(N))*0.0014
    A = (np.ones(N))*a
    A = A.reshape((np.shape(X1)))
    #print ((np.shape(A)))
    B1 = (np.ones(N))*b
    B1 = B1.reshape((np.shape(X1)))
    B2 = (np.ones(N))*b
    B2 = B2.reshape((np.shape(X1)))
    E1 = (np.ones(N))*e1
    E1 = E1.reshape((np.shape(X1)))
    E2 = (np.ones(N))*e2
    E2 = E2.reshape((np.shape(X1)))
    #dt = (np.ones(N))*0.013
    dt  = 1
    K = (np.ones(N))*k
    K = K.reshape((np.shape(X1)))
    T = (np.ones(N))*(t+dt)
    T = T.reshape((np.shape(X1)))
    #print(np.shape(np.sin(B1*T)), "TR")
    R1 = (X1 - (A*T+K*np.sin(B1*T)))
    #print(np.shape(R1))
    R2 = (X2 - (A*T+K*np.sin(B2*T)))
    F = E1*R1*R1 + E2*R2*R2
    return F

def fp(x1, x2, t):
    # constants from experiment
    e1 = 10
    e2 = 1
    a_max = 0.00055
    a_min = 0.0014
    a = a_min
    b_max = 0.087
    b_min = 0.175
    b = b_min
    k = 0.15
    dt = 1 #dt = 20 minuts and it is new measurement equivalent for all
    t_=t+dt
    #print('start fp debug')
    #print('x1 is {} x2 is {}'.format(np.shape(x1), np.shape(x2)))
    #print('t is {}'.format(np.shape(t)))
    f = e1*(x1-(a*t_+k*np.sin(b*t_)))*(x1-(a*t_+k*np.sin(b*t_)))+ \
    e2*(x2-(a*t_+k*np.sin(b*t_)))*(x2-(a*t_+k*np.sin(b*t_)))
    #f = e1*(x1-(a*t_+k*np.sin(b*t)))
    #print('f is {}'.format(np.shape(f)))
    #print('end fp debug')
    return f

def gradient_step(x1, x2, t, dx1, dx2, gamma):
    dt = 1 #dt = 20 minuts and it is one
    f0 = fp(x1, x2, t)
    #print('f0 is {}'.format(f0))
    f1 = fp(x1 + dx1, x2, t+dt)
    #print('f1 is {}'.format(f1))
    f2 = fp(x1, x2 + dx2, t+2*dt)
    #print('f2 is {}'.format(f2))
    x1_next = x1-gamma*((f1 - f0)/np.float(dx1))
    x2_next = x2-gamma*((f2 - f0)/np.float(dx2))
    #t = t+2*dt
    return x1_next, x2_next

def deep_gradient_step(x1, x2, x1_last, x2_last, t, dx1, dx2, gamma, alpha):
    dt = 1 #dt = 20 minuts and it is one
    f0 = fp(x1, x2, t)
    #print('f0 is {}'.format(f0))
    f1 = fp(x1 + dx1, x2, t+dt)
    #print('f1 is {}'.format(f1))
    f2 = fp(x1, x2 + dx2, t+2*dt)
    #print('f2 is {}'.format(f2))
    last_step_1 = x1 - x1_last
    new_step_1 = -gamma*((f1 - f0)/np.float(dx1))
    last_step_2 = x2 - x2_last
    new_step_2 = -gamma*((f2 - f0)/np.float(dx2))
    x1_next = x1 + (alpha*last_step_1 + (1-alpha)*new_step_1)
    x2_next = x2 + (alpha*last_step_2 + (1-alpha)*new_step_2)
    #t = t+2*dt
    return x1_next, x2_next

def conjugate_gradient_step(start, x1, x2, dx1, dx2, df1, df2, S1_last, S2_last, lam, t):
    # x1 x2 - point to step
    # dx1, dx2 - steps to find gradient
    # df1, df2 - last gradient components
    # S_last - last S component for conjugate step
    dt = 1 #dt = 20 minuts and it is one
    #print('start conjugate_gradient_step debug\n')
    #print('input x1 = {}, x2 = {}'.format(np.shape(x1), np.shape(x2)))
    #print('input dx1 = {}, dx2 = {}'.format(np.shape(dx1), np.shape(dx2)))
    #print('input df1 = {}, df2 = {}'.format(np.shape(df1), np.shape(df2)))
    #print('input S1_l = {}, S2_l = {}'.format(np.shape(S1_last), np.shape(S2_last)))
    #print('start is {}'.format(start))

    if(start==True):
        # it means that it is first iteration
        f0 = fp(x1, x2, t)
        #print(np.shape(f0))
        #print('f0 is {}'.format(f0))
        f1 = fp(x1 + dx1, x2, t+dt)
        #print('f1 is {}'.format(np.shape(f1)))
        #print('f1 is {}'.format(f1))
        f2 = fp(x1, x2 + dx2, t+2*dt)
        #print(np.shape(f2))
        #print('f2 is {}'.format(f2))

        df1_next = ((f1 - f0)/np.float(dx1))
        #print(np.shape(df1_next))
        df2_next = ((f2 - f0)/np.float(dx2))
        #print(np.shape(df2_next))
        #w = (df1_next*df1_next + df2_next*df2_next)/(df1*df1 + df2*df2)
        S1_next = -1*df1_next
        S2_next = -1*df2_next

        l = np.arange(0.000001, 1, 0.0005)
        x1vec = np.ones(np.shape(l)[0])*x1
        x2vec = np.ones(np.shape(l)[0])*x2
        S1vec = np.ones(np.shape(l)[0])*S1_next
        S2vec = np.ones(np.shape(l)[0])*S2_next
        func = Functional(x1vec+l*S1vec, x2vec+l*S2vec, t+2*dt)
        n_min = np.argmin(func)
        lam = l[n_min]
        print('lambda min is {}'.format(lam))
        x1_next = x1 + lam*S1_next
        x2_next = x2 + lam*S2_next
        #print('output x1 = {}, x2 = {}'.format(np.shape(x1_next), np.shape(x2_next)))
        #print('output df1 = {}, df2 = {}'.format(np.shape(df1_next), np.shape(df2_next)))
        #print('output S1_l = {}, S2_l = {}'.format(np.shape(S1_next), np.shape(S2_next)))
        #print('end conjugate_gradient_step debug\n')
        return x1_next, x2_next, df1_next, df2_next, S1_next, S2_next
    else:
        f0 = fp(x1, x2, t)
        #print('f0 is {}'.format(f0))
        f1 = fp(x1 + dx1, x2, t+dt)
        #print('f1 is {}'.format(f1))
        f2 = fp(x1, x2 + dx2, t+2*dt)
        #print('f2 is {}'.format(f2))

        df1_next = ((f1 - f0)/np.float(dx1))
        df2_next = ((f2 - f0)/np.float(dx2))
        w = (df1_next*df1_next + df2_next*df2_next)/np.float((df1*df1 + df2*df2))
        S1_next = -1*df1_next + w*S1_last
        S2_next = -1*df2_next + w*S2_last

        l = np.arange(0.000001, 1, 0.0005)
        x1vec = np.ones(np.shape(l)[0])*x1
        x2vec = np.ones(np.shape(l)[0])*x2
        S1vec = np.ones(np.shape(l)[0])*S1_next
        S2vec = np.ones(np.shape(l)[0])*S2_next
        func = Functional(x1vec+l*S1vec, x2vec+l*S2vec, t+2*dt)
        n_min = np.argmin(func)
        lam = l[n_min]
        print('lambda min is {}'.format(lam))
        x1_next = x1 + lam*S1_next
        x2_next = x2 + lam*S2_next
        #print('output x1 = {}, x2 = {}'.format(np.shape(x1_next), np.shape(x2_next)))
        #print('output df1 = {}, df2 = {}'.format(np.shape(df1_next), np.shape(df2_next)))
        #print('output S1_l = {}, S2_l = {}'.format(np.shape(S1_next), np.shape(S2_next)))
        #print('end conjugate_gradient_step debug\n')
        return x1_next, x2_next, df1_next, df2_next, S1_next, S2_next

def newton(x1, x2, dx1, dx2, gamma,t):
    dt = 1 #dt = 20 minuts and it is one
    f0 = fp(x1, x2, t)
    f1 = fp(x1 + dx1, x2, t+dt)
    f11 = fp(x1-dx1, x2, t+dt)
    f2 = fp(x1, x2 + dx2, t+dt)
    f22 = fp(x1, x2 - dx2, t+dt)
    # first order derivative
    df1 = (f1 - f0)/np.float(dx1)
    df2 = (f2 - f0)/np.float(dx2)
    # second order derivative
    ddf1 = (f1 - 2*f0 + f11)/(np.float(dx1*dx1))
    ddf2 = (f2 - 2*f0 + f22)/(np.float(dx2*dx2))

    x1_next = x1-(gamma/np.float(ddf1*ddf2))*(ddf2*df1+0*df2)#must be corrected
    x2_next = x2-(gamma/np.float(ddf1*ddf2))*(ddf1*df2+0*df1)#must be corrected

    return x1_next, x2_next

def show_3D(X, Y, Z):
    "shows all"

    fig=pl.figure()

    ax = p3.Axes3D(fig)
    cs = ax.contour(X, Y, Z, 50)
    pl.clabel(cs)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Add a color bar which maps values to colors.
    fig.colorbar(cs, shrink=0.5, aspect=5)

    pl.show()
    #surf = ax.contourf3D(X,Y,Z, np.linspace(-1, 1, 40), cmap=cm.coolwarm)
    #surf = ax.contour3D(X,Y,Z, cmap=cm.coolwarm)# cmap=cm.coolwarm)
    #surf = ax.plot_surface(X,Y,Z, rstride = 3, cstride = 3, color = 'g', cmap=cm.coolwarm)
    #surf = ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap=cm.coolwarm,linewidth=0, antialiased=False)


    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=5)

    #pl.show()
def show_2D(X, Y, Z):
    fig=pl.figure()
    cs = pl.contour(X, Y, Z, 30)
    pl.clabel(cs, fmt = '%.1f', colors="black")
    # Add a color bar which maps values to colors.
    fig.colorbar(cs, shrink=0.5, aspect=5)
    pl.plot(n)
    pl.show()
    return 0

def main():
    # Make data.
    # X is E W/m^2
    # Y is T Celsius
    E = np.arange(-100, 200, 0.25)
    T = np.arange(-30, 40, 0.05)
    # gradient parameters
    dx1 = 0.1
    dx2 = 0.1
    gamma = 0.5
    alpha = 0.5
    lam = 0.001
    x_start = 3
    y_start = 3
    # mesh data
    X, Y = np.meshgrid(E, T)
    d1x, d2x = np.shape(X)
    d1y, d2y = np.shape(Y)
    X_ = X.reshape((d1x*d2x, 1))
    Y_ = Y.reshape((d1y*d2y, 1))
    t = 1
    Z_ = Functional(X_, Y_, t)
    z_min = np.array((0, ))
    y_min = np.array((0, ))
    x_min = np.array((0, ))
    x_grad = np.array([x_start])
    y_grad = np.array([y_start])
    # for conjugate gradient method
    S1 = 0
    S2 = 0
    df1 = 0
    df2 = 0
    # lol
    dz = np.array((0, ))
    t_max = 100
    Time = 1
    tt = 1*5
    t = np.arange(0, t_max+1, 1)*tt

    # find minimum and gradient steps
    for i in range(0, t_max):
        if (i == 0):
            ZZ_ = Functional(X_, Y_, Time)
            # find min of ZZ_
            n_min = np.argmin(ZZ_)
            z_min = np.append(z_min, np.min(ZZ_))
            x_min = np.append(x_min, X_[n_min])
            y_min = np.append(y_min, Y_[n_min])
            #xg, yg = gradient_step(x_grad[i], y_grad[i], Time, dx1, dx2, gamma)
            #xg, yg = deep_gradient_step(x_grad[i], y_grad[i], Time, dx1, dx2, gamma)
            #xg, yg, df1_n, df2_n, S1_n, S2_n = conjugate_gradient_step(1, x_start, y_start, dx1, dx2, df1, df2, S1, S2, lam, t[i])
            #print('xg = {}, yg = {}'.format(np.shape(xg), np.shape(yg)))
            #print('df1_n = {}, df2_n = {}'.format(np.shape(df1_n), np.shape(df2_n)))
            #print('S1_n = {}, S2_n = {}'.format(np.shape(S1_n), np.shape(S2_n)))
            xg, yg = newton(x_start, y_start, dx1, dx2, gamma,t[i])
            x_grad = np.append(x_grad, xg)
            y_grad = np.append(y_grad, yg)
            # remember new parameters
            #S1 = S1_n
            #S2 = S2_n
            #df1 = df1_n
            #df2 = df2_n
            dz = np.append(dz, np.min(ZZ_) - fp(xg, yg, Time+2))
            print(x_grad[i], y_grad[i], Time)
            print(x_min[i],  y_min[i])
            Time = Time + tt
        else:
            ZZ_ = Functional(X_, Y_, Time)
            # find min of ZZ_
            n_min = np.argmin(ZZ_)
            z_min = np.append(z_min, np.min(ZZ_))
            x_min = np.append(x_min, X_[n_min])
            y_min = np.append(y_min, Y_[n_min])
            #xg, yg = gradient_step(x_grad[i], y_grad[i], Time, dx1, dx2, gamma)
            #xg, yg = deep_gradient_step(x_grad[i], y_grad[i], x_grad[i-1],y_grad[i-1],\
              #Time, dx1, dx2, gamma, alpha)
            #xg, yg, df1_n, df2_n, S1_n, S2_n = conjugate_gradient_step(0, x_grad[i-1], y_grad[i-1], dx1, dx2, df1, df2, S1, S2, lam, t[i])
            xg, yg = newton(x_grad[i], y_grad[i], dx1, dx2, gamma,t[i])
            # remember new parameters
            #print('xg = {}, yg = {}'.format(xg, yg))
            #print('df1_n = {}, df2_n = {}'.format(df1_n, df2_n))
            #print('S1_n = {}, S2_n = {}'.format(S1_n, S2_n))
            #print('xg = {}, yg = {}'.format(np.shape(xg), np.shape(yg)))
            #print('df1_n = {}, df2_n = {}'.format(np.shape(df1_n), np.shape(df2_n)))
            #print('S1_n = {}, S2_n = {}'.format(np.shape(S1_n), np.shape(S2_n)))
            #S1 = S1_n
            #S2 = S2_n
            #df1 = df1_n
            #df2 = df2_n
            x_grad = np.append(x_grad, xg)
            y_grad = np.append(y_grad, yg)
            dz = np.append(dz, np.min(ZZ_) - fp(xg, yg, Time+4))
            if(i%25==0):
                # plot all steps
                Z = ZZ_.reshape((len(T), len(E)))
                fig=pl.figure()
                #pl.plot(X, Y, 'c')
                cs = pl.contour(X, Y, Z, 20)
                pl.clabel(cs, fmt = '%.1f', colors="black")
                # Add a color bar which maps values to colors.
                fig.colorbar(cs, shrink=0.5, aspect=5)

                pl.plot(x_min, y_min, "-b")
                pl.plot(x_grad, y_grad, "-vr")
                pl.plot(X_[n_min], Y_[n_min], "sk")

                pl.grid()
                pl.show()
            print(x_grad[i], y_grad[i], Time)
            print(x_min[i],  y_min[i])
            Time = Time + tt
    print(np.shape(Z_), "Z_")
    print('len of x_min is {}'.format(np.shape(x_min)))
    Z = ZZ_.reshape((len(T), len(E)))

    #print(np.shape(Z), "Z")
    #print(np.shape(X), "X")
    #print(np.shape(Y), "Y")

    #show_2D(X, Y, Z)
    fig=pl.figure()
    cs = pl.contour(X, Y, Z, 20)
    pl.clabel(cs, fmt = '%.1f', colors="black")
    # Add a color bar which maps values to colors.
    fig.colorbar(cs, shrink=0.5, aspect=5)
    pl.plot(x_min, y_min, "-ob")
    pl.plot(x_grad, y_grad, "-vr")
    pl.savefig("growing.png")
    #subplots
    fig=pl.figure()
    pl.subplot(2,2,1)
    pl.plot(t, y_min, "-oc")
    pl.title ("y_min(t)")
    pl.subplot(2,2,2)
    pl.plot(t, x_min, "-ob")
    pl.title ("x_min(t)")
    pl.subplot(2,2,3)
    pl.plot(t, z_min, "-or")
    pl.title ("z_min(t)")
    pl.subplot(2,2,4)
    pl.plot(t, dz, "-ok")
    pl.title ("dz(t)")
    pl.show()

main()
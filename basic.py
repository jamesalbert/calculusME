#!/usr/bin/env python

import math
import re

'''Calculus Made Easy'''

cmds = ['limit', 'derivative']

class calculusME:
    def __init__(self):
        self.cleanup()
        print(
"""Rules of CalculusME:
    -- use parentheses ie (2x+2)/(1x+1)
    -- use 'x' for variable
    -- if just 'x', put '1x'
    -- type 'help' for options
    -- type 'quit' to exit
    -- absolutely, positively NO SPACES!""")
        
        self.lim = None
        while True:
            cmd = raw_input('>')
            for k in re.findall('\-\-(\w+)', cmd):
                cmd = cmd.replace(" --"+k,'')
                self.opts[k] = True
            if cmd == 'help':
                print self.options()
            elif cmd == 'quit' or cmd == 'exit':
                break
            elif cmd in cmds:
                print getattr(self, cmd)()
            else:
                print 'no command %s' % cmd
    
    def options(self):
        return(
"""Options:
    -- limit
    -- derivative""")
    
    def format_equation(self):
        '''format f(x) for exponents'''
        self.lim = self.lim.replace('^', '**')
        
    def substitute_x(self, eq, x):
        opx = '(\+|\-|\/|\*)x'
        while opx:
            try:
                '''find operator in front of x'''
                op = re.search(
                    opx, eq).group(1)
                '''increment x with operator'''
                eq = eq.replace(op+'x', x)
            except:
                opx = False
            
        opx = '(\+|\-|\/|\*)x'
        '''replace x multiples and increment it'''
        eq = eq.replace('x', '*'+x)
        return eq
    
    def derivative(self):
        try:
            dydx = []
            eq = ""
            self.lim = f_of_x = raw_input("f(x)=")
            self.x = fprime = raw_input("f'@")
            #if self.sanitize() is False:
            #    return 'only integers and x'
            f_of_a = self.substitute_x(f_of_x, "("+str(fprime)+")")
            f_of_a_plus_x = self.substitute_x(
                f_of_x,"("+str(fprime)+'+(1x))')
            self.lim = "(("+f_of_a_plus_x+")-("+f_of_a+"))/(1x)"
            self.x = 0
            return self.limit().replace('limit','derivative')
        except:
            return 'error, please review your submission'
        finally:
            self.cleanup()

    def limit(self):
        '''if f(x) is not defined, ask for it'''
        if self.lim is None:
            self.lim = raw_input('lim ')
            self.x = raw_input('x->')
        if self.lim is 'x':
            return 'limit is '+self.x
        if self.sanitize() is False:
            return 'only integers and x'
        self.format_equation()
        try:
            approaching = []
            side = 1
            x = self.x
            i = 0
            while i <= 7:
                if i is 6:
                    '''if we're approaching from the left,
                       then we're done'''
                    if side is -1:
                        break
                    '''if we're approaching from the right,
                       switch to the left'''
                    i = 1
                    side = -1
                    continue
                i += 1
                '''get .0001 more away from approaching int'''
                inc = .0001*i*side
                eq = self.substitute_x(
                    self.lim, str(int(x)+inc))
                approaching.append(eval(eq))
                if self.opts['show_work'] is True:
                    print str(eq)+" = "+str(eval(eq))
                
            for l in approaching:
                '''if the difference from one limit
                   to the next is greater than one,
                   the limit does not exist'''
                if abs(l-approaching[-1]) > .01:
                    return 'limit does not exist'
            '''we found the limit'''
            if abs(round(approaching[1])-approaching[1]) < .01:
                return 'limit is '+str(round(approaching[1]))
            return 'limit is '+str(round(approaching[0], 2))
         
        except ZeroDivisionError:
            return 'no dividing by zero'
        except:
            return 'unforeseen error. please try again'
        finally:
            self.cleanup()
            
    def sanitize(self):
        '''confirm input is only an integer or x'''
        if self.lim is None or self.x is None:
            return False
        lim = re.findall('(\w)', self.lim)
        for l in lim:
            try:
                if l is not 'x':
                    int(l)
                elif l is 'x':
                    pass
            except ValueError:
                self.cleanup()
                return False
        
        for i in str(self.x):
            try:
                int(str(i))
            except ValueError:
                self.cleanup()
                return False
               
        return True
            
    def cleanup(self):
        self.lim = None
        self.x = None
        self.opts = {'show_work': False}
        

m = calculusME()

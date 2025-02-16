
#-----------------------------------------------
#fft_utils.py - Python Guitar Tuner general sound editing utilities
#Copyright (c) 2007, Imri Goldberg
#All rights reserved.
#
#Redistribution and use in source and binary forms,
#with or without modification, are permitted provided
#that the following conditions are met:
#
#    * Redistributions of source code must retain the
#       above copyright notice, this list of conditions
#       and the following disclaimer.
#    * Redistributions in binary form must reproduce the
#       above copyright notice, this list of conditions
#       and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#    * Neither the name of the Algorithm.co.il nor the names of
#       its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------------


import operator
import base_tools
import numpy


def window(N,n):
    return 0.5*(1-numpy.cos(2*numpy.pi*n/N))

def awindow(N):
    return window(N-1, numpy.arange(N))

def remove_harmonics(f):
    t = array(f)
    for i in range(len(f)-1,0,-1):
        t[i] = t[i] - (t[i/2]+t[1+(i/2)]+t[(i/2)-1])/3
        if t[i]<0:
            t[i] = 0
    return t

def remove_harmonics2(f):
    t = array(f)
    for i in range(len(f)-1,0,-1):
        t[i] = t[i] - (t[i/3]+t[1+(i/3)]+t[(i/3)-1])/3
        if t[i]<0:
            t[i] = 0
    return t


def compose_peak(idx,seq_len,big_list):
    peak_base = big_list[idx-seq_len-1:idx]
    indexes = numpy.array([x[0] for x in peak_base])
    values =  numpy.array([x[1] for x in peak_base])
    peak_location = sum(indexes*(values/sum(values)))
    weights = abs(indexes-peak_location)
    peak_value = sum(values*(weights/sum(weights)))
    return peak_location,peak_value

def find_peaks(a,num_deviations=3):
    E = sum(a)/len(a)
    V = sum(a*a)/len(a) - E*E
    s = numpy.sqrt(V)
    l = enumerate(a)
    big = [x for x in l if x[1] > E+num_deviations*s]
    cur_len = 0
    joint = []
    big+=[(0,0)]
    for i in range(1,len(big)):
        if big[i][0]==big[i-1][0]+1:
            cur_len+=1
        else:
            if cur_len>0:
                joint.append(compose_peak(i,cur_len,big))
            else:
                joint.append(big[i-1])
            cur_len = 0
    return joint



            
    


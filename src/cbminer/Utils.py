'''
The MIT License (MIT)

Copyright (c) 2015 @ CodeForBirmingham (http://codeforbirmingham.org)
@Author: Marcus Dillavou <marcus.dillavou@codeforbirmingham.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''
A Static Helper class with misc methods
that might be useful
'''

class Utils(object):
    @staticmethod
    def Base26ToBase10(col):
        '''
        Convert an excel column name, like AB to a number, like 28 - 1 = 27
        Since we like 0 based.
        A=0
        Z=25
        AA=26
        AZ=51
        '''
        c = 0
        place = 0
        for i in reversed(col):
            base = 26 ** place

            # We plus 1 here, because if A = 0
            #  and Z = 25, then AAA would be 0
            #  which isn't what we want. Therefore
            #  A=1 and Z=26, and we do our conversion
            #  which means we can't ever have 0, so
            #  we just subtract 1 from the final result
            r = ord(i.upper()) - ord('A') + 1

            t = base * r
            
            c += t
            
            place += 1

        return c - 1

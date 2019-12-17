import unittest
from TestUtils import TestCodeGen
from AST import *

class CheckCodeGenSuite(unittest.TestCase):
    def test_add_op(self):
        input = """
        float qswe;
        void main(){
            putIntLn(-3);
            putIntLn(return5(-4));
            abc();
            putIntLn(a);
            qswe = a;
            putFloatLn(qswe);
            putBoolLn(i);
            putFloatLn(return5float());
        }
        int a;

        int return5(int a){
            return 10-5;
        }

        float return5float()
        {
            return (10000-5)*0+5;
        }

        int abs(int n)
        {
            //if (a<0)  return -a;
            //else return a;
            return 0;
        }

        void abc(){
            i = false;
            a=4;
        }
        boolean i;
        """
        expect = "-3\n5\n4\n4.0\nfalse\n5.0\n"
        self.assertTrue(TestCodeGen.test(input,expect,500))

    def test_string(self):
        input = """
        void main()
        {
            putStringLn(returnstring("assd"));
        }

        string returnstring(string a){
            string b;
            b="ewrtgasd";
            return b;
        }
        int q;
        """
        expect = "ewrtgasd\n"
        self.assertTrue(TestCodeGen.test(input,expect,501))

    def test_giaithua(self):
        input = """
        void main(){
            putInt(gt(10));
        }

        int gt(int n){
            int i,p;
            p = 1;
            for (i = 1;i<=n;i=i+1){
                p = p * i;
            }
            return p;
        }

        int q;
        """
        expect = "3628800"
        self.assertTrue(TestCodeGen.test(input,expect,502))

    def test_giaithua_de_quy(self):
        input = """
        void main(){
            putInt(gt(5));
        }

        int gt(int n)
        {
            if (n==0) return 1;
            else return n*gt(n-1);
        }

        int q;
        """
        expect = "120"
        self.assertTrue(TestCodeGen.test(input,expect,503))

    def test_if(self):
        input = """
        void main(){
            int n;
            n=0;
            if (0==n) n=n+1;
            else n=n+2;
            n=n+4;
            putInt(n);
        }
        """
        expect = "5"
        self.assertTrue(TestCodeGen.test(input,expect,504))

    def test_bin_op_all(self):
        input = """
            void main(){
                putIntLn(9 + 6);
                putIntLn(9 - 6);
                putIntLn(9 * 6);
                putIntLn(9 / 6);
                putIntLn(9 % 6);
                putBoolLn(9 == 6);
                putBoolLn(9 <= 6);
                putBoolLn(9 < 6);
                putBoolLn(9 > 6);
                putBoolLn(9 >= 6);
                putBoolLn(9 != 6);
                putFloatLn(9 / 6);
                putFloatLn(3.14159 + 2.51);
                putFloatLn(3.14159 - 2.51);
                putFloatLn(3.14159 * 2.51);
                putFloatLn(3.14159 / 2.51);
                putBoolLn(3.14159 <= 2.51);
                putBoolLn(3.14159 < 2.51);
                putBoolLn(3.14159 > 2.51);
                putBoolLn(3.14159 >= 2.51);
                putFloatLn(3.14159 / 2.51);
                putBoolLn(true && (1.3>4));
                putBoolLn(true || (1.3>4));
                putBoolLn(true && (1.3>4));
                putBoolLn(true || (1.3>4));
                putFloatLn(3.14159 + 2);
                putFloat(3 + 2.51);
            }
        """
        expect = "15\n3\n54\n1\n3\nfalse\nfalse\nfalse\ntrue\ntrue\ntrue\n1.5\n5.6515903\n0.6315901\n7.885391\n1.2516296\nfalse\nfalse\nfalse\ntrue\ntrue\ntrue\n1.2516296\nfalse\ntrue\nfalse\ntrue\n5.14159\n5.51"
        self.assertTrue(TestCodeGen.test(input,expect,505))

    def test_unaryop_all(self):
        input = """
            void main(){
                putIntLn(-3);
                putIntLn(--3);
                putFloatLn(-3.3);
                putBoolLn(! true);
                putBool(! (1 == 2));
            }
        """
        expect = "-3\n3\n-3.3\nfalse\ntrue"
        self.assertTrue(TestCodeGen.test(input,expect,506))

    def test_assoc_bin_and_unaryop(self):
        input = """
            void main(){
                putFloatLn(-3 + 3.4);
                putFloatLn(--2.2 + -2);
            }
        """
        expect = "0.4000001\n0.20000005\n"
        self.assertTrue(TestCodeGen.test(input,expect,507))

    def test_simple_if(self):
        input = """
            int a;
            void main(){
                if (true) putInt(3);
                else putInt(2);
            }
            """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,508))

    def test_nested_if(self):
        input = """
            int a;
            void main(){
                if (true){
                    if (false) putInt(5);
                    else putFloat(5.2);
                }
                else putInt(2);
            }
            """
        expect = "5.2"
        self.assertTrue(TestCodeGen.test(input,expect,509))

    def test_ambigous_if(self):
        input = """
            int a;
            void main(){
                if (true)
                    if (false) putInt(2);
                    else putInt(3);
            }
            """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,510))

    def test_complex_if(self):
        input = """
            int a,b;
            void main(){
                a=0;
                if (true) a=a+1;
                else a=a+2;
                a=a+4;
                b=a;
                putInt(b);
            }
            """
        expect = "5"
        self.assertTrue(TestCodeGen.test(input,expect,511))

    def test_if_not_else(self):
        input = """
            void main(){
                putInt(a()+b());
            }
            int a()
            {
                if (true) return 3;
                return 7;
            }
            int b()
            {
                if (false) return 3;
                return 7;
            }
            """
        expect = "10"
        self.assertTrue(TestCodeGen.test(input,expect,512))

    def test_break(self):
        input = """
            void main(){
                int s,i;
                s=0;
                for (i=1;i<10;i=i+1){
                    s=s+i;
                    if (i==6) break;
                }
                putInt(s);
            }
            """
        expect = "21"
        self.assertTrue(TestCodeGen.test(input,expect,513))

    def test_continue(self):
        input = """
            void main(){
                int s,i;
                s=0;
                for (i=1;i<10;i=i+1){
                    if (i==6) continue;
                    s=s+i;
                }
                putInt(s);
            }
            """
        expect = "49"
        self.assertTrue(TestCodeGen.test(input,expect,514))

    def test_complex_continue(self):
        input = """
            void main(){
                int s,s1,i ,j;
                s=0;
                for (i=1;i<10;i=i+1){
                    s1=i;
                    for (j=1;j<100;j=j+1){
                        if ((50<j) && (j<75)) continue;
                        s1 = s1 + j;
                    }
                    for (j=1000;j>1;j=j-1){
                        if (j<1000) continue;
                        s1 =s1-j;
                        continue;
                    }
                    if (i==6) continue;
                    s=s+s1;
                    continue;
                }
                putInt(s);
            }
            """
        expect = "22999"
        self.assertTrue(TestCodeGen.test(input,expect,515))

    def test_simple(self):
        input = """
            int q,w;
            void main(){
                int a;
                for (a=1;a<3;a=a+1){
                putInt(1);
                if (a>1) break;
                }
            }
        """
        expect = "11"
        self.assertTrue(TestCodeGen.test(input,expect,516))

    def test_while(self):
        input = """
        void main(){
            int i,s;
            i=s=0;
            do
            {
                s = s+i;
                i=i+1;
            }while (i<=10);
            s=s*2;
            putInt(s);
            return;
        }
        """
        expect = "110"
        self.assertTrue(TestCodeGen.test(input,expect,517))

    def test_with(self):
        input = """
            void main(){
                int a,b;
                a=5;
                b=999;
                putInt(a);
                {
                    float a;
                    a=6;
                    putFloat(a);
                    putInt(b);
                    }
                putInt(a);
            }
            int a;
        """
        expect = "56.09995"
        self.assertTrue(TestCodeGen.test(input,expect,518))

    def test_andthen(self):
        input = """
            void main(){
                if (testShortCircuitHandled()) putString("Short circuit handled.");
                else putString("Short circuit did not handled.");
            }
            boolean testShortCircuitHandled(){
                int a_temp;boolean b;
                a_temp = a = 5;
                return (false && (PlusPlusA() < 0)) || (a == a_temp);
            }
            int PlusPlusA()
            {
                a=a+1;
                return a;
            }
            int APlusPlus(){
                int q;
                q=a;
                a=a+1;
                return q;
            }
            int a;
        """
        expect = "Short circuit handled."
        self.assertTrue(TestCodeGen.test(input,expect,519))

    def test_orelse(self):
        input = """
            void main(){
                if (testShortCircuitHandled()) putString("Short circuit handled.");
                else putString("Short circuit did not handled.");
            }
            boolean testShortCircuitHandled(){
                int a_temp;boolean b;
                a_temp = a = 5;
                return (true || (PlusPlusA() < 0)) && (a == a_temp);
            }
            int PlusPlusA()
            {
                a=a+1;
                return a;
            }
            int APlusPlus(){
                int q;
                q=a;
                a=a+1;
                return q;
            }
            int a;
        """
        expect = "Short circuit handled."
        self.assertTrue(TestCodeGen.test(input,expect,520))

    def test_coercions_param(self):
        input = """
            void main(){
                putFloatLn(4);
                putFloat(intTofloat(5));
            }
            float intTofloat(int n)
            {
                return n;
            }
        """
        expect = "4.0\n5.0"
        self.assertTrue(TestCodeGen.test(input,expect,521))

    def test_passingparam(self):
        input = """
            void main(){
                caller(1,2,3.0,true, false == true,"day la string");
            }
            void caller(int a, float b,float c, boolean d, boolean e ,string f){
                putInt(a);
                putFloat(b);
                putFloat(c);
                putBool(d);
                putBool(e);
                putString(f);
            }
        """
        expect = "12.03.0truefalseday la string"
        self.assertTrue(TestCodeGen.test(input,expect,522))

    def test_passingparam_function(self):
        input = """
            void main(){
                putString(caller(1,2,3.0,true, false == true,"day la string"));
            }
            string caller(int a, float b,float c, boolean d, boolean e ,string f)
            {
                putInt(a);
                putFloat(b);
                putFloat(c);
                putBool(d);
                putBool(e);
                putString(f);
                return f;
            }
        """
        expect = "12.03.0truefalseday la stringday la string"
        self.assertTrue(TestCodeGen.test(input,expect,523))

    def test_for_downto(self):
        input = """
            void main(){
                int i;
                for (i=10;i>=1;i=i-1){
                    putIntLn(i);
                }
            }
        """
        expect = "10\n9\n8\n7\n6\n5\n4\n3\n2\n1\n"
        self.assertTrue(TestCodeGen.test(input,expect,524))

    def test_add_op_large(self):
        """int Simple program main() {} """
        input = """void main(){ putInt(32767+32767); }"""
        expect = "65534"
        self.assertTrue(TestCodeGen.test(input,expect,525))

    def test_mul_op(self):
        input =  """void main(){ putInt(4*6); }"""
        expect = "24"
        self.assertTrue(TestCodeGen.test(input,expect,526))

    def test_sub_op(self):
        input =  """void main(){ putInt(6-32767); }"""
        expect = "-32761"
        self.assertTrue(TestCodeGen.test(input,expect,527))

    def test_add_op_float(self):
        """int Simple program main() {} """
        input = """void main(){ putFloat(100.5+40); }"""
        expect = "140.5"
        self.assertTrue(TestCodeGen.test(input,expect,528))

    def test_add_op_large_float(self):
        """int Simple program main() {} """
        input = """void main(){ putFloat(32766.9+32766.5); }"""
        expect = "65533.4"
        self.assertTrue(TestCodeGen.test(input,expect,529))

    def test_mul_op_float(self):
        input =  """void main(){ putFloat(4e3*6.5); }"""
        expect = "26000.0"
        self.assertTrue(TestCodeGen.test(input,expect,530))

    def test_sub_op_float(self):
        input =  """void main(){ putFloat(6-327.67); }"""
        expect = "-321.67"
        self.assertTrue(TestCodeGen.test(input,expect,531))

    def test_div_op_1_float(self):
        input =  """void main(){ putFloat(6/327.67); }"""
        expect = "0.018311106"
        self.assertTrue(TestCodeGen.test(input,expect,532))

    def test_div_op_2_float(self):
        input =  """void main(){ putFloat(6.5/327.67); }"""
        expect = "0.019837031"
        self.assertTrue(TestCodeGen.test(input,expect,533))

    def test_div_op_2_int(self):
        input =  """void main(){ putFloat(9/5); }"""
        expect = "1.0"
        self.assertTrue(TestCodeGen.test(input,expect,534))
        
    def test_ppa(self):
        input = """
            int a,b,c,d;
            void main(){
                b=c=d=PlusPlusA();
                putInt(a);
                putInt(b);
                putInt(c);
                putInt(d);
                putInt(PlusPlusA());
                putInt(PlusPlusA());
                putInt(PlusPlusA());
                putInt(PlusPlusA());
            }
            int PlusPlusA()
            {
                a=a+1;
                return a;
            }
        """
        expect = "11112345"
        self.assertTrue(TestCodeGen.test(input,expect,535))

    def test_float_compare(self):
        input = """
             void main(){
                 putBool(1.23 < 2.19);
                 putBool(1.23 < 0.2);
                 putBool(1.23 > 2.11);
                 putBool(1.23 > (-0.1));
                 putBool(1.23 >= 2.1);
                 putBool(1.23 >= 1);
                 putBool(1.23 >= 1.23);
                 putBool(1.23 <= 2.1);
                 putBool(1.23 <= 0.12);
                 putBool(1.23 <= 1.23);
             }
        """
        expect = "truefalsefalsetruefalsetruetruetruefalsetrue"
        self.assertTrue(TestCodeGen.test(input,expect,536))

    def test_while_stmt__1(self):
        input = """
             void main(){
                int i,s;
                i = 1;
                s = 0;
                do
                {
                    s = s + i;
                    break;
                    i = i + 1;
                }while (i <= 10);
                putInt(s);
             }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,537))

    def test_for_stmt__1(self):
        input = """
             void main(){
                int i,s;
                s = 0;
                for (i = 10;i>1;i=i-1){
                    s = s + i;
                    break;
                }
                putInt(s);
             }
        """
        expect = "10"
        self.assertTrue(TestCodeGen.test(input,expect,538))

    def test_compicate_if(self):
        input = """
        boolean foo()
        {
            putStringLn("hello");
            return true;
        }

        void main(){
            int x ;
            x = 123;
            if (x > 100)
                putStringLn("100 < x < 200");
            else {
                if (x > 200)
                    putStringLn("200 < x < 300");
                else {
                    if (x > 300)
                        putStringLn("x > 300");
                    else {
                        if (x > 100) x = x + 100;
                    }
                }
            }
            putIntLn(x);
        }"""
        expect = """100 < x < 200
123
"""
        self.assertTrue(TestCodeGen.test(input, expect, 539))

    def test_hello(self):
        input = """
        boolean foo()
        {
            putStringLn("hello");
            return true;
        }

        void main(){
            int x ;
            x = 123;
            if (true && false)
                x = x - 100;
            putIntLn(x);
        }
        """
        expect = """123\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 540))

    def test_while_lmao(self):
        input = """
        boolean foo()
        {
            putStringLn("hello");
            return true;
        }

        void main(){
            int x ;
            x = 1;
            do
            {
                putIntLn(x);
                if (x == 10) putStringLn("lmao");
                x = x + 1;
            }while (x <= 10);
        }
        """
        expect = """1
2
3
4
5
6
7
8
9
10
lmao
"""
        self.assertTrue(TestCodeGen.test(input, expect, 541))

    def test_is_prime(self):
        input = """
        boolean isPrime(int x)
        {
            int i ;
            for (i = 2;i< x / 2;i=i+1){
                if (x % i == 0) return false;
            }
            return true;
        }
        
        void main()
        {
            int x, i;
            i = 0;
            x = 100;
            do
            {
                if (isPrime(i)) putIntLn(i);
                i = i + 1;
            }while (i <= x);
        
        }
        """
        expect = """0
1
2
3
5
7
11
13
17
19
23
29
31
37
41
43
47
53
59
61
67
71
73
79
83
89
97
"""
        self.assertTrue(TestCodeGen.test(input, expect, 542))

    def test_fact(self):
        input = """
        int fact(int x)
        {
            int i, f ;
            f = 1;
            for (i = 1;i<=x;i=i+1){
                f = f * i;
            }
            return f;
        }
        void main()
        {
            int s, i ;
            i = 1;
            s = 0;
            do 
            {
                putIntLn(fact(i));
                i = i + 1;
            }while (i <= 10);
        
        }
        """
        expect = """1
2
6
24
120
720
5040
40320
362880
3628800
"""
        self.assertTrue(TestCodeGen.test(input, expect, 543))

    def testnested_with(self):
        input = """
        void main(){
            int x;
            x = 1;
            {
                int x; 
                x = 2;
                {
                    int x ; 
                    x = 3;
                    putInt(x);
                }
                putInt(x);
            }
        }
        """
        expect = """32"""
        self.assertTrue(TestCodeGen.test(input, expect, 544))

    def test_if_then_else(self):
        input = """

        int x;
        
        boolean foo()
        {
            putString("in foo");
            return false;
        }
    
        void main(){
            x = 10;
            if (x > 100 && foo())
                putStringLn("in then");
            else
                putStringLn("in else");
        }
        """
        expect = """in else\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 545))

    def test_if_then_elsse(self):
        input = """
        int x;
        
        boolean foo()
        {
            putString("in foo ");
            x = 1000;
            return true;
        }
    
        void main(){
            x = 10;

            if (x < 100 && foo()){
                putStringLn("in then");
            }
            else{
                putStringLn("in else");
                }
        }        """
        expect = """in foo in then\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 546))

    def test_in_foo(self):
        input = """
        int x;
        boolean foo()
        {
            putString("in foo ");
            return false;
        }
    
        void main(){
            x = 10;
            if (x < 100 && foo()) {
                putStringLn("in then");
            }
            else{
                putStringLn("in else");
                }
        }        """
        expect = """in foo in else\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 547))

    def test_nice(self):
        input = """
        int x;
        
        boolean foo()
        {
            putString("in foo ");
            x = 1000;
            return true;
        }
    
        void main(){
            x = 10;

            if (x > 100 && foo()){
                putStringLn("in then");
            }
            else{
                putStringLn("in else");
            }
    
            putIntLn(x);
    }        """
        expect = """in else\n10\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 548))

    def test_float(self):
        input = """
        float foo()
        {
            return 1;
        }

        void main(){
            putFloat(foo());
        }
        """
        expect = """1.0"""
        self.assertTrue(TestCodeGen.test(input, expect, 549))

    def test_gcd(self):
        input = """
        void main(){
            int x, y;
            x = 10;
            y = 12;
            putInt(gcd(x + y, x));
        }

        int gcd(int a,int b )
        {
            if (b == 0)
                return a;
            else
                return gcd(b, a % b);
        }"""
        expect = """2"""
        self.assertTrue(TestCodeGen.test(input, expect, 550))

    def test_assign(self):
        input = """
            int d;
            void main(){
                boolean a,b;
                string c;
                a = true;
                b = false;
                c = "ahihi";
                d = 1 + 2;
                putBool(a || b && ! b || false);
                putString(c);
                putInt(d);
            }
        """
        expect = "trueahihi3"
        self.assertTrue(TestCodeGen.test(input, expect, 551))

    def test_simple_putInt(self):
        input = """
        void main(){
            int x;
            x = 12;
            putInt(x);
            foo();
        }

        void foo(){
            putString("Hello world");
        }
        """
        expect = """12Hello world"""
        self.assertTrue(TestCodeGen.test(input, expect, 552))

    def test_factor(self):
        input = """
            void main(){
                int a,b;
                b = 6;
                a = factor(b);
                putInt(a);
            }
            int factor(int a)
            {
                if (a <= 1)
                    return 1;
                else
                    return a * factor(a-1);
            }
        """
        expect = """720"""
        self.assertTrue(TestCodeGen.test(input, expect, 553))

    def test_scope1(self):
        input = """
            void main(){
                int a;
                float b;
                a = 1;
                putInt(a);
                {
                    float a;
                    int b;
                    a = 1.5;
                    b = 1;
                    putFloat(a+b+0.15);
                }
                {
                    boolean a ;
                    boolean b;
                    b = true;
                    a = b;
                    putBool(a);
                }
                a = a + 2;
                putInt(3);
            }
        """
        expect = "12.65true3"
        self.assertTrue(TestCodeGen.test(input, expect, 554))

    def test_while1(self):
        input = """
            void main(){
                int a,i;
                float b;
                i = 8 ;
                a = 1 ;
                do {
                    a = a * i;
                    i = i - 1;
                    if (i == 4) break;
                }while (i>0);
                putInt(a);
            }
            """
        expect = "1680"
        self.assertTrue(TestCodeGen.test(input, expect, 555))

    def test_bool_ast5(self):
        input = """
            void main(){
                boolean a,b;
                a = true;
                b = false;
                putBool(a && b && a && ! b && test());
            }
            boolean test(){
                float a;
                boolean res;
                res = false;
                a = 9.5;
                putFloat(a);
                return res;
            }
            """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 556))

    def test_bool_ast6(self):
        input = """
            void main(){
                boolean a,b;
                a = true;
                b = false;
                putBool((a || test()) || a && ! b && test());
            }
            boolean test(){
                float a;
                boolean res;
                res = false;
                a = 9.5;
                putFloat(a);
                return res;
            }
            """
        expect = "9.5true"
        self.assertTrue(TestCodeGen.test(input, expect, 557))

    def test_for1(self):
        input = """
            void main(){
                int a,i;
                float b;

                up = 10;
                a = 0;
                for (i=up;i>1;i=i-1){
                    if (a > 40) continue;
                    a = a + i;
                }
                putInt(a);
            }
            int up;
            """
        expect = "45"
        self.assertTrue(TestCodeGen.test(input, expect, 558))

    def test_call_stmt1(self):
        input = """
            void main(){
                int a,b;
                b = 6;
                a = factor(b);
                putInt(a);
            }
            int factor(int a)
            {
                if (a <= 1)
                    return 1;
                else
                    return a * factor(a-1);
            }
        """
        expect = "720"
        self.assertTrue(TestCodeGen.test(input, expect, 559))

    def test_empty(self):
        input = """
        void main(){
        }
        """
        expect = """"""
        self.assertTrue(TestCodeGen.test(input, expect, 560))

    def test_int(self):
        input = """
        void main(){
            int a;
            a = 1;
            putInt(a);
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,561))

    def test_tree(self):
        input = """
        void main(){
            putFloat(100.02);
        }
        """
        expect = "100.02"
        self.assertTrue(TestCodeGen.test(input,expect,562))

    def test_simple_putFloat(self):
        input = """
        void main(){
            putFloat(1.4315E7);
        }
        """
        expect = "1.4315E7"
        self.assertTrue(TestCodeGen.test(input,expect,563))

    def test_float_and_putFloat(self):
        input = """
        void main(){
            putFloat(121.5E5);
        }
        """
        expect = "1.215E7"
        self.assertTrue(TestCodeGen.test(input,expect,564))

    def test_two_putInt(self):
        input = """
        void main(){
            if (true) putInt(1);
            else putInt(2);
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,565))

    def test_foo(self):
        input = """
        void main(){
            int a;
            a = 4;
            putFloatLn(foo(a));
        }
        float foo(int a){
            int foo;
            foo = 5;
            return foo + a;
        } 
        """
        expect = """9.0\n"""
        self.assertTrue(TestCodeGen.test(input,expect,566))

    def test_putLn(self):
        input = """
        void main(){
            putIntLn(000);
            putLn();
        }
        """
        expect = "0\n\n"
        self.assertTrue(TestCodeGen.test(input,expect,567))

    def test_float_put(self):
        input = """
        void main(){
            putFloatLn(1.0);
        }"""
        expect = "1.0\n"
        self.assertTrue(TestCodeGen.test(input,expect,568))

    def test_put_float(self):
        input = """
        void main(){
            putFloatLn(10.5);
        }
        """
        expect = "10.5\n"
        self.assertTrue(TestCodeGen.test(input,expect,569))
        
    def test_putFloatLn(self):
        input = """
        void main(){
            putFloatLn(100.14);
        }
        """
        expect = "100.14\n"
        self.assertTrue(TestCodeGen.test(input,expect,570))

    def test_putBool(self):
        input = """
        void main(){
            putBoolLn(true);
        }
        """
        expect = "true\n"
        self.assertTrue(TestCodeGen.test(input,expect,571))

    def test_manipulate(self):
        input = """
        void main(){
            int a;
            a = 2;
            if (a > 5)
                if (a % 2==0)
                    a = a * 2;
                else
                {
                }
            else {
                a = 11;
                if (a % 3 != 0)
                    a = a * 3 / 2;
            }
            putInt(a);
        }
        """
        expect = "16"
        self.assertTrue(TestCodeGen.test(input,expect,572))

    def test_dowhile_stmt_simple(self):
        input = """
        void main(){
            int a;
            a = 1;
            do
            {
                putInt(a);
                a = a + 1;
            }while (a < 5);
        }
        """
        expect = "1234"
        self.assertTrue(TestCodeGen.test(input,expect,573))

    def test_manipulate_continue(self):
        input = """
        void main(){
            int a, iSum;
            a = 0;
            iSum = 0;
            do
            {
                a = a + 1;
                if (a % 2==0) continue;
                iSum = iSum + a;
            }while (a < 20);
            putInt(iSum);
        }
        """
        expect = "100"
        self.assertTrue(TestCodeGen.test(input,expect,574))
        
    def test_while_has_break(self):
        input = """
        void main(){
            int a, iSum;
            a = 0;
            iSum = 0;
            do
            {
                a = a + 1;
                if (a > 17) break;
                iSum = iSum + a;
            }while (a < 20);
            putInt(iSum);
        }
        """
        expect = "153"
        self.assertTrue(TestCodeGen.test(input,expect,575))

    def test_while_has_break_and_continue(self):
        input = """
        void main(){
            int a, iSum;
            a = 0;
            iSum = 0;
            do
            {
                a = a + 1;
                if (a > 17) break;
                if (a % 2==0) continue;
                iSum = iSum + a;
            }while (a < 20);
            putInt(iSum);
        }
        """
        expect = "81"
        self.assertTrue(TestCodeGen.test(input,expect,576))

    def test_inner(self):
        input = """
        void main(){
            int a, b, iSum;
            a = b = iSum = 0;
            do
            {
                b = 0;
                a = a + 1;
                do
                {
                    b = b + 1;
                    iSum = iSum + b;
                }while (b < a);
                iSum = iSum + a;
            }while (a < 20);
            putInt(iSum);
        }
        """
        expect = "1750"
        self.assertTrue(TestCodeGen.test(input,expect,577))

    def test_continue_and_break(self):
        input = """
        void main(){
            int a, b, iSum;
            a = b = iSum = 0;
            do
            {
                b = 0;
                a = a + 1;
                do
                {
                    b = b + 1;
                    if (b > 10) break;
                    if (b % 2==1) continue;
                    iSum = iSum + b;
                }while (b < a); 
                if (a % b==0) continue;
                if (a + b > 40) break;
                iSum = iSum + a;
            }while (a < 20);
            putInt(iSum);
        }
        """
        expect = "554"
        self.assertTrue(TestCodeGen.test(input,expect,578))

    def test_putInt_in_for(self):
        input = """
        void main(){
            int a;
            for (a = 0;a<10;a=a+1){
                putInt(a);
                break;
            }
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,579))
        
    def test_sum(self):
        input = """
        void main(){
            int a, b, iSum;
            iSum = 0;
            for (a = 0;a<9;a=a+1){
                if (a % 2==0) continue;
                iSum = iSum + a;
            }
            putInt(iSum);
        }
        """
        expect = "25"
        self.assertTrue(TestCodeGen.test(input,expect,580))

    def test_break_sum(self):
        input = """
        void main(){
            int a, b, iSum;
            iSum = 0;
            for (a = 0;a<9;a=a+1){
                if (iSum > 27) break;
                iSum = iSum + a;
            }
            putInt(iSum);
        }
        """
        expect = "28"
        self.assertTrue(TestCodeGen.test(input,expect,581))

    def test_isum(self):
        input = """
        void main(){
            int a, b, iSum;
            iSum = 0;
            for (a = 0;a<9;a=a+1){
                if (iSum > 27) break;
                if (a % 3==0) continue;
                iSum = iSum + a;
            }
            putInt(iSum);
        }
        """
        expect = "27"
        self.assertTrue(TestCodeGen.test(input,expect,582))

    def test_isum_compicate(self):
        input = """void main(){
            int a, b, iSum;
            iSum = 0;
            for (a = 0;a<9;a=a+1){
                for (b = 0;b<a - 1;b=b+1){
                    if (a + b > 17) break;
                    if (b % 2==0) continue;
                    iSum = iSum + b;
                }
                if (iSum > 27) break;
                if (a % 3 != 0) continue;
                iSum = iSum + a;
            }
            putIntLn(iSum);
        }
        """
        expect = "37\n"
        self.assertTrue(TestCodeGen.test(input,expect,583))

    def test_put_float(self):
        input = """
        int i, j;
        void main(){
            int a, b, iSum;
            i = 10;
            {
                float i; 
                i = 11.8;
                putFloat(i);
            }
            i = 11;
            putIntLn(i);
        }
        """
        expect = "11.811\n"
        self.assertTrue(TestCodeGen.test(input,expect,584))

    def test_putInt(self):
        """Program ==> block manipulate data in Main function inner block"""
        input = """
        int i, j;
        void main(){
            int a, b, iSum;
            i = 10;
            {
                float i; 
                i = 14.3;
                {
                    int i; 
                    i = 19;
                    putInt(i);
                }
                putFloat(i);
            }
            putInt(i);
        }
        """
        expect = "1914.310" 
        self.assertTrue(TestCodeGen.test(input,expect,585))

    def test_putFloat(self):
        """Program ==> Funcall is stmt in main function"""
        input = """
        int a;
        void main(){
            int b;
            float c;
            b = 5;
            c = foo(b);
            putFloat(c);
        }
        
        int foo(int a)
        {
            return a * a;
        }
        """
        expect = "25.0"
        self.assertTrue(TestCodeGen.test(input,expect,586))

    def test_compication_if(self):
        """Program ==> return stmt in if-else stmt in function call"""
        input = """
        void main(){
            int a, b, res;
            a = 1;
            b = 1;
            res = foo(a, b);
            putIntLn(res);
        }
        
        int foo(int a, int b)
        {
            if (a==b) return 111;
                else return 222;
        }
        """
        expect = "111\n"
        self.assertTrue(TestCodeGen.test(input,expect,587))

    def test_put_int(self):
        input = """
            void main(){
                putIntLn(100);
                putIntLn(-100);
                putInt(0);
            }
        """
        expect = "100\n-100\n0"
        self.assertTrue(TestCodeGen.test(input,expect,588))

    def test_large_int_literal(self):
        input = """
            void main(){
                putIntLn(-2147483648);
                putIntLn(-1000000000 + 65565654);
                putFloatLn(-1000000000 / 65565654);
                putIntLn(2147483647);   
            }
        """
        expect = "-2147483648\n-934434346\n-15.0\n2147483647\n"
        self.assertTrue(TestCodeGen.test(input,expect,589))

    
    def test_float_literal(self):
        input = """
            void main(){
                putFloatLn(10.0);
                putFloatLn(1e3);
                putFloatLn(1e-3);
                putFloat(1.e-3);
            }
        """
        expect = "10.0\n1000.0\n0.001\n0.001"
        self.assertTrue(TestCodeGen.test(input,expect,590))

    def test_boolean_literal(self):
        input = """
            void main(){
                putBoolLn(true);
                putBool(false);
            }
        """
        expect = "true\nfalse"
        self.assertTrue(TestCodeGen.test(input,expect,591))
    
    def test_string_literal(self):
        input = """
            void main(){
                putStringLn("PPL");
                putString("2018");
            }
        """
        expect = "PPL\n2018"
        self.assertTrue(TestCodeGen.test(input,expect,592))

    def test_binary_op_with_add(self):
        input = """
            void main(){
                putIntLn(1 + 2);
                putFloatLn(1 + 2.0);
                putFloatLn(1.23 + -9.34);
                putFloat(1.2376 + -9);
            }
        """
        expect = "3\n3.0\n-8.110001\n-7.7624"
        self.assertTrue(TestCodeGen.test(input,expect,593))

    def test_binary_op_with_sub(self):
        input = """
            void main(){
                putIntLn(1 - 2);
                putFloatLn(1 - 2.0);
                putFloatLn(1.23 - -9.34);
                putFloat(1.2376 - -9);
            }
        """
        expect = "-1\n-1.0\n10.57\n10.2376"
        self.assertTrue(TestCodeGen.test(input,expect,594))

    def test_binary_op_with_divide(self):
        input = """
            void main(){
                putFloatLn(14/2);
                putFloatLn(13 / 2.08783);
                putFloatLn(158.2035564 / --236.256885);
                putFloat(122.23762 / ---9);
            }
        """
        expect = "7.0\n6.2265606\n0.66962516\n-13.581958"
        self.assertTrue(TestCodeGen.test(input,expect,595))

    def test_binary_op_with_mul(self):
        input = """
            void main(){
                putFloatLn(14/-2.0);
                putFloatLn(13 * 2.08783);
                putFloatLn(158.2035564 * -236.256885);
                putFloat(122.23762 * 9);
            }
        """
        expect = "-7.0\n27.14179\n-37376.68\n1100.1385"
        self.assertTrue(TestCodeGen.test(input,expect,596))


    def test_binary_op_add_int(self):
        input = """
            void main(){
                putInt(1+2+30);
            }
        """
        expect = "33"
        self.assertTrue(TestCodeGen.test(input,expect,597))
    
    def test_binary_op_divide(self):
        input = """
            void main(){
                putFloat(1*45+30/12);
            }
        """
        expect = "47.0"
        self.assertTrue(TestCodeGen.test(input,expect,598))
    
    def test_binary_op_div_int(self):
        input = """
            void main(){
                putInt(100 / 3 / 2);
            }
        """
        expect = "16"
        self.assertTrue(TestCodeGen.test(input,expect,599))

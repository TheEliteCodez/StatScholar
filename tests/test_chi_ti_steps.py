import contextlib
import io
import re
import unittest
from unittest.mock import patch

import STCORE as c
import STCHIM as math
import STCHITI as ti


class TiChiSteps(unittest.TestCase):
    def test_gof_instructions_use_counts_and_adjusted_df(self):
        pages=[]
        with patch.object(c,'ON_TI',False),patch.object(c,'menu',side_effect=['1','3']),patch.object(c,'view',side_effect=lambda title,lines:pages.append(list(lines))),patch('builtins.input',side_effect=['dice','.05','3','10','20','30','1/6','1/3','1/2','1']),contextlib.redirect_stdout(io.StringIO()):
            c.call('STCHI','session')
        text='\n'.join(pages[1])
        self.assertTrue(text.startswith('TI-84: GOF BUTTON STEPS'))
        self.assertIn('STAT > TESTS > chi2GOF-Test',text)
        self.assertIn('Observed: L1; Expected: L2.',text)
        self.assertIn('df=1 (INCLUDING ANY FITTED-PARAMETER ADJUSTMENT).',text)
        for i,count in enumerate((10,20,30)):
            self.assertIn('ROW %d: L1=%d; L2=%d'%(i+1,count,count),text)
        self.assertIn('chi2cdf(0,1E99,1)',text)
        self.assertIn('E1: chi2cdf(X,1E99,1)',text)
        self.assertIn('E2: 0.05',text)

    def test_independence_instructions_preserve_matrix_orientation(self):
        observed=[35,62,20,21,65,33]
        expected,ts,df,_,_=math.independence([observed[:3],observed[3:]])
        text='\n'.join(ti.steps(observed,expected,3,df,.05,ts,math.survival(ts,df),math.critical(.05,df),True))
        self.assertIn('SET SIZE: 2 ROWS, 3 COLS.',text)
        self.assertIn('Observed: [A]; Expected: [B].',text)
        for i,value in enumerate(observed):
            self.assertIn('[A](%d,%d)=%d'%(i//3+1,i%3+1,value),text)
        self.assertNotIn('chi2GOF-Test',text)

    def test_displayed_cdf_and_cv_equation_reproduce_numeric_answers(self):
        for df,ts,alpha in ((1,20,.05),(3,10,.05),(4,1.875,.01)):
            p=math.survival(ts,df);cv=math.critical(alpha,df)
            text='\n'.join(ti.steps([20,20],[20,20],2,df,alpha,ts,p,cv))
            command=re.search(r'^chi2cdf\(([^,]+),1E99,(\d+)\)$',text,re.M)
            self.assertAlmostEqual(math.survival(float(command[1]),int(command[2])),p,places=10)
            equation=re.search(r'0=, ENTER chi2cdf\(X,1E99,(\d+)\)-([^\n]+)',text)
            self.assertAlmostEqual(math.survival(cv,int(equation[1]))-float(equation[2]),0,places=10)
            upper=float(re.search(r'bound=\{0,([^}]+)\}',text)[1])
            self.assertGreater(upper,cv)
            self.assertGreater(math.survival(0,df),alpha)
            self.assertLess(math.survival(upper,df),alpha)


if __name__=='__main__':unittest.main()

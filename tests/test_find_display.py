import contextlib
import io
import unittest
from unittest.mock import patch
import STCORE as c
import STFIND as find
import STPRE as pre
import STWORDS as words
import STVIEW as display
import STNORM as normal
from test_expansion import flow


class FindDisplay(unittest.TestCase):
    def test_specific_words_before_general_comparisons(self):
        for phrase in ('half below','half are below','50% below'):
            self.assertEqual(find.search_methods(phrase)[0][1],'W:median')
        for phrase,token in [('not','not'),('does not','not'),('every kth','sampling'),
                             ('no fewer than','>='),('not more than','<='),
                             ('below','<'),('at least one','one')]:
            self.assertEqual(find.recognition(phrase),token)

    def test_complement_solver_from_word(self):
        output,_=flow(lambda:words.word_route('not'),['1','.3','1'])
        self.assertIn('0.7000',output)
        for word,module,method in [('median','STDATA','raw_session'),
                                   ('sampling','STSTUDY','sampling_menu')]:
            with patch.object(c,'view'),patch.object(c,'call') as dispatch:
                words.word_route(word)
            dispatch.assert_called_once_with(module,method)

    def test_paper_name_and_question_number_are_distinct(self):
        self.assertEqual(pre.search('practice test 1'),[])
        self.assertIn('X:pretest',[route for _,route in find.search_methods('practice test 1')])
        for query in ('pretest24','pretest 24','practice test 1 question 24'):
            self.assertEqual(pre.search(query)[0][0],'PR:24')
        self.assertEqual(pre.search('birth weights')[0][0],'PR:24')

    def test_answer_separate_from_requested_method_and_format(self):
        screens=[]
        with patch.object(c,'view',side_effect=lambda title,lines:screens.append((title,list(lines)))),patch.object(c,'menu',side_effect=['5','3','1']):
            display.results('ANSWER',[('P',(1,3))],['TRANSLATION','FORMULA','EXPLANATION'])
        self.assertEqual(screens[0][1],['P=0.3333'])
        self.assertEqual(screens[1],('WORK / FORMULA',['TRANSLATION','FORMULA','EXPLANATION']))
        self.assertEqual(screens[-1][1],['P=1/3'])

    def test_table_arrows_still_change_rows_with_method_option(self):
        screens=[]
        with patch.object(c,'view',side_effect=lambda title,lines:screens.append((title,list(lines)))),patch.object(c,'read_choice',side_effect=['N','5','P','0']),contextlib.redirect_stdout(io.StringIO()):
            display.paged_results('TABLE',9,lambda i:('ROW '+str(i),i),['TABLE METHOD'])
        self.assertIn('ROWS 8..9/9',screens[1][1])
        self.assertEqual(screens[2],('WORK / FORMULA',['TABLE METHOD']))
        self.assertIn('ROWS 1..7/9',screens[-1][1])

    def test_aligned_axes_values_markers_and_width(self):
        lines=normal.axis_lines((42,1),(3,1),-1,((42,1),))
        self.assertEqual(lines[0].index('*'),14)
        self.assertEqual(lines[3],lines[4])
        self.assertEqual([i for i,v in enumerate(lines[3]) if v=='|'],[4,14,24])
        self.assertEqual(lines[2].split(),['-1','0','1'])
        self.assertEqual(lines[5].split(),['39','42','45'])
        self.assertTrue(all(len(line)<=30 for line in lines))
        long=normal.axis_lines((1234567890123,1),(1,3),-1)
        self.assertIn('A=',str(long))
        self.assertTrue(all(len(line)<=30 for line in long[:6]))
        # An off-panel observation must not be clamped onto an endpoint.
        self.assertNotIn('*',''.join(normal.axis_lines((42,1),(3,1),-1,((60,1),))))

    def test_axes_real_arrow_paging(self):
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[1,1,2,9],create=True),contextlib.redirect_stdout(io.StringIO()) as output:
            normal.show_axes('ALIGNED AXES',(42,1),(3,1))
        text=output.getvalue()
        self.assertIn('z: -3 TO -1',text)
        self.assertIn('z: 1 TO 3',text)
        self.assertEqual(text.count('z: -1 TO 1'),2)


if __name__=='__main__': unittest.main()

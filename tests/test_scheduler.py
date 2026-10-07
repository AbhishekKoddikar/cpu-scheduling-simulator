import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from scheduler import Process, fcfs, sjf, priority_scheduling, round_robin, simulate

class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.ps=[Process('P1',0,5,2),Process('P2',1,3,1),Process('P3',2,1,3)]

    def test_fcfs(self):
        r=fcfs(self.ps)
        self.assertEqual([x['completion'] for x in r['processes']], [5,8,9])
        self.assertAlmostEqual(r['average_waiting_time'], (0+4+6)/3)

    def test_sjf(self):
        r=sjf(self.ps)
        self.assertEqual([x['completion'] for x in r['processes']], [5,9,6])

    def test_priority_lower_number_wins(self):
        r=priority_scheduling(self.ps)
        self.assertEqual(r['gantt'][1]['pid'], 'P2')

    def test_round_robin(self):
        r=round_robin(self.ps, 2)
        self.assertEqual(r['makespan'], 9)
        self.assertTrue(all(x['waiting'] >= 0 for x in r['processes']))

    def test_idle_time(self):
        r=fcfs([Process('P1',3,2,1)])
        self.assertEqual(r['gantt'][0]['pid'], 'IDLE')
        self.assertEqual(r['gantt'][0]['end'], 3)

    def test_all_algorithms(self):
        r=simulate(self.ps,2)
        self.assertEqual(set(r['results']), {'FCFS','SJF','Round Robin','Priority'})
        self.assertEqual(len(r['comparison']),4)

if __name__=='__main__': unittest.main()

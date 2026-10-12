import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).parents[1]/'experiments/parallel_instruct/gpu_ownership.py'
s=importlib.util.spec_from_file_location('ownership',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class OwnershipTests(unittest.TestCase):
    devices='0, GPU-a\n1, GPU-b\n2, GPU-c\n3, GPU-d\n'
    def test_one_two_four_gpu_scopes(self):
        self.assertEqual(m.assigned_uuids(self.devices,None,1),{'GPU-a'})
        self.assertEqual(m.assigned_uuids(self.devices,None,2),{'GPU-a','GPU-b'})
        self.assertEqual(len(m.assigned_uuids(self.devices,None,4)),4)
    def test_visible_order_and_other_gpu_workers(self):
        assigned=m.assigned_uuids(self.devices,'2,0',2)
        self.assertEqual(assigned,{'GPU-c','GPU-a'})
        self.assertEqual(m.owned_processes('GPU-b, 123\nGPU-d, 456\n',assigned),[])
        self.assertEqual(m.owned_processes('GPU-a, 345\nGPU-b, 123\n',assigned),[345])
        self.assertEqual(m.assigned_uuids(self.devices,'GPU-d,GPU-c',1),{'GPU-d'})
    def test_invalid_or_ambiguous_assignment_fails(self):
        for visible,n in [('0',2),('0,0',2),('99',1),('',1),('GPU-',1)]:
            with self.assertRaises(ValueError):m.assigned_uuids(self.devices,visible,n)
        with self.assertRaises(ValueError):m.assigned_uuids(self.devices,None,5)
if __name__=='__main__':unittest.main()

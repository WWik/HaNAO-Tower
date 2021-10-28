"""
Test support for parametrized increment/decrement values in numeric effects
"""
from __future__ import print_function
from pyddl import Domain, Problem, Action, planner, neg

def problem(verbose):
    domain = Domain((
        Action(
            'move',
            parameters=(
                ('position', 'X'),
                ('position', 'Y'),
                ('position', 'Z'),
            ),
            preconditions=(
                ('Clear',  'X'),
                ('Clear', 'Z'),
                ('On', 'X',  'Y'),
                ('smaller', 'X', 'Z'),
            ),
            effects=(
                neg(('Clear', 'Z')),
                neg(('On',  'X', 'Y')),
                ('Clear', 'Y'),
                ('Clear', 'X'),
                ('On',  'X',  'Z'),
            ),
        ),
    ))
    problem = Problem(
        domain,
        {
            'position': ('Disk1','Disk2','Disk3','start','middle','finish'),
        },
        init=(
            ('Clear', 'Disk1'),
            ('Clear',  'middle'),
            ('Clear',  'finish'),

            ('On',  'Disk1', 'Disk2'),
            ('On', 'Disk2', 'Disk3'),
            ('On', 'Disk3', 'start'),

            ('smaller',  'Disk1',   'Disk2'),
            ('smaller',  'Disk1',   'Disk3'),
            ('smaller',  'Disk1',   'start'),
            ('smaller',  'Disk1',   'middle'),
            ('smaller',  'Disk1',   'finish'),

            ('smaller',  'Disk2',   'Disk3'),
            ('smaller',  'Disk2',   'start'),
            ('smaller',  'Disk2',   'middle'),
            ('smaller',  'Disk2',   'finish'),
            
            ('smaller',  'Disk3',   'start'),
            ('smaller',  'Disk3',   'middle'),
            ('smaller',  'Disk3',   'finish'),

        ),
        goal=(
            ('Clear',  'start'),
            ('Clear',  'middle'),
            ('Clear',  'Disk1'),
            ('On',  'Disk1',  'Disk2'),
            ('On',  'Disk2',  'Disk3'),
            ('On',  'Disk3', 'finish'),
        )
    )
    lista=[]
    plan = planner(problem, verbose=verbose)
    if plan is None:
        print('No Plan!')
    else:
        state = problem.initial_state
        for action in plan:
            if verbose: print(action)
            lista.append(str(action))
            state = state.apply(action)
            if verbose: print(state.f_dict)
    return lista

def runquiet():
    plan=problem(verbose=False)
    print(plan)

if __name__ == '__main__':
    # from optparse import OptionParser
    # parser = OptionParser(usage="Usage: %prog [options]")
    # parser.add_option('-q', '--quiet',
    #                   action='store_false', dest='verbose', default=True,
    #                   help="don't print statistics to stdout")

    # # Parse arguments
    # opts, args = parser.parse_args()
    # plan=problem(opts.verbose)
    # print(plan)
    runquiet()
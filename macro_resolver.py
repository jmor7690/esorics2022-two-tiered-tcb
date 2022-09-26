"""
Compile the "extended proverif" file "script.epv" to a regular
proverif file "script.pv" with a command like this:
      python3 macro_resolver.py -i script.epv -o script.pv -r "i<[i_max], j<[j_max], k<[k_max]"

Example:
      python3 macro_resolver.py -i mtcb_prov.epv -o mtcb_prov.pv -r "i<2,j<5"

Actions of macro_resolver:
    For each declaration in the file that has this shape:
        @macro MACRONAME_i { MACROBODY } { MACROEND } 
    
    macro_resolver does this:
        while True:
             Find an occurrence of MACRONAME_X in the file, where X is an integer
             If there are no occurrences, break out of the loop
             If X <= i_max:
                 Replace the occurrence with MACROBODY[_X/_i, _X+1/_i']
             Else:
                 Replace the occurrence with MACROEND 
"""

from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument('--inputfile','-i', help='Input file', type=str)
parser.add_argument('--outputfile', '-o', help='Output file', type=str, default='')
parser.add_argument('--ranges', '-r', help='Ranges for variables', type=str, default='i<5')
parser.add_argument('--verbose','-v', action='store_true')
args = parser.parse_args()

if args.outputfile == "": args.outputfile = args.inputfile.replace(".epv", ".pv")

with open(args.inputfile, "r") as f:
    prog = f.read()


vars_range = {}
for r in args.ranges.split(","):
    try:
        r = r.strip()
        range_var = r[0]
        assert( r[1] == "<")
        range_max = int(r[2:])
        vars_range[range_var] = range_max
        if args.verbose: print(f"Range for {range_var} is 0..{range_max}")
    except:
        print(f"Error: the range declaration looks wrong")
        print(f"range: {r}")
        print(f"ranges string: {args.ranges}")
        exit()
        
    
# regexp for macro
pat_macro = re.compile("@macro +([a-zA-Z]+)_([a-zA-Z]+) *{([^}]*)} *{([^}]*)}", re.DOTALL)

# Gather the macro definitions in a list
macro_list = []

while True:
    m = pat_macro.search(prog)
    if not m: break
    macro_name = m.group(1)
    macro_var = m.group(2)
    macro_body = m.group(3)
    macro_end = m.group(4)
    if args.verbose:
        print("Macro found:")
        print("name:", macro_name)
        print("var:", macro_var)
        print("body:", macro_body)
        print("end:", macro_end)
    if macro_body.find("@macro") > -1:
        print(f"Warning: looks like a nested macro in {macro_name}, but I'll proceed.")
    macro_list.append((macro_name, macro_var, macro_body, macro_end))
    prog = prog[:m.start()] + prog[m.end():]

if args.verbose: print("=== starting processing ===")

# Replace macro calls with macro body + substitutions
prog_changes = True
while prog_changes:
    prog_changes = False
    for (macro_name, macro_var, macro_body, macro_end) in macro_list:
        p = re.compile(macro_name + r'_(\d+)')
        m = p.search(prog)
        if not m: continue # no more occurrences of macro_name to substitute
        macro_arg = int(m.group(1))
        if macro_var not in vars_range:
            print(f"Error: variable {macro_var} not bound in ranges declaration: {args.ranges}")
            exit()
        if macro_arg < vars_range[macro_var]:
            macro_subst = macro_body
            macro_subst = re.sub(f"_{macro_var}'", f"_{macro_arg+1}", macro_subst)
            macro_subst = re.sub(r"\b"+macro_var+"'", f"{macro_arg+1}", macro_subst)
            macro_subst = re.sub(f"_{macro_var}", f"_{macro_arg}", macro_subst)
            macro_subst = re.sub(r"\b"+macro_var+r"\b", f"{macro_arg}", macro_subst)
            prog_changes = True
        else:
            macro_subst = macro_end
            prog_changes = True
        if args.verbose:
            print(f"REPLACING {m.group(0)} WITH")
            print(macro_subst)
            
        macro_subst = "(* " + macro_name + "-" + str(macro_arg) + " *)\n" + macro_subst
        prog = prog[:m.start()] + macro_subst + prog[m.end():]

with open(args.outputfile, "w") as f:
    f.write(prog)

    


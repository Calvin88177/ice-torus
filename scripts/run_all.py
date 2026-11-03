"""Regenerate every figure into ../figures and the structural report into ../analysis."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
SCRIPTS = ["torus_3d.py", "section_plan.py", "arch_options.py", "formwork.py",
           "compass_cables.py", "leapfrog_rails.py", "pitch_figs.py", "ice_properties.py"]
os.makedirs(FIG, exist_ok=True)
for s in SCRIPTS:
    print("->", s)
    subprocess.run([sys.executable, os.path.join(HERE, s)], cwd=FIG, check=True, stdout=subprocess.DEVNULL)
ana = os.path.join(ROOT, "analysis")
subprocess.run([sys.executable, "calc.py"], cwd=ana, check=True, stdout=subprocess.DEVNULL)
subprocess.run([sys.executable, "make_tex_en.py"], cwd=ana, check=True)
print("Figures written to", FIG)
print("LaTeX source written to analysis/structural_integrity_EN.tex (build with latexmk -pdf)")

# Main.py

from compiler import TokenCompiler

# Filename
filename = './YALex/slr.yal'
output = 'NFA_Visualization'

# TokenCompiler instance
analyzer = TokenCompiler(filename)
analyzer.compileTokens(output)

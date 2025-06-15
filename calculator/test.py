import subprocess

expression = "3 + 7 * 2"

result = subprocess.run(['python', 'main.py', expression], capture_output=True, text=True, cwd='./calculator')

print(result.stdout)
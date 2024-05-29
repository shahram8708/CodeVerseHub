from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

def run_code(code, language):
    supported_languages = {
        'assembly': 'asm',
        'ada': 'adb',
        'algol': 'alg',
        'bash': 'sh',
        'basic': 'bas',
        'c': 'c',
        'csharp': 'cs',
        'cpp': 'cpp',
        'cobol': 'cob',
        'crystal': 'cr',
        'dart': 'dart',
        'delphi': 'pas',
        'd': 'd',
        'elixir': 'ex',
        'elm': 'elm',
        'erlang': 'erl',
        'fsharp': 'fs',
        'forth': 'fth',
        'fortran': 'f90',
        'go': 'go',
        'groovy': 'groovy',
        'haskell': 'hs',
        'html': 'html',
        'idris': 'idr',
        'io': 'io',
        'java': 'java',
        'javascript': 'js',
        'julia': 'jl',
        'kotlin': 'kt',
        'lisp': 'lisp',
        'lua': 'lua',
        'matlab': 'm',
        'nim': 'nim',
        'objc': 'm',
        'ocaml': 'ml',
        'pascal': 'pas',
        'perl': 'pl',
        'php': 'php',
        'prolog': 'pl',
        'python': 'py',
        'r': 'r',
        'ruby': 'rb',
        'rust': 'rs',
        'scala': 'scala',
        'scheme': 'scm',
        'scratch': 'sb2',
        'shell': 'sh',
        'smalltalk': 'st',
        'solidity': 'sol',
        'sql': 'sql',
        'swift': 'swift',
        'tcl': 'tcl',
        'typescript': 'ts',
        'vhdl': 'vhdl',
        'vbnet': 'vb',
        'webassembly': 'wasm',
        'zig': 'zig',
        'css': 'css'
    }

    if language not in supported_languages:
        return "Language not supported yet.", 400

    filename = f'code.{supported_languages[language]}'
    with open(filename, 'w') as f:
        f.write(code)

    try:
        if language in ['python', 'javascript', 'ruby', 'go', 'php', 'perl', 'r', 'swift', 'typescript', 'bash', 'sh']:
            cmd = f'{language} {filename}'
        elif language == 'java':
            cmd = f'javac {filename} && java {filename.split(".")[0]}'
        elif language == 'kotlin':
            cmd = f'kotlinc {filename} -include-runtime -d {filename.split(".")[0]}.jar && java -jar {filename.split(".")[0]}.jar'
        elif language in ['c', 'cpp', 'objc']:
            executable = filename.split('.')[0]
            compiler = 'gcc' if language == 'c' else 'g++'
            cmd = f'{compiler} {filename} -o {executable} && ./{executable}'
        elif language == 'rust':
            cmd = f'rustc {filename} && ./{filename.split(".")[0]}'
        elif language == 'haskell':
            cmd = f'ghc {filename} -o {filename.split(".")[0]} && ./{filename.split(".")[0]}'
        elif language == 'assembly':
            cmd = f'nasm -f elf64 {filename} && ld -s -o {filename.split(".")[0]} {filename.split(".")[0]}.o && ./{filename.split(".")[0]}'
        elif language == 'html':
            cmd = f'cat {filename}'  
        elif language == 'sql':
            cmd = f'sqlite3 :memory: < {filename}' 
        elif language == 'elixir':
            cmd = f'elixir {filename}'
        elif language == 'erlang':
            cmd = f'erlc {filename} && erl -noshell -s {filename.split(".")[0]} -s init stop'
        elif language == 'fortran':
            executable = filename.split('.')[0]
            cmd = f'gfortran {filename} -o {executable} && ./{executable}'
        elif language == 'fsharp':
            cmd = f'fsharpc {filename} && mono {filename.split(".")[0]}.exe'
        elif language == 'groovy':
            cmd = f'groovy {filename}'
        elif language == 'julia':
            cmd = f'julia {filename}'
        elif language == 'lua':
            cmd = f'lua {filename}'
        elif language == 'nim':
            cmd = f'nim compile --run {filename}'
        elif language == 'ocaml':
            cmd = f'ocaml {filename}'
        elif language == 'pascal':
            executable = filename.split('.')[0]
            cmd = f'fpc {filename} && ./{executable}'
        elif language == 'smalltalk':
            cmd = f'gst {filename}'
        elif language == 'solidity':
            cmd = f'solc --bin --abi {filename}'
        elif language ==         'tcl':
            cmd = f'tclsh {filename}'
        elif language == 'vhdl':
            cmd = f'ghdl -a {filename} && ghdl -e {filename.split(".")[0]} && ghdl -r {filename.split(".")[0]}'
        elif language == 'webassembly':
            cmd = f'wasmer {filename}' 
        elif language == 'zig':
            cmd = f'zig build-exe {filename} && ./{filename.split(".")[0]}'
        else:
            return "Language support needs specific implementation.", 500

        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = str(e)

    os.remove(filename)
    return output, 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')

    output, status = run_code(code, language)
    return jsonify({'output': output}), status

if __name__ == '__main__':
    app.run(debug=True)


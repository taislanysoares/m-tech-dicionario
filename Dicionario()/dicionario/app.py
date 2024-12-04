from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

def search_word(query):
    results = []
    try:
        with open('dictionary.txt', 'r') as file:
            content = file.read()
            entries = content.split('\n---\n')  # Divide o conteúdo em topicos baseadas nos separadores '---'
            for entry in entries:
                lines = entry.strip().split('\n')
                if not lines:
                    continue
                
                header = lines[0].strip()
                if header.startswith('# '):
                    word = header[2:].strip()
                    if query.lower() in word.lower():
                        description = '\n'.join(lines[1:]).strip()
                        results.append({
                            'word': word,
                            'description': description
                        })
    except FileNotFoundError:
        print("O arquivo 'dictionary.txt' não foi encontrado.")
    return results

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').strip()
    results = search_word(query)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='192.168.1.78', port=5000, debug=True)

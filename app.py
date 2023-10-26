from flask import Flask, request, jsonify
from sympy import symbols, S, limit

app = Flask(__name__)
x = symbols('x')


def resolver_limite(expressao, variavel, ponto):
    passos = []
    try:
        resultado_direto = limit(expressao, variavel, ponto)
    except Exception as e:
        return {"erro": str(e)}, 500

    passos.append({
        "acao": "Avaliar o limite diretamente",
        "etapa": "1",
        "expressao": str(expressao),
        "resultado": str(resultado_direto)
    })

    if resultado_direto == S.NaN:
        # Caso de indeterminação, simplificar
        passos_simplificacao = [
            "Simplificação inicial: {}".format(str(expressao))]
        # Adicione lógica de simplificação aqui
        # Substitua isso após a lógica de simplificação
        expressao_simplificada = expressao

        passos.append({
            "acao": "Simplificar a expressão",
            "etapa": "2",
            "passos_simplificacao": passos_simplificacao,
            "resultado": str(expressao_simplificada)
        })

        try:
            resultado_limite = limit(expressao_simplificada, variavel, ponto)
        except Exception as e:
            return {"erro": str(e)}, 500

        passos.append({
            "acao": "Avaliar o limite da expressão simplificada",
            "etapa": "3",
            "expressao": str(expressao_simplificada),
            "resultado": str(resultado_limite)
        })

        return {"passos": passos, "resultado": str(resultado_limite)}

    return {"passos": passos, "resultado": str(resultado_direto)}


@app.route('/limite', methods=['POST'])
def limite():
    data = request.json
    expressao = data.get('expressao', '')
    variavel = data.get('variavel', 'x')
    ponto = data.get('ponto', 0)

    return jsonify(resolver_limite(expressao, variavel, ponto))


if __name__ == '__main__':
    app.run(debug=True)

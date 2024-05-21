from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from parser.parser import Parser
from environment.ast import Ast
from environment.generator import Generator
from environment.environment import Environment
from environment.execute import RootExecuter
from environment.errores import extraer_datos, limpiar_errores
from environment.table import extraer_datos_tabla,limpiar_tabla

app = Flask(__name__)
CORS(app)

# Ruta para recibir datos mediante POST
@app.route('/interpreter', methods=['POST'])
def submit_data():
    
    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    input_data = data.get("code")
    print(input_data)
    # Limpiar tabla de simbolos
    limpiar_tabla()
    # Limpiar errores
    limpiar_errores()
       
    # Creación del entorno global
    env = Environment(None, 'GLOBAL')
    # Creación del AST
    ast = Ast()
    # Creacion del generador
    gen = Generator()
    # Creación del parser
    parser = Parser()

    # [inst1, inst2, inst2]
    instructionsArr = parser.interpretar(input_data ,ast)
    try:
        # Ejecución
        RootExecuter(instructionsArr, ast, env, gen)
        data_errors = extraer_datos()
        data_tabla = extraer_datos_tabla()
        for datas in data_tabla:
            print(datas)

        if data_errors:
            print("Hay errores")

        # Estructurando respuesta
        res = {"result": True,"console":gen.get_final_code(),"errores":data_errors, "tabla_simbolos":data_tabla}
        return jsonify(res)
    except Exception as e:
        print(e)
        data_errors = extraer_datos()
        res = {"result":False, "console":"Error","errores":data_errors}
        return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
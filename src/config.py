from flask.json.provider import DefaultJSONProvider
"""
config.py

Configura a aplicação Flask para diferentes ambientes de operação (desenvolvi-
mento e produção) e configurações de autenticação, documentação e modelos

Classes:
- ConfigDev: configurações para o ambiente de desenvolvimento.
- ConfigProd: configurações para o ambiente de produção.
- CustomJSONProvider: sobreposição de métodos padrão json no Flask.
"""
class ConfigDev:
    """
    Configurações para o ambiente de desenvolvimento.
    ---
    Atributos:
        DEBUG (bool): ativa o modo de debug do Flask.
        JWT_SECRET_KEY (str): defini a chave de segurança para assinar o JWT.
        JSONIFY_PRETTYPRINT_REGULAR (bool): formatação da saída do json para fa-
        cilitar a leitura.
        SWAGGER (dict): configurações de documentação do Swagger.
        CACHE_TYPE: ativa o cache em memória local para projetos simples e 
        testes.
    """
    DEBUG = True
    JWT_SECRET_KEY = 'Nem_toda_senha_sera_segura'
    JSONIFY_PRETTYPRINT_REGULAR = True
    SWAGGER = {
    "title":"Embrapa's API",
    "uiversion":3
}
    CACHE_TYPE = 'simple'

class ConfigProd:
    """
    Configurações para o ambiente de produção.
    ---
    Atributos:
        DEBUG (bool): desativa o modo de debug do Flask, por questões de segu-
        rança.
    """
    DEBUG = False

class CustomJSONProvider(DefaultJSONProvider):
    """
    Sobreposição de métodos padrão json no Flask.
    ---
    Métodos:
        dumps: convete dicionários Python para json.
        Atributos:
            self: instância da classe CustomJSONProvider.
            obj: objeto Python que será convertido para json.
            **kwargs: captura todos os argumentos nomeados passados para o 
            método.
        loads: converte json para dicionários Python.
        Atributos:
            self: instância da classe CustomJSONProvider.
            s: json string que será convertida para dicionário Python.
            **kwargs: captura todos os argumentos nomeados passados para o 
            método.
    """
    def dumps(self, obj, **kwargs):
        kwargs.setdefault('ensure_ascii', False)
        kwargs.setdefault('sort_keys', False)
        return super().dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return super().loads(s, **kwargs)


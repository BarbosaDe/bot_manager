from squarecloud.errors import (
    ApplicationNotFound,
    BadMemory,
    BadRequestError,
    FewMemory,
    InvalidConfig,
    InvalidDisplayName,
    InvalidDomain,
    InvalidFile,
    InvalidMain,
    InvalidMemory,
    InvalidStart,
    InvalidVersion,
    MissingConfigFile,
    MissingDependenciesFile,
    MissingDisplayName,
    MissingMainFile,
    MissingMemory,
    MissingVersion,
    NotFoundError,
    RequestError,
    TooManyRequests,
)

EXCEPTION_TRANSLATIONS = {
    RequestError.__name__: "Erro ao processar a requisição.",
    NotFoundError.__name__: "Recurso não encontrado (404).",
    BadRequestError.__name__: "Requisição malformada (400).",
    ApplicationNotFound.__name__: "Aplicação não encontrada.",
    InvalidFile.__name__: "Arquivo inválido.",
    MissingConfigFile.__name__: "Arquivo de configuração ausente.",
    MissingDependenciesFile.__name__: "Arquivo de dependências ausente.",
    TooManyRequests.__name__: "Muitas requisições. Tente novamente mais tarde.",
    FewMemory.__name__: "Memória insuficiente para hospedar a aplicação.",
    BadMemory.__name__: "Você não possui memória disponível para hospedar a aplicação.",
    InvalidConfig.__name__: "Arquivo de configuração inválido ou corrompido.",
    InvalidDisplayName.__name__: "Nome de exibição inválido no arquivo de configuração.",
    MissingDisplayName.__name__: "Nome de exibição ausente no arquivo de configuração.",
    InvalidMain.__name__: "Arquivo principal inválido no arquivo de configuração.",
    MissingMainFile.__name__: "Arquivo principal ausente no arquivo de configuração.",
    InvalidMemory.__name__: "Valor de memória inválido no arquivo de configuração.",
    MissingMemory.__name__: "Valor de memória ausente no arquivo de configuração.",
    InvalidVersion.__name__: "Versão inválida no arquivo de configuração.",
    MissingVersion.__name__: "Versão ausente no arquivo de configuração.",
    InvalidDomain.__name__: "Domínio personalizado inválido.",
    InvalidStart.__name__: "Valor de inicialização inválido no arquivo de configuração.",
}


def get_translated_exception_message(exc: Exception) -> str:
    exc_type = type(exc)

    for cls in exc_type.__mro__:
        if cls.__name__ in EXCEPTION_TRANSLATIONS:
            base_msg = EXCEPTION_TRANSLATIONS[cls.__name__]
            break
    else:
        base_msg = "Ocorreu um erro inesperado."

    return base_msg


class DuplicateEntryError(Exception): ...

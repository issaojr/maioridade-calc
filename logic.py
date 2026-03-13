from datetime import datetime, date
import calendar


class DataFuturaError(ValueError):
    """Levantada quando a data de nascimento é posterior a hoje."""


def _normalizar_data(data: str) -> str:
    """Aceita DD/MM/AAAA ou DDMMAAAA e retorna DD/MM/AAAA."""
    digits = data.replace("/", "").strip()
    if len(digits) == 8:
        return f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"
    return data  # deixa o strptime levantar o erro


def calcular_maioridade(data_nascimento: str) -> str:
    """Retorna a data (DD/MM/AAAA) em que a pessoa completa 18 anos."""
    data = _normalizar_data(data_nascimento)
    nascimento = datetime.strptime(data, "%d/%m/%Y").date()
    try:
        maioridade = nascimento.replace(year=nascimento.year + 18)
    except ValueError:  # 29/02 em ano não-bissexto
        maioridade = nascimento.replace(year=nascimento.year + 18, day=28)
    return maioridade.strftime("%d/%m/%Y")


def calcular_idade_completa(data_nascimento: str) -> tuple:
    """Retorna (anos, meses, dias) de idade. Levanta DataFuturaError se futura, ValueError se inválida."""
    data = _normalizar_data(data_nascimento)
    nascimento = datetime.strptime(data, "%d/%m/%Y").date()
    hoje = date.today()

    if nascimento > hoje:
        raise DataFuturaError("A data de nascimento é posterior a hoje.")

    anos = hoje.year - nascimento.year
    meses = hoje.month - nascimento.month
    dias = hoje.day - nascimento.day

    if dias < 0:
        prev_month = hoje.month - 1 if hoje.month > 1 else 12
        prev_year = hoje.year if hoje.month > 1 else hoje.year - 1
        dias += calendar.monthrange(prev_year, prev_month)[1]
        meses -= 1

    if meses < 0:
        meses += 12
        anos -= 1

    return anos, meses, dias


def calcular_idade(data_nascimento: str) -> int:
    """Retorna apenas os anos de idade (compatibilidade)."""
    anos, _, _ = calcular_idade_completa(data_nascimento)
    return anos
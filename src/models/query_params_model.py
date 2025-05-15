from pydantic import BaseModel, model_validator, computed_field
from typing import Optional
    
class QueryParametersModel(BaseModel):
    option: str
    year: Optional[str] = None
    sub_option: Optional[str] = None
    
    _original_option: Optional[str] = None
    _original_year: Optional[str] = None
    _original_sub_option: Optional[str] = None

    model_config = {
        'extra':'forbid'
    }

    @model_validator(mode='after')
    def validate_and_transform_option(self) -> 'QueryParametersModel':
        option_map = {
            'producao':'opcao=opt_02',
            'processamento':'opcao=opt_03',
            'comercializacao':'opcao=opt_04',
            'importacao':'opcao=opt_05',
            'exportacao':'opcao=opt_06',
        }

        if self.option is None or self.option not in option_map:
            raise ValueError(
                'Você precisa escolher uma opção entre (producao, ' 
                'processamento, comercializacao, importacao, exportacao)'
            )

        self._original_option = self.option
        self.option = option_map[self.option]

        return self
        
    @computed_field
    def original_option(self) -> Optional[str]:
        return self._original_option
    
    @model_validator(mode='after')
    def validate_and_transform_year(self) -> 'QueryParametersModel':
        year_map = {
            "until_2024":['importacao', 'exportacao'],
            "until_2023":['producao', 'processamento', 'comercializacao']
        }

        if self.year is None:
            self._original_year = '2023'
            self.year = 'ano=2023'
            return self

        try:
            parsed_year = int(self.year)
        except ValueError:
            raise ValueError(
                'Você digitou um ano inválido. '
                'São aceitos apenas números inteiros.'
                ) 
                
        if self._original_option in year_map['until_2024']:
            
            if not (1970 <= parsed_year <= 2024):
                raise ValueError(
                    'O ano precisa estar no ' 
                    'intervalo entre 1970 e 2024'
                )
            
        if self._original_option in year_map['until_2023']:
                
            if not (1970 <= parsed_year <= 2023):
                raise ValueError(
                    'O ano precisa estar no ' 
                    'intervalo entre 1970 e 2023'
                )
            
        self._original_year = self.year
        self.year = 'ano='+self.year 

        return self  

    @computed_field
    def original_year(self) -> Optional[str]:
        return self._original_year
    
    @model_validator(mode='after')
    def validate_and_set_sub_option(self) -> 'QueryParametersModel':
        sub_options_map = {
            'processamento': {
                'viniferas':'subopcao=subopt_01',
                'americanas_e_hibridas':'subopcao=subopt_02',
                'uvas_de_mesa':'subopcao=subopt_03',
                'sem_classificacao':'subopcao=subopt_04'
            },
            'importacao': {
                'vinhos_de_mesa':'subopcao=subopt_01',
                'espumantes':'subopcao=subopt_02',
                'uvas_frescas':'subopcao=subopt_03',
                'uvas_passas':'subopcao=subopt_04',
                'suco_de_uva':'subopcao=subopt_05'
            },
            'exportacao': {
                'vinhos_de_mesa':'subopcao=subopt_01',
                'espumantes':'subopcao=subopt_02',
                'uvas_frescas':'subopcao=subopt_03',
                'suco_de_uva':'subopcao=subopt_04'
            }
        }

        if self._original_option in sub_options_map:
            valids_sub = sub_options_map[self._original_option]

            if self.sub_option is None:

                self._original_sub_option = list(valids_sub.keys())[0]
                self.sub_option = valids_sub[self._original_sub_option]
                return self

            elif self.sub_option not in valids_sub:
                raise ValueError(
                    "Valor inválido para sub_option com option = "
                    f"'{self._original_option}'. "
                    f"Permitidos: {list(valids_sub.keys())}"
                )
            
            self._original_sub_option = self.sub_option
            self.sub_option = valids_sub[self.sub_option]
            
        else:

            if self.sub_option is not None:
                raise ValueError(
                    "sub_option não é permitido quando option="
                    f"'{self._original_option}'"
                )

        return self
    
    @computed_field
    def original_sub_option(self) -> Optional[str]:
        return self._original_sub_option
        

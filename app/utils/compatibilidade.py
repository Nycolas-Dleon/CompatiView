# Funções que checam a compatibilidade entre as peças do computador
# Não detecta casos de atualização de BIOS nem gargalo por frequência de RAM
from app.utils.data_manager import load_json

motherboards = load_json('motherboards')
cpus = load_json('cpus')
gpus = load_json('gpus')
rams = load_json('rams')

def cpu_motherboard(cpu_name:str, motherboard_name:str) -> bool:

    cpu_socket = cpus[cpu_name]['socket']
    motherboard_socket = motherboards[motherboard_name]['socket']

    return cpu_socket == motherboard_socket

def ram_motherboard(ram_type:str, motherboard_name:str) -> bool:

    if ram_type == motherboards[motherboard_name]['memory_type']:
        return True
    elif motherboards[motherboard_name]['memory_type'] == 'DDR4/DDR5':
        return None
    else:
        return False

def ram_cpu(ram_type:str, cpu_name:str) -> bool:

    return ram_type == cpus[cpu_name]['memory_type']

def arredondar_fonte(valor):

    opcoes = [
        450,
        550,
        650,
        750,
        850,
        1000,
        1200
    ]

    for fonte in opcoes:

        if valor <= fonte:
            return fonte

def fonte(cpu_name, gpu_name):

    cpu_tdp = int(cpus[cpu_name]['tdp'])
    gpu_tdp = int(gpus[gpu_name]['estimated_tdp'])

    total = cpu_tdp + gpu_tdp

    recomendado = int(total * 1.5)

    return arredondar_fonte(recomendado)

def limite_ram(pentes:int, ram_size:int, motherboard_name:str) -> bool:

    build_ram = pentes * ram_size
    supported_ram = motherboards[motherboard_name]['max_memory']

    return build_ram <= supported_ram

def limite_pentes(pentes:int, motherboard_name:str) -> bool:

    return pentes <= motherboards[motherboard_name]['memory_slots']

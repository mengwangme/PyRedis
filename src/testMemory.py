from src.memory import memory

memory.volatile['key'] = 'value'
memory.save_state()